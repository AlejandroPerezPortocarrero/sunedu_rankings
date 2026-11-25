"""
02_construir_serie.py
Construye, a partir de las tablas transcritas en data-raw/tablas/, los archivos procesados:
    data-raw/tablas/universidades.csv          identificador único por universidad
    data-raw/tablas/alias_universidades.csv    nombre tal como aparece en cada fuente -> id_univ
    data-raw/tablas/serie_rankings_long.csv    una fila por universidad x ranking
    data-raw/tablas/serie_rankings_wide.csv    posiciones por ranking en columnas
La metodología de cada ranking está en data-raw/tablas/rankings_metodologia.csv
y data-raw/tablas/indicadores_metodologia.csv (editados a mano en data-raw/ a partir de las fuentes).
"""
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = PROC = ROOT / "data-raw" / "tablas"
PROC.mkdir(parents=True, exist_ok=True)
# las fichas metodológicas se editan a mano en data-raw/ y se copian a data-raw/tablas/
for f in ["rankings_metodologia.csv", "indicadores_metodologia.csv"]:
    (PROC / f).write_bytes((ROOT / "data-raw" / f).read_bytes())


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = s.replace('"', "").replace(".", "")
    s = re.sub(r"\b(sac|s a c|sa|s a|srl|s r l)\b", "", s)
    s = re.sub(r"^asociacion civil ", "", s)
    return re.sub(r"\s+", " ", s).strip()


# Variantes históricas de nombre que no coinciden literalmente con el nombre del IV Informe
ALIAS_MANUAL = {
    "universidad nacional de san agustin": "005",
    "universidad nacional hermilio valdizan": "023",
    "universidad nacional san luis gonzaga de ica": "009",
    "universidad privada cesar vallejo": "052",
    "universidad privada san ignacio de loyola": "057",
    "universidad privada marcelino champagnat": "049",
}

# ---------------------------------------------------------------- fuentes
I = pd.read_csv(RAW / "I_2018_ranking_general.csv")
IIw = pd.read_csv(RAW / "II_2020_ranking_wos.csv")
IIs = pd.read_csv(RAW / "II_2020_ranking_scopus.csv")
IIIh = pd.read_csv(RAW / "III_2021_ranking_historico.csv")
IIIe = pd.read_csv(RAW / "III_2021_ranking_excelencia.csv")
IVi = pd.read_csv(RAW / "IV_2025_indicadores.csv", dtype={"codigo": str})
IVr = pd.read_csv(RAW / "IV_2025_ranking.csv", dtype={"codigo_publicado": str})
V = pd.read_csv(RAW / "V_2026_ranking.csv")

# ---------------------------------------------------------------- universidades
codigo = {norm(u): c for u, c in zip(IVi.universidad, IVi.codigo)}
codigo.update(ALIAS_MANUAL)

fuentes = {
    "I_2018_general": I, "II_2020_wos": IIw, "II_2020_scopus": IIs,
    "III_2021_historico": IIIh, "III_2021_excelencia": IIIe,
    "IV_2025": IVr, "V_2026": V,
}
alias = []
for rid, d in fuentes.items():
    for u in d.universidad.unique():
        n = norm(u)
        c = codigo.get(n)
        alias.append(dict(ranking_id=rid, nombre_fuente=u, nombre_normalizado=n,
                          codigo_sunedu=c, id_univ=c if c else "X-" + re.sub(r"[^a-z0-9]+", "-", n)))
alias = pd.DataFrame(alias)

# gestión: IV/V (Pública/Privada) > I (Pública/Asociativa/Societaria) > regla por nombre
gest = {}
for d in (IVi, V):
    for u, g in zip(d.universidad, d.tipo_gestion):
        gest[norm(u)] = g
gest_det = {norm(u): g for u, g in zip(I.universidad, I.tipo_gestion)}
for n, g in gest_det.items():
    gest.setdefault(n, "Pública" if g == "Pública" else "Privada")


def gestion_de(n):
    if n in gest:
        return gest[n]
    return "Pública" if "nacional" in n else "Privada"


alias["gestion"] = alias.nombre_normalizado.map(gestion_de)

