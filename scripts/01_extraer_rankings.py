"""
01_extraer_rankings.py
Extrae (transcribe) las tablas de ranking publicadas en los Informes Bienales de SUNEDU
a archivos CSV en data/raw/, tal como aparecen en las fuentes (sin corregir nombres).

Uso:
    python scripts/01_extraer_rankings.py <carpeta_con_fuentes>

La carpeta debe contener los documentos originales con estos nombres
(ver docs/fuentes.md para los enlaces de descarga):
    I_informe_bienal_2018.pdf
    II_informe_bienal_2020.pdf
    III_informe_bienal_2021.pdf
    IV_informe_bienal_2025.pdf
    V_ranking_universitario_2026.pdf
    V_analisis_por_indicador_2026.docx

Requiere: pdftotext (poppler-utils), python-docx, pandas.
"""
import itertools
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fuentes")
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def pdftext(pdf, first, last):
    """Texto 'raw' (orden de flujo de contenido) de un rango de páginas del PDF."""
    out = subprocess.run(
        ["pdftotext", "-f", str(first), "-l", str(last), "-raw", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def num(s):
    """'1 174' -> 1174 ; '81,04' -> 81.04 ; 'N.A.' -> None"""
    s = s.strip().replace(" ", " ")
    if s in {"N.A.", "NA", "ND", ""}:
        return None
    s = s.replace(" ", "").replace(",", ".")
    return float(s)


# ---------------------------------------------------------------------------
# I Informe Bienal (2018) - Anexo F: Ranking de universidades - General
# Páginas del PDF 65-67 (impresas 128-133). 6 áreas OCDE + puntaje general.
# ---------------------------------------------------------------------------
def extraer_I():
    t = re.sub(r"\s+", " ", pdftext(SRC / "I_informe_bienal_2018.pdf", 65, 67))
    pat = re.compile(
        r"(\d{1,3}) ([A-ZÁÉÍÓÚ][^\d]+?) (\d+) ([A-Za-zÁÉÍÓÚáéíóúñ\- ]+?) "
        r"(Pública|Asociativa|Societaria) (\d+|ND) "
        r"(Licenciada|Autorización Definitiva|Autorización Provisional)"
        r"((?: \d+ [\d\.]+){6}) ([\d\.]+) ([\d\.]+)"
    )
    areas = ["cn", "it", "mcs", "ca", "cs", "hum"]
    rows = []
    for m in pat.finditer(t):
        pares = m.group(8).split()
        r = dict(
            posicion=int(m.group(1)), universidad=m.group(2).strip(),
            anios_al_2016=int(m.group(3)), sede=m.group(4).strip(),
            tipo_gestion=m.group(5),
            n_programas_pregrado_2015=None if m.group(6) == "ND" else int(m.group(6)),
            autorizacion_licencia=m.group(7),
        )
        for i, a in enumerate(areas):
            r[f"rank_{a}"] = int(pares[2 * i])
            r[f"puntaje_{a}"] = float(pares[2 * i + 1])
        r["produccion_cientifica"] = float(m.group(9))
        r["puntaje"] = float(m.group(10))
        rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(RAW / "I_2018_ranking_general.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# II Informe Bienal (2020) - Tablas 3.1 (Web of Science) y 3.2 (Scopus)
# El texto del PDF trae primero la lista de nombres y luego cada columna completa.
# ---------------------------------------------------------------------------
def _bloque_columnas(texto, n):
    nombres = re.findall(r"^(\d{1,2}) (Universidad.+|Pontificia.+)$", texto, re.M)
    nombres = nombres[:n]
    assert [int(a) for a, _ in nombres] == list(range(1, n + 1)), "orden de nombres"
    # tokens numéricos posteriores al último nombre
    resto = texto.split(nombres[-1][1], 1)[1]
    toks = re.findall(r"^\s*(\d+(?:,\d+)?)\s*$", resto, re.M)
    cols = [toks[i * n:(i + 1) * n] for i in range(4)]
    return nombres, cols


def extraer_II():
    pdf = SRC / "II_informe_bienal_2020.pdf"
    out = {}
    for base, pag, n in [("wos", 110, 45), ("scopus", 112, 53)]:
        t = pdftext(pdf, pag, pag)
        if base == "scopus":
            # la pág. 112 contiene la capa completa de 53 filas
            t = t.split("Tabla 3.2")[-1] if "Tabla 3.2" in t else t
        nombres, cols = _bloque_columnas(t, n)
        df = pd.DataFrame({
            "posicion": [int(a) for a, _ in nombres],
            "universidad": [b.strip() for _, b in nombres],
            "puntaje": [num(x) for x in cols[0]],
            "produccion_per_capita": [num(x) for x in cols[1]],
            "impacto_cientifico_h5": [num(x) for x in cols[2]],
            "excelencia_internacional_top10": [num(x) for x in cols[3]],
        })
        df.to_csv(RAW / f"II_2020_ranking_{base}.csv", index=False)
        out[base] = df
    return out


# ---------------------------------------------------------------------------
# III Informe Bienal (2021) - Tabla 4.3 Ranking histórico y Tabla 4.4 Excelencia
# ---------------------------------------------------------------------------
def extraer_III():
    t = pdftext(SRC / "III_informe_bienal_2021.pdf", 207, 210)
    hist_txt = t.split("Tabla 4.3")[1].split("4.5.2.")[0]
    exc_txt = t.split("Tabla 4.4")[1].split("Nota:")[0]
    filas = re.findall(r"^(\d{1,2}|-) (.+?) (\d+(?:,\d+)?|N\.A\.)$", hist_txt, re.M)
    hist = pd.DataFrame(
        [dict(posicion=None if p == "-" else int(p), universidad=u.strip(), puntaje=num(s))
         for p, u, s in filas]
    )
    filas = re.findall(r"^(\d{1,2}) (.+?) (\d+(?:,\d+)?)$", exc_txt, re.M)
    exc = pd.DataFrame([dict(posicion=int(p), universidad=u.strip(), puntaje=num(s)) for p, u, s in filas])
    hist.to_csv(RAW / "III_2021_ranking_historico.csv", index=False)
    exc.to_csv(RAW / "III_2021_ranking_excelencia.csv", index=False)
    return hist, exc


# ---------------------------------------------------------------------------
# IV Informe Bienal (2025) - tablas de indicadores y de ranking (públicas / privadas)
# ---------------------------------------------------------------------------
def extraer_IV():
    t = pdftext(SRC / "IV_informe_bienal_2025.pdf", 195, 202)
    flat = re.sub(r"\s+", " ", t)
    # Las cifras con separador de miles (p. ej. "3 892") hacen ambiguo el corte entre columnas;
    # se resuelve probando todas las particiones válidas y exigiendo PAC <= PI.
    filas = re.findall(
        r"(\d{3}) ((?:Universidad|Pontificia|Asociación)[^\d]+?) (Pública|Privada) (\d+,\d+) (\d+,\d+) "
        r"([\d ]+?)(?= \d{3} (?:Universidad|Pontificia|Asociación)| Estandarización| RANKING| Código| \d{3} SUPERINT| \d{2} Según| Tabla|$)",
        flat,
    )
    def particiones(toks):
        sols = []
        for cortes in itertools.combinations(range(1, len(toks)), 2):
            partes = [toks[a:b] for a, b in zip((0,) + cortes, cortes + (len(toks),))]
            ok = all(len(p[0]) <= 3 and all(len(x) == 3 for x in p[1:]) and (len(p) == 1 or p[0] != "0") for p in partes)
            if ok:
                vals = [int("".join(p)) for p in partes]
                if vals[1] <= vals[0] and max(vals) < 100000:
                    sols.append(vals)
        return sols
    registros = []
    for c, u, g, a, b, resto in filas:
        sols = particiones(resto.split())
        if len(sols) != 1:
            print("AMBIGUO/REVISAR", c, u, resto, sols)
        pi, pac, inn = sols[0]
        registros.append(dict(codigo=c, universidad=u.strip(), tipo_gestion=g, DE=num(a), TPT=num(b), PI=pi, PAC=pac, IN=inn, revisar_manual=len(sols) != 1))
    indic = pd.DataFrame(registros)
    indic["codigo"] = indic.codigo.astype(str)
    indic.to_csv(RAW / "IV_2025_indicadores.csv", index=False)

    pub_txt = flat.split("RANKING DE UNIVERSIDADES PÚBLICAS")[1].split("De los resultados en el ranking de universidades privadas")[0]
    pri_txt = flat.split("RANKING DE UNIVERSIDADES PRIVADAS, 2022")[1]
    pat = re.compile(r"(\d{3}A?) ((?:Universidad|Pontificia|Asociación)[^\d]+?) (\d+,\d) (\d{1,2})(?= |$)")
    rk = []
    for sector, txt in [("Pública", pub_txt), ("Privada", pri_txt)]:
        for c, u, s, p in pat.findall(txt):
            rk.append(dict(codigo_publicado=c, universidad=u.strip(), tipo_gestion=sector,
                           puntaje=num(s), posicion=int(p)))
    rk = pd.DataFrame(rk)
    rk.to_csv(RAW / "IV_2025_ranking.csv", index=False)
    return indic, rk


# ---------------------------------------------------------------------------
# V Informe Bienal (documento de ranking, 2026) + "Análisis por indicador" (.docx)
# ---------------------------------------------------------------------------
def extraer_V():
    t = pdftext(SRC / "V_ranking_universitario_2026.pdf", 1, 4)
    rk = []
    for sector, ini, fin in [("Privada", "RANKING DE UNIVERSIDADES PRIVADAS", "Los puntajes son"),
                             ("Pública", "RANKING DE UNIVERSIDADES PÚBLICAS", "Decenio")]:
        bloque = t.split(ini)[1].split(fin)[0]
        for u, s, p in re.findall(r"^(.+?) (\d+,\d\d) (\d+)$", bloque, re.M):
            rk.append(dict(universidad=u.strip(), tipo_gestion=sector, puntaje=num(s), posicion=int(p)))
    pd.DataFrame(rk).to_csv(RAW / "V_2026_ranking.csv", index=False)

    import docx  # python-docx
    codes = {
        "Proporción de docentes con doctorado": "PDD", "Ratio estudiante - docente": "RED",
        "Tasa de continuidad": "TC", "Impacto normalizado": "PIN",
        "Cantidad de publicaciones indexadas según nivel de citación recibido": "PIC",
        "Proporción de publicaciones de alta calidad": "PAC",
        "Proporción de docentes en el Renacyt": "DR",
        "Proporción de docentes a tiempo completo y/o dedicación exclusiva": "DTC",
        "Tiempo promedio para la obtención del título profesional": "TPT",
        "Tiempo promedio para la obtención del grado de bachiller": "TPB",
    }
    d = docx.Document(SRC / "V_analisis_por_indicador_2026.docx")
    out = []
    for i, tb in enumerate(d.tables, start=1):
        rows = [[c.text.strip() for c in r.cells] for r in tb.rows]
        titulo = re.sub(r"\s+", " ", rows[0][0])
        ind = [v for k, v in codes.items() if k.lower() in titulo.lower()][0]
        for r in rows:
            if len(r) >= 3 and re.match(r"^-?[\d\.,]+$", r[1].replace(" ", "")) and r[2].isdigit():
                out.append(dict(tabla=i, titulo=titulo, indicador=ind,
                                sector_titulo="Pública" if "Públicas" in titulo else "Privada",
                                institucion=re.sub(r"\s+", " ", r[0]),
                                valor=float(r[1].replace(" ", "").replace(",", ".")),
                                posicion=int(r[2])))
    pd.DataFrame(out).to_csv(RAW / "V_analisis_por_indicador_long.csv", index=False)


if __name__ == "__main__":
    extraer_I()
    extraer_II()
    extraer_III()
    extraer_IV()
    extraer_V()
    print("Listo: tablas en", RAW)
