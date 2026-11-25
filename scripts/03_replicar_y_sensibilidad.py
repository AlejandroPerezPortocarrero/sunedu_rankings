"""
03_replicar_y_sensibilidad.py
1) Reproduce los puntajes publicados a partir de los indicadores publicados (II, IV y V Informe).
2) Descompone el puntaje del V Informe por indicador (contribución = z-score x peso).
3) Análisis de sensibilidad de la posición de la Universidad de San Martín de Porres (USMP)
   en el ranking de privadas del V Informe.

Salidas en data/processed/ y output/.
Advertencia: el V Informe aplica bonificadores cuyos valores por universidad no se publicaron;
la réplica del V es SIN bonificadores y por ello aproximada.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "output"
OUT.mkdir(exist_ok=True)


def z(x):
    return (x - x.mean()) / x.std()


def minmax(s, lo=0, hi=100):
    return lo + (hi - lo) * (s - s.min()) / (s.max() - s.min())


lineas = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    lineas.append(s)


# ============================================================ II Informe
for base in ["wos", "scopus"]:
    d = pd.read_csv(RAW / f"II_2020_ranking_{base}.csv")
    X = d[["produccion_per_capita", "impacto_cientifico_h5", "excelencia_internacional_top10"]]
    r = minmax(X.apply(z).mean(axis=1))
    log(f"II {base}: error absoluto medio de la réplica = {(r - d.puntaje).abs().mean():.2f} pts "
        f"(máx {(r - d.puntaje).abs().max():.2f})")

# ============================================================ IV Informe
ind = pd.read_csv(RAW / "IV_2025_indicadores.csv", dtype={"codigo": str})
rk = pd.read_csv(RAW / "IV_2025_ranking.csv", dtype={"codigo_publicado": str})
rk["codigo"] = rk.codigo_publicado.str[:3]
m4 = ind.merge(rk[["codigo", "puntaje", "posicion"]], on="codigo")
W4 = {"DE": .15, "TPT": .15, "PI": .7 / 3, "PAC": .7 / 3, "IN": .7 / 3}
X = m4[list(W4)].astype(float).copy()
X["TPT"] = -X["TPT"]  # entra como complemento (1 - TPT): equivalente a -TPT tras estandarizar
s4 = (X.apply(z) * pd.Series(W4)).sum(axis=1)
m4["replica"] = s4.groupby(m4.tipo_gestion).transform(minmax)
e = (m4.replica - m4.puntaje).abs()
log(f"IV: error absoluto medio de la réplica = {e.mean():.2f} pts (máx {e.max():.2f}); "
    "z-score sobre el conjunto público+privado, reescalado por sector")

# ============================================================ V Informe
lg = pd.read_csv(RAW / "V_analisis_por_indicador_long.csv")
lg = lg[lg.tabla != 3].copy()            # la tabla 3 duplica la tabla 13 (RED privadas)
lg["sector"] = np.where(lg.tabla == 17, "Privada", lg.sector_titulo)  # la tabla 17 está mal rotulada como 'Públicas'
v = lg.pivot_table(index=["sector", "institucion"], columns="indicador", values="valor", aggfunc="first").reset_index()
pub = pd.read_csv(RAW / "V_2026_ranking.csv").rename(columns={"universidad": "institucion", "tipo_gestion": "sector"})
v = v.merge(pub, on=["sector", "institucion"], how="left")
assert v.puntaje.notna().all()
v.to_csv(PROC / "V_2026_indicadores_wide.csv", index=False)

W5 = {"PDD": 90 / 7, "RED": 90 / 7, "TC": 90 / 7, "PIN": 90 / 7, "PIC": 90 / 7, "PAC": 90 / 7, "DR": 90 / 7,
      "DTC": 10 / 3, "TPT": 10 / 3, "TPB": 10 / 3}
W5 = {k: w / 100 for k, w in W5.items()}
INVERSOS = ["RED", "TPT", "TPB"]


def puntaje_V(df, pesos=W5):
    X = df[list(W5)].astype(float).copy()
    for c in INVERSOS:
        X[c] = 1 / X[c].replace(0, np.nan)
    X = X.fillna(X.min())  # 3 públicas reportan RED = 0 (sin docentes registrados): se les asigna el mínimo
    Z = X.apply(z)
    contrib = Z * pd.Series(pesos)
    total = contrib.sum(axis=1)
    out = df[["sector", "institucion", "puntaje", "posicion"]].copy()
    out["indice"] = total
    out["replica_1_100"] = total.groupby(df.sector).transform(lambda s: minmax(s, 1, 100))
    out["posicion_replica"] = total.groupby(df.sector).rank(ascending=False).astype(int)
    return out, contrib


base, contrib = puntaje_V(v)
for sec, g in base.groupby("sector"):
    log(f"V {sec}: correlación de Spearman réplica vs. publicado = "
        f"{g[['puntaje', 'replica_1_100']].corr(method='spearman').iloc[0, 1]:.3f}; "
        f"error absoluto medio = {(g.puntaje - g.replica_1_100).abs().mean():.1f} pts (sin bonificadores)")
base.to_csv(PROC / "V_2026_replica.csv", index=False)

contrib.insert(0, "institucion", v.institucion)
contrib.insert(0, "sector", v.sector)
contrib["indice_sin_bonif"] = contrib[list(W5)].sum(axis=1)
contrib.to_csv(PROC / "V_2026_contribuciones_por_indicador.csv", index=False)

USMP = "Universidad de San Martín de Porres"
c = contrib.set_index("institucion").loc[USMP, list(W5)]
log("\nUSMP - contribución de cada indicador al índice (z x peso):")
for k, val in c.items():
    log(f"   {k:4s} {val:+.3f}")
log(f"   total {c.sum():+.3f} ; sin PIN {c.drop('PIN').sum():+.3f}")
zp = (v.PIN - v.PIN.mean()) / v.PIN.std()
log(f"USMP: FWCI promedio = {v.set_index('institucion').PIN[USMP]:.2f}; z = {zp[v.institucion == USMP].iloc[0]:.1f} "
    f"desviaciones estándar (media del conjunto {v.PIN.mean():.2f}, mediana {v.PIN.median():.2f})")

# ------------------------------------------------------------ sensibilidad
def pos_usmp(df, pesos=W5):
    o, _ = puntaje_V(df, pesos)
    o = o[o.sector == "Privada"]
    return int(o.loc[o.institucion == USMP, "posicion_replica"].iloc[0])


escenarios = []
def esc(nombre, df=None, pesos=W5):
    escenarios.append(dict(escenario=nombre, posicion_USMP_privadas=pos_usmp(v if df is None else df, pesos)))

esc("Réplica base (sin bonificadores)")
pesos_sin_pin = dict(W5, PIN=0)
esc("Sin el indicador PIN (los demás pesos sin cambio)", pesos=pesos_sin_pin)
for tope in [3.0, 2.0, 1.5]:
    d = v.copy(); d["PIN"] = d.PIN.clip(upper=tope)
    esc(f"PIN con tope de {tope}", d)
d = v.copy(); d.loc[d.institucion == USMP, "PIN"] = d.loc[d.sector == "Privada", "PIN"].median()
esc("PIN de la USMP = mediana de las privadas", d)
d = v.copy(); d.loc[d.institucion == USMP, "PIN"] = 1.0
esc("PIN de la USMP = 1,0 (promedio mundial)", d)
d = v.copy(); d["PIN"] = d.PIN * d.PIC
esc("PIN ponderado por volumen (como en el IV: impacto x publicaciones; aprox. con PIC)", d)
esc_df = pd.DataFrame(escenarios)
esc_df.to_csv(PROC / "V_2026_sensibilidad_USMP.csv", index=False)
log("\nSensibilidad - posición de la USMP entre privadas (publicada: 2):")
log(esc_df.to_string(index=False))

(OUT / "resultados_replicacion.txt").write_text("\n".join(lineas), encoding="utf-8")
