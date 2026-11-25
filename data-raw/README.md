# data-raw: reconstrucción de los datos

Los scripts de esta carpeta transcriben las tablas publicadas por SUNEDU y construyen todos los datasets del paquete. Se ejecutan en este orden, desde la raíz del repositorio:

| Paso | Script | Qué hace | Salida |
|---|---|---|---|
| 1 | `01_extraer_rankings.py <carpeta>` | Transcribe las tablas de ranking de los PDF y del DOCX | `tablas/I_2018_*.csv` … `tablas/V_*.csv` |
| 2 | `02_construir_serie.py` | Identificadores únicos, equivalencia de nombres y serie armonizada | `tablas/universidades.csv`, `alias_universidades.csv`, `serie_rankings_*.csv` |
| 3 | `03_replicar_rankings.py` | Reproduce los puntajes del I, II, IV y V a partir de sus componentes | `tablas/*_indicadores_y_replica.csv`, `*_contribuciones_por_indicador.csv`, `validacion/replicacion.txt` |
| 4 | `04_robustez.py` | Recalcula el IV y el V con especificaciones alternativas; alertas | `tablas/robustez_*.csv`, `alertas_valores_atipicos.csv` |
| 5 | `05_progreso.py` | Concordancia entre rankings, estratos del grupo A, cambios IV → V | `tablas/concordancia_rankings.csv`, `grupoA_estratos.csv`, `grupoB_cambio_IV_V.csv`, `universo_por_ranking.csv` |
| 6 | `06_figuras.py` | Figuras del README y de las viñetas | `../man/figures/`, `../vignettes/figures/` |
| 7 | `make_datasets.R` | Construye los datasets del paquete | `../data/*.rda`, `../inst/extdata/*.csv` |

`indices.py` define los índices del IV y el V (pesos, transformaciones de sentido y especificaciones alternativas). `rankings_metodologia.csv` e `indicadores_metodologia.csv` son las fichas metodológicas, **editadas a mano** a partir de las fuentes; el paso 2 las copia a `tablas/`.

Requisitos: Python 3 con `pandas`, `numpy`, `python-docx` y `matplotlib` (`requirements.txt`), `pdftotext` (poppler-utils) y R con `devtools`.

## Documentos fuente

Guarda los documentos en una carpeta (por ejemplo `fuentes/`, excluida del repositorio) con estos nombres:

| Archivo esperado | Documento | Páginas usadas (PDF) | Tablas |
|---|---|---|---|
| `I_informe_bienal_2018.pdf` | Informe Bienal sobre la Realidad Universitaria Peruana (134 pp. en pliegos dobles) | 46–48, 57–58, 65–67 | Cuadro 4.40; Anexos B, C y F |
| `II_informe_bienal_2020.pdf` | II Informe Bienal sobre la Realidad Universitaria en el Perú | 107–112 | Tablas 3.1 y 3.2 |
| `III_informe_bienal_2021.pdf` | III Informe Bienal sobre la Realidad Universitaria en el Perú | 206–210, 282–284 | Tablas 4.3 y 4.4; Anexo metodológico C |
| `IV_informe_bienal_2025.pdf` | IV Informe Bienal sobre la realidad universitaria en Perú (2021-2022) | 189–202 | Indicadores y ranking por sector |
| `V_ranking_universitario_2026.pdf` | Ranking Universitario del V Informe Bienal 2023-2024 (27 pp.) | 1–27 | Ámbitos, indicadores, fichas técnicas y ranking |
| `V_analisis_por_indicador_2026.docx` | Análisis por indicador (V Informe), 21 tablas | — | Valor de cada indicador por universidad |

Los enlaces de descarga están en la sección "Fuentes" del README principal.

## Validación

`validacion/replicacion.txt` registra el error de la réplica de cada ranking; `validacion/robustez_log.txt` y `validacion/progreso_log.txt`, las salidas de los pasos 4 y 5. El paso 3 verifica además que las posiciones de todas las tablas sean secuenciales y los puntajes monótonos. La coincidencia de las 32 universidades del Anexo F del I Informe con el Cuadro 4.40 se verificó a mano.
