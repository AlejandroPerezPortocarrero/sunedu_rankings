# Diccionario: `data/processed/serie_rankings_long.csv`

| Variable | Descripción |
|---|---|
| `edicion` | I, II, III, IV, V |
| `anio_publicacion` | Año de publicación o aprobación del informe (V: 2026, documento del ranking) |
| `ranking_id` | `I_2018_general`, `II_2020_wos`, `II_2020_scopus`, `III_2021_historico`, `III_2021_excelencia`, `IV_2025`, `V_2026` |
| `periodo_datos` | Ventana de los datos según la fuente |
| `ambito_ranking` | `nacional` (públicas y privadas juntas) o `por_sector` |
| `grupo_comparabilidad` | `A_investigacion_nacional`, `B_multidimensional_por_sector`, `X_excelencia_ARWU` |
| `id_univ` | Identificador único (código SUNEDU o `X-...`) |
| `codigo_sunedu` | Código de 3 dígitos (IV Informe); vacío si no existe |
| `gestion` | Pública / Privada |
| `nombre_fuente` | Nombre tal como aparece en la fuente |
| `posicion_publicada` | Posición publicada (en IV y V, dentro del sector) |
| `puntaje_publicado` | Puntaje publicado (escala propia de cada edición; **no comparable entre ediciones**) |
| `con_dato` | `True` si la universidad fue efectivamente ordenada (en I y II, puntaje > 0; en III excluye N.A.) |
| `posicion_en_sector` | Posición dentro de públicas o privadas (calculada para I–III, publicada para IV–V) |
| `n_en_sector` | Universidades ordenadas en ese sector y ranking |
| `percentil_en_sector` | 1 − (posición − 1) / n (1 = primera) |

`universidades.csv` incluye además `gestion_detalle_2017` (Pública / Asociativa / Societaria), tomada del I Informe.
