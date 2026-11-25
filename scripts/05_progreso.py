"""
05_progreso.py
¿Qué se puede decir sobre el progreso de las universidades a partir de los rankings de SUNEDU?

1) Concordancia entre rankings: correlación de Spearman de las posiciones dentro del sector
   entre cada par de rankings (solo universidades ordenadas en ambos).
2) Grupo A (I, II y III; solo investigación): estratos por edición y estabilidad.
3) Grupo B (IV -> V): un cambio de posición se califica como "robusto" solo si el intervalo de
   posiciones del V (bajo especificaciones alternativas, ver 04_robustez.py) no se superpone con
   el del IV. Aun así, un cambio robusto mezcla desempeño y cambio metodológico.
4) Tamaño del universo ordenado en cada ranking (los cambios de universo mueven posiciones).

Salidas en data/processed/: concordancia_rankings.csv, grupoA_estratos.csv,
grupoB_cambio_IV_V.csv, universo_por_ranking.csv
"""
import itertools

import numpy as np
import pandas as pd

from indices import PROC, ROOT

L = pd.read_csv(PROC / "serie_rankings_long.csv", dtype={"codigo_sunedu": str})
L = L[L.con_dato]
U = pd.read_csv(PROC / "universidades.csv", dtype={"codigo_sunedu": str}).set_index("id_univ")
orden = ["I_2018_general", "II_2020_wos", "II_2020_scopus", "III_2021_historico", "IV_2025", "V_2026"]

# ------------------------------------------------------------------ 4) universo
uni = L.groupby(["ranking_id", "gestion"]).size().unstack().reindex(orden + ["III_2021_excelencia"])
uni.to_csv(PROC / "universo_por_ranking.csv")
print("Universidades ordenadas por ranking y sector:\n", uni, "\n")

# ------------------------------------------------------------------ 1) concordancia
W = L.pivot_table(index=["id_univ", "gestion"], columns="ranking_id", values="posicion_en_sector", aggfunc="first")
filas = []
for sec in ["Privada", "Pública"]:
    w = W.xs(sec, level="gestion")
    for a, b in itertools.combinations(orden, 2):
        x = w[[a, b]].dropna()
        if len(x) >= 8:
            # re-rankear dentro de la intersección para que el universo sea común
            rho = x[a].rank().corr(x[b].rank())
            top10_a = set(x[a].rank().nsmallest(10).index)
            top10_b = set(x[b].rank().nsmallest(10).index)
            filas.append(dict(sector=sec, ranking_a=a, ranking_b=b, n_comun=len(x), spearman=round(rho, 3),
                              coincidencia_top10=len(top10_a & top10_b)))
C = pd.DataFrame(filas)
C.to_csv(PROC / "concordancia_rankings.csv", index=False)
print(C.to_string(index=False), "\n")

# ------------------------------------------------------------------ 2) grupo A: estratos
A_ids = ["I_2018_general", "II_2020_wos", "III_2021_historico"]


def estrato(p):
    if pd.isna(p):
        return "sin producción / no listada"
    return "1-5" if p <= 5 else "6-10" if p <= 10 else "11-20" if p <= 20 else ">20"


WA = W[A_ids].reset_index()
for c in A_ids:
    WA[f"estrato_{c}"] = WA[c].map(estrato)
def clasif(r):
    p = [r[c] for c in A_ids]
    if all(pd.notna(x) and x <= 5 for x in p):
        return "siempre en el top 5"
    if all(pd.notna(x) and x <= 10 for x in p):
        return "siempre en el top 10"
    if pd.isna(p[0]) and pd.notna(p[2]):
        return "entra a la lista (sin producción indexada en 2014-16)"
    if all(pd.notna(x) for x in p):
        return "rango amplio" if max(p) - min(p) >= 10 else "estable fuera del top 10"
    return "cobertura incompleta"
WA["patron_grupo_A"] = WA.apply(clasif, axis=1)
WA.insert(1, "nombre", WA.id_univ.map(U.nombre))
WA.sort_values(["gestion", "III_2021_historico"]).to_csv(PROC / "grupoA_estratos.csv", index=False)
print(WA.groupby(["gestion", "patron_grupo_A"]).size(), "\n")

# ------------------------------------------------------------------ 3) grupo B: IV -> V
R = pd.read_csv(PROC / "robustez_resumen.csv")
alias = pd.read_csv(PROC / "alias_universidades.csv", dtype={"codigo_sunedu": str})
mapa = {}
for rid, ed in [("IV_2025", "IV_2025"), ("V_2026", "V_2026")]:
    a = alias[alias.ranking_id == rid].set_index("nombre_fuente").id_univ
    mapa[ed] = a
# los nombres del IV en robustez vienen de la tabla de indicadores: mapear por código
ind4 = pd.read_csv(ROOT / "data/raw/IV_2025_indicadores.csv", dtype={"codigo": str}).set_index("universidad").codigo
R["id_univ"] = np.where(R.edicion == "IV_2025", R.institucion.map(ind4), R.institucion.map(mapa["V_2026"]))
assert R.id_univ.notna().all()
cols = ["posicion_publicada", "posicion_mejor", "posicion_peor", "posicion_mediana"]
B = R[R.edicion == "IV_2025"].set_index("id_univ")[["sector"] + cols].join(
    R[R.edicion == "V_2026"].set_index("id_univ")[cols], lsuffix="_IV", rsuffix="_V", how="outer")
B.insert(0, "nombre", B.index.map(U.nombre))
B["sector"] = B.sector.fillna(pd.Series(B.index.map(U.gestion), index=B.index))


def cambio(r):
    if pd.isna(r.posicion_publicada_IV):
        return "solo en V"
    if pd.isna(r.posicion_publicada_V):
        return "solo en IV"
    if r.posicion_peor_V < r.posicion_mejor_IV:
        return "sube (robusto a la ponderación)"
    if r.posicion_mejor_V > r.posicion_peor_IV:
        return "baja (robusto a la ponderación)"
    return "no concluyente"


B["cambio_publicado"] = B.posicion_publicada_IV - B.posicion_publicada_V  # + = sube
B["clasificacion"] = B.apply(cambio, axis=1)
B = B.sort_values(["sector", "posicion_publicada_V"])
B.to_csv(PROC / "grupoB_cambio_IV_V.csv")
print(B.groupby(["sector", "clasificacion"]).size())
print(B[B.clasificacion.str.contains("robusto")][["nombre", "sector", "posicion_publicada_IV", "posicion_publicada_V",
                                                 "posicion_mejor_IV", "posicion_peor_IV", "posicion_mejor_V",
                                                 "posicion_peor_V", "clasificacion"]].to_string())
big = B[(B.cambio_publicado.abs() >= 10) & (B.clasificacion == "no concluyente")]
print(f"\nCambios publicados de 10 o más puestos que no son robustos: {len(big)} de "
      f"{(B.cambio_publicado.abs() >= 10).sum()}")
