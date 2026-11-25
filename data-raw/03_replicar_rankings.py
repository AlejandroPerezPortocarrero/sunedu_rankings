"""
03_replicar_rankings.py
Reproduce los puntajes publicados a partir de los indicadores publicados (II, IV y V Informe),
lo que valida la transcripción y la lectura de la metodología. También guarda, para el IV y el V,
la contribución de cada indicador al índice de cada universidad (z-score x peso).
El V aplica bonificadores cuyos valores por universidad no se publicaron: su réplica es aproximada.
"""
import pandas as pd

from indices import OUT, PROC, RAW, cargar, indice, posiciones, reescalar

OUT.mkdir(exist_ok=True)
log = []

for base in ["wos", "scopus"]:
    d = pd.read_csv(RAW / f"II_2020_ranking_{base}.csv")
    X = d[["produccion_per_capita", "impacto_cientifico_h5", "excelencia_internacional_top10"]]
    s = ((X - X.mean()) / X.std()).mean(axis=1)
    r = 100 * (s - s.min()) / (s.max() - s.min())
    e = (r - d.puntaje).abs()
    log.append(f"II {base:6s}: error absoluto medio {e.mean():.2f} pts (máx. {e.max():.2f})")

I = pd.read_csv(RAW / "I_2018_ranking_general.csv")
areas = I[[c for c in I if c.startswith("puntaje_") and c != "puntaje"]].mean(axis=1)
e = (100 * areas / areas.max() - I.puntaje).abs()
log.append(f"I        : puntaje general desde los 6 puntajes por área, error máx. {e.max():.3f} pts")

for ed in ["IV_2025", "V_2026"]:
    d = cargar(ed)
    s, C = indice(d, ed)
    d["replica"] = reescalar(d, s, ed)
    d["posicion_replica"] = posiciones(d, s)
    for sec, g in d.groupby("sector"):
        rho = g[["puntaje", "replica"]].corr(method="spearman").iloc[0, 1]
        log.append(f"{ed} {sec:8s}: Spearman {rho:.3f}; error absoluto medio {(g.puntaje - g.replica).abs().mean():.2f} pts")
    C.insert(0, "institucion", d.institucion)
    C.insert(0, "sector", d.sector)
    C["indice"] = s
    C.to_csv(PROC / f"{ed}_contribuciones_por_indicador.csv", index=False)
    d.to_csv(PROC / f"{ed}_indicadores_y_replica.csv", index=False)

# ---------------------------------------------------------------- coherencia de las tablas transcritas
for f, grupo in [("II_2020_ranking_wos.csv", None), ("II_2020_ranking_scopus.csv", None),
                 ("III_2021_ranking_historico.csv", None), ("III_2021_ranking_excelencia.csv", None),
                 ("IV_2025_ranking.csv", "tipo_gestion"), ("V_2026_ranking.csv", "tipo_gestion")]:
    t = pd.read_csv(RAW / f).dropna(subset=["posicion"])
    for _, g in (t.groupby(grupo) if grupo else [(None, t)]):
        assert list(g.posicion) == list(range(1, len(g) + 1)), f"posiciones no secuenciales en {f}"
        assert g.puntaje.is_monotonic_decreasing, f"puntajes no monótonos en {f}"
I32 = I[I.puntaje > 0]
assert len(I32) == 32 and list(I32.posicion) == list(range(1, 33))
log.append("Tablas transcritas: posiciones secuenciales y puntajes monótonos en todos los rankings; "
           "32 universidades con puntaje > 0 en el I")
log.append("(V sin bonificadores; IV y V con z-score sobre públicas y privadas juntas, reescalado por sector)")
print("\n".join(log))
(OUT / "replicacion.txt").write_text("\n".join(log), encoding="utf-8")
