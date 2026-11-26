# sunedu_rankings (paquete de R sunedurankings): Rankings universitarios de los Informes Bienales de SUNEDU, 2018-2026

Serie histórica de los rankings universitarios publicados por la Superintendencia Nacional de Educación Superior Universitaria (SUNEDU) en sus cinco Informes Bienales sobre la realidad universitaria en el Perú. Incluye la transcripción de cada tabla publicada, la metodología de cada edición (indicadores, pesos, fuentes, ventanas y universo), un identificador único por universidad, la réplica de los puntajes a partir de los indicadores publicados y análisis de comparabilidad y robustez.

![Concordancia entre los rankings de SUNEDU](man/figures/concordancia_rankings.png)

## Instalación

Este paquete no está en CRAN. Puedes instalarlo con `devtools`:

```r
devtools::install_github("AlejandroPerezPortocarrero/sunedu_rankings")
```
Puedes pegar este texto en el README, justo debajo de la figura:

### Nota

Si prefieres usar archivos CSV, están en [`inst/extdata/`](inst/extdata/).

## Motivación

La Ley Universitaria (Ley 30220, art. 15.15) obliga a SUNEDU a publicar cada dos años un informe sobre la realidad universitaria que incluya un ranking "respecto al número de publicaciones indexadas, entre otros indicadores". Hasta hoy hubo cinco ediciones. Sus rankings suelen leerse como una serie, del tipo "la universidad X subió del puesto 9 al 4", pero **cada edición usó una metodología distinta**: cambiaron la base bibliográfica, la ventana de datos, los indicadores, la forma de estandarizarlos, el universo evaluado y, desde 2025, la estructura misma del ranking, que pasó a separar públicas y privadas.

El paquete busca que esos rankings puedan usarse con el cuidado que requieren. Para eso:

- **Documenta cómo se construyó cada ranking**, con la página de la fuente (`metodologia_rankings`, `metodologia_indicadores`).
- **Armoniza la serie**: un identificador único por universidad (`id_univ`, el código SUNEDU cuando existe), la posición publicada y una posición dentro del sector comparable en escala (`rankings`, `rankings_ancho`).
- **Valida la transcripción reproduciendo los puntajes** publicados a partir de los indicadores publicados (`replicas`, `contribuciones`).
- **Distingue el progreso real de los cambios de metodología**:
  - concordancia entre rankings (`concordancia`);
  - robustez de cada posición ante especificaciones alternativas razonables (`robustez`, `robustez_especificaciones`);
  - qué cambios entre ediciones resisten esos ajustes (`estratos_grupo_A`, `cambio_IV_V`).

## Las cinco ediciones

| Edición | Publicación | Datos | Qué mide | Fuente bibliométrica | Ranking | Universidades ordenadas | Grupo |
|---|---|---|---|---|---|---|---|
| I | 2018 | 2014–2016 | Investigación: 4 indicadores × 6 áreas OCDE | Web of Science | Nacional | 32 | A |
| II | 2020 | 2016–2018 | Investigación: producción por docente, índice H5, top 10% | WoS y Scopus | Nacional | 45 (WoS) / 53 (Scopus) | A |
| III | 2021 | 1980–2020 | Investigación acumulada + patentes | Web of Science | Nacional | 58 | A |
| III (bis) | 2021 | varios | Réplica de ARWU ("Ranking Excelencia 2021") | WoS / Clarivate | Nacional | 19 | X |
| IV | 2025 | 2018–2022 | Formativo (30%) + investigación (70%), 5 indicadores | Scopus (SCImago) | Por sector | 39 públicas + 43 privadas | B |
| V | 2026 | 2023–2024 | Formativo + investigación + capacidad institucional, 10 indicadores + 5 bonificadores | Scopus (SciVal) | Por sector | 42 públicas + 45 privadas | B |

