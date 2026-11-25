"""
04_grafico_trayectorias.py
Posición dentro del sector privado en cada ranking (posición calculada para los rankings
nacionales I-III; publicada para IV y V). Destaca a la USMP.
Ojo: los rankings de grupos distintos NO son comparables; el gráfico solo muestra trayectorias
descriptivas y marca el quiebre metodológico.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
w = pd.read_csv(ROOT / "data/processed/serie_rankings_wide_posicion_en_sector.csv", dtype={"codigo_sunedu": str})
cols = ["I_2018_general", "II_2020_wos", "III_2021_historico", "IV_2025", "V_2026"]
etiquetas = ["I (2018)\nWoS 2014-16", "II (2020)\nWoS 2016-18", "III (2021)\nWoS 1980-2020", "IV (2025)\nmultidim.", "V (2026)\nmultidim."]
priv = w[w.gestion == "Privada"].copy()
top = priv[(priv[cols] <= 8).any(axis=1)]

cortos = {
    "014": "Cayetano Heredia", "008": "PUCP", "019": "San Martín de Porres", "068": "Científica del Sur",
    "054": "UPC", "017": "Pacífico", "029": "Piura", "018": "Lima", "132": "UTEC", "057": "San Ignacio de Loyola",
    "052": "César Vallejo", "079": "ESAN", "030": "Ricardo Palma", "067": "Continental",
}
INK, MUTED, GRID, HI = "#1f1f1f", "#8a8a8a", "#e6e6e6", "#f47230"
fig, ax = plt.subplots(figsize=(10, 7.2), dpi=200)
x = range(len(cols))
ax.axvspan(2.5, 4.4, color="#f4f4f4", zorder=0)
ax.text(1, 1.01, "Solo investigación · ranking nacional\n(posición entre privadas, calculada)", ha="center", va="bottom", fontsize=8, color=MUTED, transform=ax.get_xaxis_transform())
ax.text(3.5, 1.01, "Multidimensional · ranking por sector\n(posición publicada)", ha="center", va="bottom", fontsize=8, color=MUTED, transform=ax.get_xaxis_transform())
for _, r in top.iterrows():
    es = r.codigo_sunedu == "019"
    y = r[cols].values.astype(float)
    ax.plot(x, y, color=HI if es else "#c4c4c4", lw=2.6 if es else 1.3, marker="o", ms=6 if es else 4,
            mec="white", mew=1.2, zorder=3 if es else 2)
    last = [i for i in range(len(cols)) if pd.notna(y[i])][-1]
    if y[last] <= 30:
        ax.text(last + 0.08, y[last], cortos.get(r.codigo_sunedu, r.nombre), va="center", fontsize=8,
                color=INK if es else MUTED, fontweight="bold" if es else "normal")
ax.set_ylim(30, 0.3)
ax.set_yticks([1, 5, 10, 15, 20, 25, 30])
ax.set_xticks(list(x), etiquetas, fontsize=8, color=INK)
ax.set_xlim(-0.3, 4.9)
ax.set_ylabel("Posición entre universidades privadas", fontsize=9, color=INK)
ax.grid(axis="y", color=GRID, lw=0.8)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=MUTED, length=0)
ax.set_title("Universidades privadas en los rankings de los Informes Bienales de SUNEDU",
             loc="left", fontsize=11, color=INK, pad=34)
fig.text(0.01, 0.01, "Universidades que estuvieron alguna vez entre las 8 primeras privadas. Los rankings a ambos lados de la zona sombreada usan "
         "metodologías distintas y no son comparables entre sí.", fontsize=7, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
(ROOT / "output").mkdir(exist_ok=True)
fig.savefig(ROOT / "output/trayectorias_privadas.png")