# nombre canónico = el más reciente disponible (V > IV > III > II > I)
orden = ["V_2026", "IV_2025", "III_2021_historico", "III_2021_excelencia", "II_2020_scopus", "II_2020_wos", "I_2018_general"]
alias["_o"] = alias.ranking_id.map({r: i for i, r in enumerate(orden)})
canon = alias.sort_values("_o").groupby("id_univ").first()
univ = pd.DataFrame({
    "id_univ": canon.index,
    "codigo_sunedu": canon.codigo_sunedu.values,
    "nombre": canon.nombre_fuente.values,
    "gestion": [gestion_de(n) for n in canon.nombre_normalizado],
})
# tipo de gestión privada detallado (I Informe, 2017): Asociativa/Societaria
det = alias.assign(det=alias.nombre_normalizado.map(gest_det)).dropna(subset=["det"]).groupby("id_univ").det.first()
univ["gestion_detalle_2017"] = univ.id_univ.map(det)
univ = univ.sort_values(["codigo_sunedu", "nombre"], na_position="last")
univ.to_csv(PROC / "universidades.csv", index=False)
alias.drop(columns="_o").to_csv(PROC / "alias_universidades.csv", index=False)

# ---------------------------------------------------------------- serie larga
def apilar(rid, d, sector_col=None):
    x = d[["universidad", "posicion", "puntaje"]].copy()
    x["ranking_id"] = rid
    x["sector_publicado"] = d[sector_col] if sector_col else np.nan
    return x


long = pd.concat([
    apilar("I_2018_general", I),
    apilar("II_2020_wos", IIw),
    apilar("II_2020_scopus", IIs),
    apilar("III_2021_historico", IIIh),
    apilar("III_2021_excelencia", IIIe),
    apilar("IV_2025", IVr, "tipo_gestion"),
    apilar("V_2026", V, "tipo_gestion"),
], ignore_index=True)
long = long.rename(columns={"universidad": "nombre_fuente", "posicion": "posicion_publicada",
                            "puntaje": "puntaje_publicado"})
long = long.merge(alias[["ranking_id", "nombre_fuente", "id_univ", "codigo_sunedu", "gestion"]],
                  on=["ranking_id", "nombre_fuente"], how="left")

meta = pd.read_csv(PROC / "rankings_metodologia.csv")
long = long.merge(meta[["ranking_id", "edicion", "anio_publicacion", "periodo_datos",
                        "ambito_ranking", "grupo_comparabilidad"]], on="ranking_id", how="left")

# "con_dato": la universidad fue efectivamente ordenada. En el I Informe, las universidades con puntaje 0
# empatan en el último puesto (sin producción); en el III, N.A. = sin documentos indizados.
long["con_dato"] = long.posicion_publicada.notna() & (
    (long.puntaje_publicado.fillna(0) > 0) | ~long.ranking_id.isin(["I_2018_general", "II_2020_wos", "II_2020_scopus"])
)
# posición dentro del sector (calculada aquí para los rankings nacionales; publicada en IV y V)
def pos_sector(g):
    return g.puntaje_publicado.rank(ascending=False, method="min")
long["posicion_en_sector"] = np.where(
    long.ambito_ranking.eq("por_sector"), long.posicion_publicada,
    long.where(long.con_dato).groupby(["ranking_id", "gestion"], group_keys=False).apply(pos_sector)
    .reindex(long.index),
)
n_sector = long[long.con_dato | long.ambito_ranking.eq("por_sector")].groupby(["ranking_id", "gestion"]).size()
long["n_en_sector"] = [n_sector.get((r, g), np.nan) for r, g in zip(long.ranking_id, long.gestion)]
long["percentil_en_sector"] = 1 - (long.posicion_en_sector - 1) / long.n_en_sector
cols = ["edicion", "anio_publicacion", "ranking_id", "periodo_datos", "ambito_ranking", "grupo_comparabilidad",
        "id_univ", "codigo_sunedu", "gestion", "nombre_fuente", "posicion_publicada", "puntaje_publicado",
        "con_dato", "posicion_en_sector", "n_en_sector", "percentil_en_sector"]
long = long[cols].sort_values(["anio_publicacion", "ranking_id", "gestion", "posicion_en_sector"])
long.to_csv(PROC / "serie_rankings_long.csv", index=False)

# ---------------------------------------------------------------- serie ancha (posición en sector)
wide = long.pivot_table(index="id_univ", columns="ranking_id", values="posicion_en_sector", aggfunc="first")
wide = wide[[c for c in meta.ranking_id if c in wide.columns]]
wide = univ.set_index("id_univ")[["codigo_sunedu", "nombre", "gestion"]].join(wide, how="right")
wide.sort_values(["gestion", "V_2026"]).to_csv(PROC / "serie_rankings_wide_posicion_en_sector.csv")
print(univ.shape, long.shape, wide.shape)
print("sin código SUNEDU:", univ.codigo_sunedu.isna().sum())