**Grupos de comparabilidad**: A = solo investigación, ranking nacional; B = multidimensional, ranking separado por sector; X = no comparable con los demás. Los puntajes no son comparables entre ediciones. Las posiciones son comparables de forma parcial dentro del grupo A y de forma limitada dentro del grupo B. Los grupos A y B no son comparables entre sí. Detalle en `vignette("metodologia", package = "sunedurankings")`.

## Qué se puede afirmar sobre el progreso

- **El grupo A es consistente; el grupo B no.** Los rankings de investigación (I–III) concuerdan mucho entre sí: la correlación de Spearman va de 0,79 a 0,96. Las dos ediciones multidimensionales, en cambio, concuerdan poco: 0,75 en privadas y 0,50 en públicas.
- **Los primeros puestos son robustos; el resto no.** Al recalcular el IV y el V con especificaciones alternativas razonables (acotar valores extremos, otra normalización, otros pesos, quitar un indicador a la vez), las primeras posiciones casi no cambian (con una excepción en el V, ver el último punto). La posición típica, en cambio, varía unos 10 puestos.
- **Hay un núcleo estable de universidades líderes en investigación**, en el top 5 de su sector en todos los rankings del grupo A:
  - privadas: Cayetano Heredia, Católica del Perú y Científica del Sur;
  - públicas: San Marcos, Agraria La Molina, Ingeniería y San Antonio Abad del Cusco.
- **Entre el IV y el V, tres de cada cuatro cambios de posición no resisten un cambio de ponderación.** Los que sí lo resisten mezclan desempeño con un cambio de indicadores, así que con lo publicado no es posible medir el progreso de la mayoría de universidades.
- **Algunas posiciones del V dependen de un solo indicador o de datos aparentemente faltantes** (`robustez$alerta_dependencia`, `robustez$alerta_datos`). El caso más notorio es el 2.º puesto de la Universidad de San Martín de Porres entre las privadas, sostenido por un impacto normalizado atípico.

Detalle en `vignette("robustez_y_progreso", package = "sunedurankings")`.

![Robustez de las posiciones en el V Informe](man/figures/robustez_V_2026.png)

## Cobertura y limitaciones conocidas

- **Rankings**: los siete rankings generales de los cinco Informes Bienales. No se incluyen los seis rankings por área del I Informe (Anexos G–L), aunque los puntajes por área están en `ranking_I_2018`.
- **V Informe**: se usan el documento del ranking (fichas técnicas y resultados) y el anexo "Análisis por indicador". Corresponden a la versión de los documentos descargada el 24/11/2026; si SUNEDU publica una versión corregida, los puntajes podrían cambiar.
- **Réplica**:
  - I, II-WoS y IV se reproducen exactamente o casi (error medio ≤ 0,7 puntos).
  - II-Scopus se reproduce de forma aproximada (0,8 puntos).
  - El V se reproduce sin bonificadores, cuyos valores por universidad no se publicaron (Spearman 0,95 en privadas y 0,99 en públicas).
  - El III no publicó sus componentes y no puede reproducirse.
- **Identificadores**: 55 de las 137 universidades no tienen código SUNEDU. Son universidades que no figuran en el IV Informe, en su mayoría presentes solo en el I Informe, antes del licenciamiento.
- **Posición dentro del sector**: en el I, II y III es una posición calculada aquí, ordenando el puntaje publicado dentro de públicas o privadas; SUNEDU no la publicó.
- **Anomalías de las fuentes**: se documentan en `metodologia_rankings$notas` y no se corrigen. Por ejemplo, la columna de excelencia del II-WoS, los sufijos "A" sin explicación en los códigos del IV, y las tablas duplicadas o mal rotuladas y los datos faltantes del V.

## Estructura de los datos

### Serie histórica (`rankings`)

Una fila por universidad y ranking.

