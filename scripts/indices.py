"""
indices.py
Funciones comunes: carga de los indicadores publicados del IV y V Informe y cálculo del índice
compuesto bajo distintas especificaciones (la oficial y alternativas razonables).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "output"

# ------------------------------------------------------------------ definición de cada edición
EDICIONES = {
    "IV_2025": dict(
        pesos={"DE": .15, "TPT": .15, "PI": .7 / 3, "PAC": .7 / 3, "IN": .7 / 3},
        ambitos={"Formativo": ["DE", "TPT"], "Investigación": ["PI", "PAC", "IN"]},
        # TPT entra como complemento (1 - TPT): tras estandarizar equivale a -TPT
        transformar={"TPT": lambda x: -x},
        reescala=(0, 100),
    ),
    "V_2026": dict(
        pesos={**{k: .9 / 7 for k in ["PDD", "RED", "TC", "PIN", "PIC", "PAC", "DR"]},
               **{k: .1 / 3 for k in ["DTC", "TPT", "TPB"]}},
        ambitos={"Formativo": ["PDD", "RED", "TC"], "Investigación": ["PIN", "PIC", "PAC", "DR"],
                 "Capacidad institucional": ["DTC", "TPT", "TPB"]},
        # RED, TPT y TPB entran "mediante la inversa"
        transformar={k: (lambda x: 1 / x.replace(0, np.nan)) for k in ["RED", "TPT", "TPB"]},
        reescala=(1, 100),
    ),
}


def cargar(edicion):
    """DataFrame con sector, institucion, id (código o nombre), indicadores, puntaje y posición publicados."""
    if edicion == "IV_2025":
        ind = pd.read_csv(RAW / "IV_2025_indicadores.csv", dtype={"codigo": str})
        rk = pd.read_csv(RAW / "IV_2025_ranking.csv", dtype={"codigo_publicado": str})
        rk["codigo"] = rk.codigo_publicado.str[:3]
        d = ind.merge(rk[["codigo", "puntaje", "posicion"]], on="codigo")
        return d.rename(columns={"tipo_gestion": "sector", "universidad": "institucion"})
    lg = pd.read_csv(RAW / "V_analisis_por_indicador_long.csv")
    lg = lg[lg.tabla != 3].copy()  # la tabla 3 duplica la 13
    lg["sector"] = np.where(lg.tabla == 17, "Privada", lg.sector_titulo)  # la 17 está mal rotulada
    d = lg.pivot_table(index=["sector", "institucion"], columns="indicador", values="valor", aggfunc="first").reset_index()
    pub = pd.read_csv(RAW / "V_2026_ranking.csv").rename(columns={"universidad": "institucion", "tipo_gestion": "sector"})
    d = d.merge(pub, on=["sector", "institucion"], how="left")
    assert d.puntaje.notna().all()
    return d


def _z(x):
    return (x - x.mean()) / x.std()


def preparar(d, edicion, winsor=None):
    """Aplica las transformaciones de sentido; opcionalmente winsoriza en los percentiles (p, 1-p)."""
    cfg = EDICIONES[edicion]
    X = d[list(cfg["pesos"])].astype(float).copy()
    for k, f in cfg["transformar"].items():
        X[k] = f(X[k])
    X = X.fillna(X.min())  # V: 3 públicas con 0 docentes registrados -> RED indefinido -> mínimo
    if winsor:
        X = X.clip(X.quantile(winsor), X.quantile(1 - winsor), axis=1)
    return X


def indice(d, edicion, pesos=None, normalizacion="z", tope_z=None, winsor=None):
    """Índice compuesto (sin bonificadores). Devuelve (índice, matriz de contribuciones)."""
    cfg = EDICIONES[edicion]
    pesos = pd.Series(pesos or cfg["pesos"], dtype=float)
    pesos = pesos / pesos.sum()
    X = preparar(d, edicion, winsor)
    if normalizacion == "z":
        Z = X.apply(_z)
    elif normalizacion == "percentil":
        Z = X.rank(pct=True)
    elif normalizacion == "minmax":
        Z = (X - X.min()) / (X.max() - X.min())
    if tope_z is not None:
        Z = Z.clip(-tope_z, tope_z)
    C = Z[pesos.index] * pesos
    return C.sum(axis=1), C


def posiciones(d, s):
    return s.groupby(d.sector).rank(ascending=False, method="min").astype(int)


def reescalar(d, s, edicion):
    lo, hi = EDICIONES[edicion]["reescala"]
    return s.groupby(d.sector).transform(lambda v: lo + (hi - lo) * (v - v.min()) / (v.max() - v.min()))


def especificaciones(edicion):
    """Especificaciones alternativas razonables para el análisis de robustez."""
    cfg = EDICIONES[edicion]
    specs = {"oficial (réplica)": {}}
    specs["z acotado a ±3"] = dict(tope_z=3)
    specs["winsorización p5-p95"] = dict(winsor=0.05)
    specs["normalización por percentiles"] = dict(normalizacion="percentil")
    specs["normalización min-max"] = dict(normalizacion="minmax")
    eq = {}
    for amb, inds in cfg["ambitos"].items():
        for i in inds:
            eq[i] = 1 / len(cfg["ambitos"]) / len(inds)
    specs["ámbitos con igual peso"] = dict(pesos=eq)
    specs["todos los indicadores con igual peso"] = dict(pesos={k: 1 for k in cfg["pesos"]})
    for k in cfg["pesos"]:
        specs[f"sin {k}"] = dict(pesos={j: w for j, w in cfg["pesos"].items() if j != k})
    return specs
