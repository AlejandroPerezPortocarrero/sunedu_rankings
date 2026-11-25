"""
06_figuras.py
Figuras del README:
  man/figures/concordancia_rankings.png  correlación de Spearman entre rankings (por sector)
  man/figures/robustez_V_2026.png        posición publicada e intervalo bajo especificaciones alternativas (V)
  man/figures/robustez_IV_2025.png       lo mismo para el IV
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from indices import FIG as OUT, PROC

INK, MUTED, GRID = "#1f1f1f", "#7a7a7a", "#e6e6e6"
BLUE, ORANGE = "#257de0", "#f47230"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": GRID, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED})
OUT.mkdir(exist_ok=True)

ETQ = {"I_2018_general": "I 2018", "II_2020_wos": "II 2020 WoS", "II_2020_scopus": "II 2020 Scopus",
       "III_2021_historico": "III 2021", "IV_2025": "IV 2025", "V_2026": "V 2026"}
orden = list(ETQ)

# ------------------------------------------------------------------ 1) concordancia
C = pd.read_csv(PROC / "concordancia_rankings.csv")
cmap = LinearSegmentedColormap.from_list("azul", ["#f5f9ff", "#9dc8f7", "#257de0", "#0e3d7e"])
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), dpi=200)
for ax, sec in zip(axes, ["Privada", "Pública"]):
    M = pd.DataFrame(np.nan, index=orden, columns=orden)
    N = M.copy()
    for _, r in C[C.sector == sec].iterrows():
        M.loc[r.ranking_a, r.ranking_b] = M.loc[r.ranking_b, r.ranking_a] = r.spearman
        N.loc[r.ranking_a, r.ranking_b] = N.loc[r.ranking_b, r.ranking_a] = r.n_comun
    mask = np.tril(np.ones_like(M, dtype=bool))
    ax.imshow(np.where(mask, np.nan, M.values), cmap=cmap, vmin=0.3, vmax=1)
    for i in range(len(orden)):
        for j in range(len(orden)):
            if j > i and pd.notna(M.iat[i, j]):
                v = M.iat[i, j]
                ax.text(j, i, f"{v:.2f}\nn={int(N.iat[i, j])}", ha="center", va="center", fontsize=7,
                        color="white" if v > 0.75 else INK)
    ax.set_xticks(range(len(orden)), [ETQ[o] for o in orden], rotation=40, ha="right")
    ax.set_yticks(range(len(orden)), [ETQ[o] for o in orden])
    ax.set_title("Universidades privadas" if sec == "Privada" else "Universidades públicas", loc="left", color=INK, fontsize=9)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    # separar grupo A / grupo B
    ax.axvline(3.5, color=MUTED, lw=0.8, ls=(0, (2, 2)))
    ax.axhline(3.5, color=MUTED, lw=0.8, ls=(0, (2, 2)))
fig.suptitle("Concordancia entre rankings: correlación de Spearman de las posiciones dentro del sector",
             x=0.01, ha="left", fontsize=10, color=INK)
fig.text(0.01, 0.01, "Calculada sobre las universidades ordenadas en ambos rankings (n). La línea punteada separa el grupo A "
         "(solo investigación, I-III) del grupo B (multidimensional, IV-V).", fontsize=7, color=MUTED)
fig.tight_layout(rect=(0, 0.04, 1, 0.95))
fig.savefig(OUT / "concordancia_rankings.png")
plt.close(fig)

# ------------------------------------------------------------------ 2) robustez
R = pd.read_csv(PROC / "robustez_resumen.csv")
for ed, titulo in [("V_2026", "V Informe (2026)"), ("IV_2025", "IV Informe (2025)")]:
    x = R[R.edicion == ed]
    alto = max(len(x[x.sector == s]) for s in ["Privada", "Pública"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.17 * alto + 1.6), dpi=200)
    for ax, sec in zip(axes, ["Privada", "Pública"]):
        g = x[x.sector == sec].sort_values("posicion_publicada").reset_index(drop=True)
        y = np.arange(len(g))
        ax.hlines(y, g.posicion_mejor, g.posicion_peor, color="#c9c9c9", lw=3, capstyle="round")
        alerta = g.alerta_dependencia | g.alerta_datos
        ax.scatter(g.posicion_publicada[~alerta], y[~alerta], s=16, color=BLUE, zorder=3, edgecolor="white", lw=0.6,
                   label="posición publicada")
        ax.scatter(g.posicion_publicada[alerta], y[alerta], s=22, color=ORANGE, marker="D", zorder=3,
                   edgecolor="white", lw=0.6, label="publicada, con alerta (depende de un solo indicador o datos faltantes)")
        nombres = g.institucion.str.replace("Universidad Nacional", "U. N.").str.replace("Universidad", "U.") \
                               .str.replace(r" S\.?A\.?C\.?$| S\.R\.L\.$| S\.A\.$| SAC$", "", regex=True)
        ax.set_yticks(y, nombres, fontsize=6.5, color=INK)
        ax.set_ylim(len(g) - 0.4, -0.6)
        ax.set_xlim(0, len(g) + 1)
        ax.set_xlabel("Posición dentro del sector")
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        for s in ["top", "right", "left"]:
            ax.spines[s].set_visible(False)
        ax.tick_params(length=0)
        ax.set_title("Privadas" if sec == "Privada" else "Públicas", loc="left", color=INK, fontsize=9)
    h, l = axes[0].get_legend_handles_labels()
    h.insert(0, plt.Line2D([], [], color="#c9c9c9", lw=3))
    l.insert(0, "intervalo de posiciones bajo especificaciones alternativas")
    fig.legend(h, l, loc="upper left", bbox_to_anchor=(0.01, 0.985), ncol=3, frameon=False, fontsize=7)
    fig.suptitle(f"{titulo}: ¿cuánto depende cada posición de las decisiones metodológicas?", x=0.01, y=0.998,
                 ha="left", fontsize=10, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(OUT / f"robustez_{ed}.png")
    plt.close(fig)
print("figuras listas")

# copias para las viñetas (man/figures no se instala con el paquete)
import shutil
VIG = OUT.parents[1] / "vignettes" / "figures"
VIG.mkdir(parents=True, exist_ok=True)
for f in ["concordancia_rankings.png", "robustez_V_2026.png"]:
    shutil.copy(OUT / f, VIG / f)