| Campo | Descripción |
|---|---|
| `edicion` | I, II, III, IV, V |
| `anio_publicacion` | Año de publicación o aprobación del informe |
| `ranking_id` | `I_2018_general`, `II_2020_wos`, `II_2020_scopus`, `III_2021_historico`, `III_2021_excelencia`, `IV_2025`, `V_2026` |
| `periodo_datos` | Ventana de los datos según la fuente |
| `ambito_ranking` | `nacional` o `por_sector` |
| `grupo_comparabilidad` | `A_investigacion_nacional`, `B_multidimensional_por_sector`, `X_excelencia_ARWU` |
| `id_univ` | Identificador único (ver `universidades`) |
| `codigo_sunedu` | Código SUNEDU de 3 dígitos (`NA` si no existe) |
| `gestion` | Pública / Privada |
| `nombre_fuente` | Nombre tal como aparece en la fuente |
| `posicion_publicada`, `puntaje_publicado` | Posición y puntaje publicados (el puntaje **no** es comparable entre ediciones) |
| `con_dato` | `TRUE` si la universidad fue efectivamente ordenada |
| `posicion_en_sector`, `n_en_sector`, `percentil_en_sector` | Posición dentro de públicas o privadas, número de universidades ordenadas y percentil |

`rankings_ancho` tiene las mismas posiciones dentro del sector con un ranking por columna.

### Universidades (`universidades`, `alias_universidades`)

| Campo | Descripción |
|---|---|
| `id_univ` | Código SUNEDU de 3 dígitos, o `X-<nombre-normalizado>` si la universidad no figura en el IV Informe |
| `codigo_sunedu` | Código SUNEDU (de las tablas del IV Informe) |
| `nombre` | Nombre más reciente en las fuentes |
| `gestion` | Pública / Privada |
| `gestion_detalle_2017` | Pública / Asociativa / Societaria (I Informe) |

`alias_universidades` vincula cada nombre de cada fuente (`ranking_id`, `nombre_fuente`) con su `id_univ`.

### Metodología (`metodologia_rankings`, `metodologia_indicadores`)

`metodologia_rankings` tiene una ficha por ranking: ubicación en la fuente, periodo y fechas de corte, universo declarado, dimensiones, número de indicadores, fuente bibliométrica, normalización, agregación, reescalamiento, ajuste por tamaño, bonificadores, grupo de comparabilidad y anomalías. `metodologia_indicadores` tiene una fila por indicador: ámbito, sigla, peso, fuente, ventana, tipo de medida (volumen o intensidad), sentido y definición.

### Tablas publicadas

| Dataset | Contenido | Fuente |
|---|---|---|
| `ranking_I_2018` | Ranking general y puntajes en las 6 áreas OCDE (124 universidades) | I Informe, Anexo F |
| `ranking_II_2020` | Rankings WoS y Scopus con sus 3 indicadores | II Informe, Tablas 3.1 y 3.2 |
| `ranking_III_2021` | Ranking histórico (1980–2020) y Ranking Excelencia 2021 | III Informe, Tablas 4.3 y 4.4 |
| `ranking_IV_2025` | Ranking por sector con sus 5 indicadores | IV Informe, capítulo "Ranking universitario" |
| `ranking_V_2026` | Ranking por sector con sus 10 indicadores | V Informe: documento del ranking y "Análisis por indicador" |
| `analisis_indicador_V_2026` | Las 21 tablas del anexo "Análisis por indicador", literales | V Informe |

### Réplica, robustez y progreso

| Dataset | Contenido |
|---|---|
| `replicas` | Puntaje y posición publicados frente a los replicados (IV y V) |
| `contribuciones` | Contribución de cada indicador al índice de cada universidad (z-score × peso) |
| `robustez` | Intervalo de posiciones bajo especificaciones alternativas, indicador de mayor aporte y alertas |
| `robustez_especificaciones` | Posición de cada universidad bajo cada especificación |
| `alertas_atipicos` | Indicadores con \|z\| > 3 |
| `concordancia` | Correlación de Spearman y coincidencia del top 10 entre cada par de rankings |
| `universo` | Universidades ordenadas por ranking y sector |
| `estratos_grupo_A` | Estrato (top 5, 6–10, 11–20, >20) y patrón de cada universidad en los rankings I–III |
| `cambio_IV_V` | Cambio de posición entre el IV y el V, y si resiste la ponderación |

