"""
04_robustez.py
¿Cuánto depende la posición de cada universidad de decisiones metodológicas discutibles?
Para el IV y el V se recalcula el índice con especificaciones alternativas razonables
(acotar valores extremos, cambiar la normalización, igualar pesos, quitar un indicador a la vez)
y se reporta, para cada universidad, el intervalo de posiciones dentro de su sector.

Además se marcan valores atípicos: indicadores con |z| > 3 y universidades cuyo índice depende
mayoritariamente de un solo indicador.

Salidas:
  data-raw/tablas/robustez_posiciones.csv          universidad x especificación (posición en sector)
  data-raw/tablas/robustez_resumen.csv             intervalo, mediana y alertas por universidad
  data-raw/tablas/alertas_valores_atipicos.csv     indicador con |z| > 3
"""
import numpy as np
import pandas as pd

from indices import EDICIONES, PROC, cargar, especificaciones, indice, posiciones, preparar

filas, resumen, alertas = [], [], []
for ed in ["IV_2025", "V_2026"]:
    d = cargar(ed)
    pos = {}
    for nombre, kw in especificaciones(ed).items():
        s, _ = indice(d, ed, **kw)
        pos[nombre] = posiciones(d, s)
    P = pd.DataFrame(pos)
    P.insert(0, "posicion_publicada", d.posicion)
    P.insert(0, "institucion", d.institucion)
    P.insert(0, "sector", d.sector)
    P.insert(0, "edicion", ed)
    filas.append(P)

    alt = P.drop(columns=["edicion", "sector", "institucion", "posicion_publicada"])
    s0, C = indice(d, ed)
    # contribución positiva dominante: parte del índice explicada por el indicador de mayor aporte
    top_ind = C.idxmax(axis=1)
    resto = C.sum(axis=1) - C.max(axis=1)
    Z = preparar(d, ed).apply(lambda x: (x - x.mean()) / x.std())
    for i, r in d.iterrows():
        atip = [f"{k} (z={Z.loc[i, k]:+.1f})" for k in Z.columns if abs(Z.loc[i, k]) > 3]
        rango = alt.loc[i].max() - alt.loc[i].min()
        n_sector = (d.sector == r.sector).sum()
        resumen.append(dict(
            edicion=ed, sector=r.sector, institucion=r.institucion,
            posicion_publicada=r.posicion,
            posicion_replica=int(alt.loc[i, "oficial (réplica)"]),
            posicion_mejor=int(alt.loc[i].min()), posicion_peor=int(alt.loc[i].max()),
            posicion_mediana=float(alt.loc[i].median()), amplitud=int(rango), n_sector=n_sector,
            indicador_de_mayor_aporte=top_ind[i],
            indice_sin_ese_indicador=round(resto[i], 3),
            indicadores_atipicos="; ".join(atip),
            # alerta: el indicador de mayor aporte por sí solo convierte un índice bajo el promedio en uno alto,
            # o la posición varía más de un cuarto del sector entre especificaciones
            alerta_dependencia=bool(C.max(axis=1)[i] > 0.3 and resto[i] < 0),
            alerta_inestable=bool(rango > n_sector / 4),
            # alerta de datos: indicadores que dependen de docentes o matrícula en 0 (probable dato faltante en el SIU)
            alerta_datos=bool(ed == "V_2026" and ((d.loc[i, ["PDD", "RED", "DTC", "DR"]] == 0).all() or d.loc[i, "TC"] == 0)),
        ))
        for k in Z.columns:
            if abs(Z.loc[i, k]) > 3:
                alertas.append(dict(edicion=ed, sector=r.sector, institucion=r.institucion, indicador=k,
                                    valor=d.loc[i, k], z=round(Z.loc[i, k], 2),
                                    media=round(d[k].mean(), 3), mediana=round(d[k].median(), 3)))

pd.concat(filas).to_csv(PROC / "robustez_posiciones.csv", index=False)
R = pd.DataFrame(resumen)
R.to_csv(PROC / "robustez_resumen.csv", index=False)
A = pd.DataFrame(alertas).sort_values(["edicion", "z"], ascending=[True, False])
A.to_csv(PROC / "alertas_valores_atipicos.csv", index=False)

pd.set_option("display.width", 250)
for ed in ["IV_2025", "V_2026"]:
    x = R[R.edicion == ed]
    print(f"\n{ed}: amplitud mediana del intervalo de posiciones = {x.amplitud.median():.0f}; "
          f"universidades con alerta de dependencia = {x.alerta_dependencia.sum()}; inestables = {x.alerta_inestable.sum()}")
    print(x[x.alerta_dependencia | x.alerta_inestable][
        ["sector", "institucion", "posicion_publicada", "posicion_mejor", "posicion_peor", "indicador_de_mayor_aporte",
         "indicadores_atipicos"]].to_string(index=False))
print("\nValores atípicos (|z|>3):")
print(A.to_string(index=False))