Cada dataset está documentado en R: por ejemplo, `?rankings` o `?robustez`.

## Reconstruir los datos

Los documentos fuente están en [`data-raw/fuentes/`](data-raw/fuentes/) (ver [Fuentes](#fuentes)). Para reconstruir los datos, ejecuta desde la raíz del repositorio:

```bash
pip install -r data-raw/requirements.txt          # además: poppler-utils (pdftotext)
python data-raw/01_extraer_rankings.py           # transcribe las tablas de data-raw/fuentes/ a data-raw/tablas/
python data-raw/02_construir_serie.py             # serie armonizada e identificadores
python data-raw/03_replicar_rankings.py           # réplica de los puntajes (validación)
python data-raw/04_robustez.py                    # especificaciones alternativas y alertas
python data-raw/05_progreso.py                    # concordancia, estratos y cambios IV -> V
python data-raw/06_figuras.py
```

```r
source("data-raw/make_datasets.R")   # data/*.rda e inst/extdata/*.csv
devtools::document()
```

## Fuentes

- **SUNEDU (2018).** *Informe Bienal sobre la Realidad Universitaria Peruana*. Lima: Superintendencia Nacional de Educación Superior Universitaria. <https://cdn.www.gob.pe/uploads/document/file/747830/Informe-Bienal-sobre-realidad.pdf>; también en <https://repositorio.minedu.gob.pe/handle/20.500.12799/5716>
- **SUNEDU (2020).** *II Informe Bienal sobre la Realidad Universitaria en el Perú*. Lima: SUNEDU. ISBN 978-612-47125-1-7. <https://www.gob.pe/institucion/sunedu/informes-publicaciones/1093280-ii-informe-bienal-sobre-la-realidad-universitaria-en-el-peru>; también en <https://repositorio.minedu.gob.pe/handle/20.500.12799/6911>
- **SUNEDU (2021).** *III Informe Bienal sobre la Realidad Universitaria en el Perú*. Lima: SUNEDU. Aprobado por Acuerdo de Consejo Directivo n.° 05-056-2021 (17/12/2021). <https://www.gob.pe/institucion/sunedu/informes-publicaciones/2824150-iii-informe-bienal-sobre-la-realidad-universitaria-en-el-peru>; también en <https://repositorio.minedu.gob.pe/handle/20.500.12799/7913>
- **SUNEDU (2025).** *IV Informe Bienal sobre la realidad universitaria en Perú (2021-2022)*. Lima: SUNEDU. Aprobado por Acuerdo de Consejo Directivo n.° 001-037-2025 (16/09/2025). <https://repositorio.minedu.gob.pe/handle/20.500.12799/11743>; ranking en <https://www.gob.pe/institucion/sunedu/informes-publicaciones/7200066-ranking-universitario-del-iv-informe-bienal-2021-2022>
- **SUNEDU (2026).** *Ranking Universitario del V Informe Bienal 2023-2024*: documento de indicadores y ranking, y anexo "Análisis por indicador". Lima: SUNEDU. <https://www.gob.pe/institucion/sunedu/informes-publicaciones/8838541-ranking-universitario-del-v-informe-bienal-2023-2024>
- Colección de los Informes Bienales en la plataforma del Estado peruano: <https://www.gob.pe/institucion/sunedu/colecciones/5716-informes-bienales>

## Versiones y cita

Cada versión del paquete es una versión fija de los datos; los cambios se registran en [`NEWS.md`](NEWS.md). Las correcciones (una transcripción, un identificador, la actualización de una edición) entran en una versión nueva, de modo que los resultados siempre pueden rastrearse a la versión usada. Para instalar una versión específica:

```r
devtools::install_github("AlejandroPerezPortocarrero/sunedu_rankings@v1.0.0")
packageVersion("sunedurankings")
```

Cita la versión que usaste: `citation("sunedurankings")` da la referencia, y el botón "Cite this repository" de GitHub usa `CITATION.cff`.

## Licencia

MIT
