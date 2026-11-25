# ==========================================================================
# Serie armonizada y catálogos
# ==========================================================================

#' Serie histórica de los rankings de SUNEDU (formato largo)
#'
#' Una fila por universidad y ranking, para los siete rankings publicados en
#' los cinco Informes Bienales. Combina la posición y el puntaje publicados con
#' una posición dentro del sector (pública o privada) que permite leer todos
#' los rankings en la misma escala ordinal.
#'
#' @format Un data frame con 503 filas y 16 variables:
#' \describe{
#'   \item{edicion}{Edición del Informe Bienal: `"I"`, `"II"`, `"III"`, `"IV"`, `"V"`}
#'   \item{anio_publicacion}{Año de publicación o aprobación del informe (V: documento del ranking, 2026)}
#'   \item{ranking_id}{Identificador del ranking: `"I_2018_general"`, `"II_2020_wos"`, `"II_2020_scopus"`,
#'     `"III_2021_historico"`, `"III_2021_excelencia"`, `"IV_2025"`, `"V_2026"`. Ver [metodologia_rankings]}
#'   \item{periodo_datos}{Ventana de los datos según la fuente}
#'   \item{ambito_ranking}{`"nacional"` (públicas y privadas en un solo ranking) o `"por_sector"`}
#'   \item{grupo_comparabilidad}{`"A_investigacion_nacional"`, `"B_multidimensional_por_sector"` o
#'     `"X_excelencia_ARWU"`. Ver Details}
#'   \item{id_univ}{Identificador único de la universidad. Ver [universidades]}
#'   \item{codigo_sunedu}{Código SUNEDU de 3 dígitos; `NA` si la universidad no figura en el IV Informe}
#'   \item{gestion}{`"Pública"` o `"Privada"`}
#'   \item{nombre_fuente}{Nombre tal como aparece en la fuente}
#'   \item{posicion_publicada}{Posición publicada (en el IV y el V, dentro del sector)}
#'   \item{puntaje_publicado}{Puntaje publicado, en la escala de cada edición}
#'   \item{con_dato}{`TRUE` si la universidad fue efectivamente ordenada. En el I y el II,
#'     las universidades con puntaje 0 empatan en el último puesto; en el III, `N.A.`
#'     significa que no se hallaron documentos indizados}
#'   \item{posicion_en_sector}{Posición dentro de públicas o privadas: calculada aquí para
#'     los rankings I-III (ordenando el puntaje publicado), publicada en el IV y el V}
#'   \item{n_en_sector}{Universidades ordenadas en ese sector y ranking}
#'   \item{percentil_en_sector}{`1 - (posicion_en_sector - 1) / n_en_sector` (1 = primera)}
#' }
#' @details
#' **Comparabilidad.** Los puntajes no son comparables entre ediciones: cada una
#' los reescala sobre su propio universo. Las posiciones son comparables de forma
#' parcial dentro del grupo A (solo investigación, ranking nacional: I, II y III
#' histórico) y de forma limitada dentro del grupo B (multidimensional, ranking por
#' sector: IV y V). Los grupos A y B no son comparables entre sí, y el Ranking
#' Excelencia 2021 (grupo X) es de otro tipo. Ver
#' `vignette("metodologia", package = "sunedurankings")`.
#' @source SUNEDU, Informes Bienales I-V. Ver [metodologia_rankings].
"rankings"

#' Serie histórica de los rankings de SUNEDU (formato ancho)
#'
#' Posición dentro del sector de cada universidad en cada ranking, en columnas.
#' Mismo contenido que `posicion_en_sector` en [rankings], restringido a las
#' universidades efectivamente ordenadas en al menos un ranking.
#'
#' @format Un data frame con 89 filas y 11 variables:
#' \describe{
#'   \item{id_univ, codigo_sunedu, nombre, gestion}{Ver [universidades]}
#'   \item{I_2018_general,II_2020_wos,II_2020_scopus,III_2021_historico,III_2021_excelencia,IV_2025,V_2026}{Posición
#'     dentro del sector en cada ranking; `NA` si la universidad no fue ordenada}
#' }
#' @source Elaborado a partir de [rankings].
"rankings_ancho"

#' Universidades
#'
#' Identificador único de cada universidad que aparece en al menos un ranking.
#'
#' @format Un data frame con 137 filas y 5 variables:
#' \describe{
#'   \item{id_univ}{Identificador único: el código SUNEDU de 3 dígitos cuando la universidad
#'     figura en el IV Informe; si no, `"X-"` seguido del nombre normalizado}
#'   \item{codigo_sunedu}{Código SUNEDU de 3 dígitos, tomado de las tablas del IV Informe; `NA` en 55 universidades}
#'   \item{nombre}{Nombre más reciente con el que aparece en las fuentes}
#'   \item{gestion}{`"Pública"` o `"Privada"`}
#'   \item{gestion_detalle_2017}{Tipo de gestión en el I Informe: `"Pública"`, `"Asociativa"` o `"Societaria"`}
#' }
#' @details
#' Las universidades sin código SUNEDU son, en su mayoría, universidades que
#' aparecen solo en el I Informe (2018), antes del licenciamiento, o instituciones
#' que no figuran en el IV Informe (por ejemplo, la Facultad de Teología Pontificia
#' y Civil de Lima o la Universidad Nacional Autónoma de Huanta).
#' @source SUNEDU, IV Informe Bienal (códigos) y el resto de ediciones (nombres).
"universidades"

#' Nombres de las universidades en cada fuente
#'
#' Equivalencia entre el nombre con que cada universidad aparece en cada ranking
#' y su identificador único.
#'
#' @format Un data frame con 503 filas y 6 variables:
#' \describe{
#'   \item{ranking_id}{Ranking en que aparece el nombre. Ver [metodologia_rankings]}
#'   \item{nombre_fuente}{Nombre tal como aparece en la fuente}
#'   \item{nombre_normalizado}{Nombre en minúsculas, sin tildes ni sufijos societarios (S.A.C., S.R.L., etc.)}
#'   \item{codigo_sunedu}{Código SUNEDU de 3 dígitos o `NA`}
#'   \item{id_univ}{Identificador único. Ver [universidades]}
#'   \item{gestion}{`"Pública"` o `"Privada"`}
#' }
#' @details
#' La equivalencia se hace por nombre normalizado. Seis variantes históricas se
#' asignan a mano: San Agustín, Hermilio Valdizán, San Luis Gonzaga, César Vallejo,
#' San Ignacio de Loyola y Marcelino Champagnat (ver `data-raw/02_construir_serie.py`).
#' @source Elaborado a partir de las tablas de cada Informe Bienal.
"alias_universidades"

#' Metodología de cada ranking
#'
#' Ficha de cada uno de los siete rankings publicados en los Informes Bienales.
#'
#' @format Un data frame con 7 filas y 20 variables:
#' \describe{
#'   \item{ranking_id}{Identificador del ranking}
#'   \item{edicion}{Edición del Informe Bienal}
#'   \item{anio_publicacion}{Año de publicación o aprobación}
#'   \item{nombre_ranking}{Nombre del ranking en la fuente}
#'   \item{ubicacion_en_fuente}{Capítulo, tabla y páginas de la fuente}
#'   \item{ambito_ranking}{`"nacional"` o `"por_sector"`}
#'   \item{periodo_datos}{Ventana de los datos}
#'   \item{fecha_corte}{Fechas de corte declaradas}
#'   \item{universo_declarado}{Universo evaluado según la fuente}
#'   \item{n_con_puntaje}{Universidades con puntaje}
#'   \item{dimensiones}{Dimensiones o ámbitos y sus pesos}
#'   \item{n_indicadores}{Número de indicadores}
#'   \item{fuente_bibliometrica}{Base bibliográfica usada}
#'   \item{normalizacion_indicadores}{Método de estandarización de los indicadores}
#'   \item{agregacion}{Ponderación de los indicadores}
#'   \item{reescalamiento_final}{Reescalamiento del puntaje final}
#'   \item{ajuste_por_tamano}{Si los indicadores se ajustan por el tamaño de la universidad}
#'   \item{bonificadores}{Bonificadores aplicados, si los hay}
#'   \item{grupo_comparabilidad}{Grupo de comparabilidad (ver [rankings])}
#'   \item{notas}{Anomalías e inconsistencias encontradas en la fuente}
#' }
#' @source SUNEDU, Informes Bienales I-V; páginas en `ubicacion_en_fuente`.
"metodologia_rankings"

#' Indicadores de cada ranking
#'
#' Cada indicador usado en cada ranking, con su peso, fuente, ventana y tipo de medida.
#'
#' @format Un data frame con 40 filas y 10 variables:
#' \describe{
#'   \item{ranking_id}{Identificador del ranking}
#'   \item{ambito}{Ámbito o dimensión del indicador}
#'   \item{sigla}{Sigla del indicador (la de la fuente cuando existe)}
#'   \item{indicador}{Nombre del indicador}
#'   \item{peso_pct}{Peso en el índice (porcentaje), o tasa máxima en el caso de los bonificadores}
#'   \item{fuente}{Fuente de los datos}
#'   \item{ventana}{Periodo de los datos}
#'   \item{tipo_medida}{`"volumen"` (conteo, favorece a las universidades grandes), `"intensidad"`
#'     (proporción o promedio) u otro}
#'   \item{sentido}{`"ascendente"` o `"descendente"`, y cómo entra al índice}
#'   \item{definicion_resumida}{Definición operativa resumida}
#' }
#' @source SUNEDU, Informes Bienales I-V y fichas técnicas del ranking del V Informe.
"metodologia_indicadores"

# ==========================================================================
# Tablas publicadas
# ==========================================================================

#' I Informe Bienal (2018): ranking general de investigación
#'
#' Transcripción del Anexo F del I Informe Bienal: ranking general de producción de
#' investigación y puntajes en cada una de las seis áreas de conocimiento de la OCDE.
#'
#' @format Un data frame con 124 filas y 22 variables:
#' \describe{
#'   \item{posicion}{Posición (las 92 universidades sin producción empatan en el puesto 33)}
#'   \item{universidad}{Nombre en la fuente}
#'   \item{anios_al_2016}{Años de creación al 2016}
#'   \item{sede}{Departamento de la sede principal}
#'   \item{tipo_gestion}{`"Pública"`, `"Asociativa"` o `"Societaria"`}
#'   \item{n_programas_pregrado_2015}{Programas de pregrado al 2015 (`NA` = ND en la fuente)}
#'   \item{autorizacion_licencia}{Licenciada, autorización definitiva o provisional (al 11/11/2017)}
#'   \item{rank_cn,puntaje_cn}{Posición y puntaje en Ciencias Naturales}
#'   \item{rank_it,puntaje_it}{Ingeniería y Tecnología}
#'   \item{rank_mcs,puntaje_mcs}{Medicina y Ciencias de la Salud}
#'   \item{rank_ca,puntaje_ca}{Ciencias Agrícolas}
#'   \item{rank_cs,puntaje_cs}{Ciencias Sociales}
#'   \item{rank_hum,puntaje_hum}{Humanidades}
#'   \item{produccion_cientifica}{Promedio simple de los seis puntajes por área}
#'   \item{puntaje}{Puntaje general: `produccion_cientifica` dividido entre su máximo (0-100)}
#'   \item{id_univ}{Identificador único (añadido). Ver [universidades]}
#' }
#' @details
#' En cada área se promedian cuatro indicadores de Web of Science (artículos 2014-2016,
#' documentos citables 2014-2016, índice H 1996-2016 y artículos en el 10% más citado
#' 2014-2016), cada uno dividido entre el máximo del área. El puntaje general se reproduce
#' exactamente a partir de los seis puntajes por área.
#' @source SUNEDU (2018). *Informe Bienal sobre la Realidad Universitaria Peruana*,
#'   Cuadro 4.40 y Anexo F (pp. 94-95, 128-133); Anexos B y C (pp. 113-115).
#'   <https://cdn.www.gob.pe/uploads/document/file/747830/Informe-Bienal-sobre-realidad.pdf>
"ranking_I_2018"

#' II Informe Bienal (2020): ranking nacional según investigación
#'
#' Transcripción de las Tablas 3.1 (Web of Science, 45 universidades) y 3.2
#' (Scopus, 53 universidades) del II Informe Bienal, con los tres indicadores.
#'
#' @format Un data frame con 98 filas y 8 variables:
#' \describe{
#'   \item{base}{`"Web of Science"` o `"Scopus"`}
#'   \item{posicion}{Posición}
#'   \item{universidad}{Nombre en la fuente}
#'   \item{puntaje}{Puntaje (0-100)}
#'   \item{produccion_per_capita}{(Artículos x 4 + otros documentos) 2016-2018 por docente (SIBE 2017)}
#'   \item{impacto_cientifico_h5}{Índice H5 (documentos 2014-2018, citas al 15/09/2019)}
#'   \item{excelencia_internacional_top10}{Documentos en el 10% más citado a nivel mundial, 2016-2018}
#'   \item{id_univ}{Identificador único (añadido)}
#' }
#' @details
#' Puntaje = min-max (0-100) del promedio simple de los z-scores de los tres indicadores.
#' La versión de Web of Science se reproduce a partir de sus componentes con un error
#' medio de 0,07 puntos y la de Scopus con uno de 0,8 puntos. En la versión de Web of
#' Science, la columna de excelencia (p. ej. 1 174 para la UPCH, frente a 182 en Scopus)
#' parece incompatible con su definición, aunque es la que produce el puntaje publicado.
#' @source SUNEDU (2020). *II Informe Bienal sobre la Realidad Universitaria en el Perú*,
#'   sección 3.3, Tablas 3.1 y 3.2 (pp. 106-111).
#'   <https://www.gob.pe/institucion/sunedu/informes-publicaciones/1093280-ii-informe-bienal-sobre-la-realidad-universitaria-en-el-peru>
"ranking_II_2020"

#' III Informe Bienal (2021): ranking histórico y Ranking Excelencia
#'
#' Transcripción de las Tablas 4.3 (Ranking histórico de instituciones universitarias,
#' 1980-2020) y 4.4 (Ranking Excelencia 2021) del III Informe Bienal.
#'
#' @format Un data frame con 112 filas y 5 variables:
#' \describe{
#'   \item{ranking}{`"Histórico (1980-2020)"` o `"Excelencia 2021 (ARWU)"`}
#'   \item{posicion}{Posición; `NA` en las 35 instituciones sin documentos indizados (`N.A.` en la fuente)}
#'   \item{universidad}{Nombre en la fuente}
#'   \item{puntaje}{Puntaje (0-100); `NA` cuando la fuente indica `N.A.`}
#'   \item{id_univ}{Identificador único (añadido)}
#' }
#' @details
#' El ranking histórico combina producción, índice H y documentos en el 10% más citado
#' de Web of Science entre 1980 y 2020 (31,67% cada uno) con el número de patentes
#' vigentes en Indecopi (5%). El Ranking Excelencia replica los seis indicadores del
#' Academic Ranking of World Universities (ARWU) y no es comparable con los demás.
#' La fuente no publicó los componentes, así que no se pueden reproducir.
#' @source SUNEDU (2021). *III Informe Bienal sobre la Realidad Universitaria en el Perú*,
#'   sección 4.5, Tablas 4.3 y 4.4 (pp. 191-194); Anexo metodológico C (pp. 266-268).
#'   <https://www.gob.pe/institucion/sunedu/informes-publicaciones/2824150-iii-informe-bienal-sobre-la-realidad-universitaria-en-el-peru>
"ranking_III_2021"

#' IV Informe Bienal (2025): ranking universitario por sector
#'
#' Ranking de universidades públicas (39) y privadas (43) del IV Informe Bienal, con
#' los cinco indicadores publicados.
#'
#' @format Un data frame con 82 filas y 11 variables:
#' \describe{
#'   \item{id_univ}{Código SUNEDU de 3 dígitos}
#'   \item{codigo_publicado}{Código tal como aparece en la tabla de ranking (algunos llevan un sufijo `"A"` que la fuente no explica)}
#'   \item{universidad}{Nombre en la tabla de ranking}
#'   \item{tipo_gestion}{`"Pública"` o `"Privada"`}
#'   \item{puntaje}{Índice normalizado (0-100, por sector)}
#'   \item{posicion}{Posición dentro del sector}
#'   \item{DE}{Ratio docente-estudiante, 2021-2022 (rotulado `TA` en la fuente; 15%)}
#'   \item{TPT}{Tiempo promedio de titulación (meses x proporción de bachilleres sin título; 15%)}
#'   \item{PI}{Publicaciones indizadas en Scopus, 2018-2022 (23,33%)}
#'   \item{PAC}{Publicaciones en revistas Q1, 2018-2022 (23,33%)}
#'   \item{IN}{Impacto normalizado x número de publicaciones, 2018-2022 (23,33%)}
#' }
#' @details
#' Índice = suma ponderada de z-scores (formativo 30%, investigación 70%), reescalada
#' a 0-100 dentro de cada sector. Se reproduce a partir de estos indicadores con un
#' error medio de 0,7 puntos (ver [replicas]).
#' @source SUNEDU (2025). *IV Informe Bienal sobre la realidad universitaria en Perú
#'   (2021-2022)*, capítulo "Ranking universitario" (pp. 189-202).
#'   <https://repositorio.minedu.gob.pe/handle/20.500.12799/11743>;
#'   <https://www.gob.pe/institucion/sunedu/informes-publicaciones/7200066-ranking-universitario-del-iv-informe-bienal-2021-2022>
"ranking_IV_2025"

#' V Informe Bienal (2026): ranking universitario por sector
#'
#' Ranking de universidades privadas (45) y públicas (42) del V Informe Bienal, con
#' los diez indicadores publicados en el anexo "Análisis por indicador".
#'
#' @format Un data frame con 87 filas y 15 variables:
#' \describe{
#'   \item{tipo_gestion}{`"Pública"` o `"Privada"`}
#'   \item{universidad}{Nombre en la fuente}
#'   \item{puntaje}{Puntaje (reescalado 1-100 por sector)}
#'   \item{posicion}{Posición dentro del sector}
#'   \item{PDD}{Proporción de docentes con doctorado (12,86%)}
#'   \item{RED}{Ratio estudiante-docente; entra como inversa (12,86%)}
#'   \item{TC}{Tasa de continuidad (12,86%)}
#'   \item{PIN}{Impacto normalizado: FWCI promedio, 2023-2024 (12,86%)}
#'   \item{PIC}{Publicaciones ponderadas por decil de citación (12,86%)}
#'   \item{PAC}{(Q1 x 2 + Q2) / artículos y revisiones (12,86%)}
#'   \item{DR}{Docentes en Renacyt ponderados por nivel / total de docentes (12,86%)}
#'   \item{DTC}{Proporción de docentes a tiempo completo (3,33%)}
#'   \item{TPT}{Meses de bachiller a título; entra como inversa (3,33%)}
#'   \item{TPB}{Meses de egreso a bachiller; entra como inversa (3,33%)}
#'   \item{id_univ}{Identificador único (añadido)}
#' }
#' @details
#' Al índice se le aplican cinco bonificadores (acreditación de programas, patentes,
#' publicaciones citadas en patentes o políticas, gestión ambiental y acreditación
#' institucional) cuyos valores por universidad no se publicaron. Sin ellos, la
#' réplica del ranking alcanza una correlación de Spearman de 0,95 (privadas) y
#' 0,99 (públicas). Tres universidades públicas (Huancavelica, Ucayali y Del Santa)
#' tienen 0 en todos los indicadores que dependen de docentes, al parecer por datos
#' faltantes en el Sistema de Información Universitaria.
#' @source SUNEDU (2026). *Ranking Universitario del V Informe Bienal 2023-2024*:
#'   documento de indicadores y ranking, y anexo "Análisis por indicador".
#'   <https://www.gob.pe/institucion/sunedu/informes-publicaciones/8838541-ranking-universitario-del-v-informe-bienal-2023-2024>
"ranking_V_2026"

#' V Informe Bienal (2026): tablas del anexo "Análisis por indicador"
#'
#' Transcripción literal, en formato largo, de las 21 tablas del anexo "Análisis por
#' indicador" del V Informe Bienal: el valor de cada indicador por universidad.
#'
#' @format Un data frame con 915 filas y 7 variables:
#' \describe{
#'   \item{tabla}{Número de tabla en el documento (1-21)}
#'   \item{titulo}{Título de la tabla}
#'   \item{indicador}{Sigla del indicador}
#'   \item{sector_titulo}{Sector según el título de la tabla}
#'   \item{institucion}{Nombre en la fuente}
#'   \item{valor}{Valor del indicador}
#'   \item{posicion}{Posición en ese indicador}
#' }
#' @details
#' La tabla 3 duplica la tabla 13 (ratio estudiante-docente de las privadas) y la tabla 17
#' (proporción de publicaciones de alta calidad) está rotulada "Universidades Públicas",
#' aunque contiene las 45 privadas. [ranking_V_2026] corrige ambos problemas.
#' @source Ver [ranking_V_2026].
"analisis_indicador_V_2026"

# ==========================================================================
# Réplica y robustez
# ==========================================================================

#' Réplica de los rankings IV y V
#'
#' Puntaje y posición publicados frente a los que se obtienen al aplicar la metodología
#' declarada a los indicadores publicados.
#'
#' @format Un data frame con 169 filas y 8 variables:
#' \describe{
#'   \item{edicion}{`"IV_2025"` o `"V_2026"`}
#'   \item{sector}{`"Pública"` o `"Privada"`}
#'   \item{institucion}{Nombre en la fuente}
#'   \item{puntaje,posicion}{Puntaje y posición publicados}
#'   \item{replica,posicion_replica}{Puntaje y posición replicados}
#'   \item{id_univ}{Identificador único}
#' }
#' @details
#' Los z-scores se calculan sobre públicas y privadas juntas y el índice se reescala
#' dentro de cada sector. La réplica del V no incluye los bonificadores.
#' @source Elaborado con `data-raw/03_replicar_rankings.py`.
"replicas"

#' Contribución de cada indicador al índice (IV y V)
#'
#' Descomposición del índice replicado de cada universidad: z-score de cada indicador
#' multiplicado por su peso.
#'
#' @format Un data frame con 1 280 filas y 6 variables:
#' \describe{
#'   \item{edicion,sector,institucion}{Ver [replicas]}
#'   \item{indicador}{Sigla del indicador}
#'   \item{contribucion}{z-score x peso. La suma por universidad es el índice antes del reescalamiento}
#'   \item{id_univ}{Identificador único}
#' }
#' @source Elaborado con `data-raw/03_replicar_rankings.py`.
"contribuciones"

#' Robustez de las posiciones (IV y V)
#'
#' Intervalo de posiciones de cada universidad al recalcular el índice con
#' especificaciones alternativas razonables, y alertas.
#'
#' @format Un data frame con 169 filas y 17 variables:
#' \describe{
#'   \item{edicion,sector,institucion}{Ver [replicas]}
#'   \item{posicion_publicada,posicion_replica}{Posición publicada y replicada}
#'   \item{posicion_mejor,posicion_peor,posicion_mediana}{Mejor, peor y mediana de las posiciones
#'     bajo todas las especificaciones (ver [robustez_especificaciones])}
#'   \item{amplitud}{`posicion_peor - posicion_mejor`}
#'   \item{n_sector}{Universidades ordenadas en el sector}
#'   \item{indicador_de_mayor_aporte}{Indicador con la mayor contribución al índice}
#'   \item{indice_sin_ese_indicador}{Índice sin la contribución de ese indicador}
#'   \item{indicadores_atipicos}{Indicadores con |z| > 3}
#'   \item{alerta_dependencia}{`TRUE` si el indicador de mayor aporte (contribución > 0,30) convierte
#'     un índice que sin él estaría bajo el promedio en uno alto}
#'   \item{alerta_inestable}{`TRUE` si la amplitud supera un cuarto del sector}
#'   \item{alerta_datos}{`TRUE` si los indicadores que dependen de docentes valen 0, o la tasa
#'     de continuidad vale 0 (probable dato faltante; solo en el V)}
#'   \item{id_univ}{Identificador único}
#' }
#' @source Elaborado con `data-raw/04_robustez.py`. Ver
#'   `vignette("robustez_y_progreso", package = "sunedurankings")`.
"robustez"

#' Posición bajo cada especificación alternativa (IV y V)
#'
#' @format Un data frame con 2 463 filas y 6 variables:
#' \describe{
#'   \item{edicion,sector,institucion}{Ver [replicas]}
#'   \item{especificacion}{`"oficial (réplica)"`, `"z acotado a ±3"`, `"winsorización p5-p95"`,
#'     `"normalización por percentiles"`, `"normalización min-max"`, `"ámbitos con igual peso"`,
#'     `"todos los indicadores con igual peso"` o `"sin <indicador>"` (quitar un indicador a la vez)}
#'   \item{posicion}{Posición dentro del sector bajo esa especificación}
#'   \item{id_univ}{Identificador único}
#' }
#' @source Elaborado con `data-raw/04_robustez.py`.
"robustez_especificaciones"

#' Valores atípicos en los indicadores (IV y V)
#'
#' Indicadores con un z-score mayor que 3 en valor absoluto.
#'
#' @format Un data frame con 19 filas y 9 variables:
#' \describe{
#'   \item{edicion,sector,institucion}{Ver [replicas]}
#'   \item{indicador}{Sigla del indicador}
#'   \item{valor}{Valor publicado}
#'   \item{z}{z-score (calculado sobre el indicador ya transformado según su sentido)}
#'   \item{media,mediana}{Media y mediana del indicador en el conjunto evaluado}
#'   \item{id_univ}{Identificador único}
#' }
#' @details
#' Un valor atípico no es necesariamente un error: los z-scores altos de las
#' universidades con más producción científica reflejan su liderazgo real. Ver
#' [robustez] para las alertas que sí afectan la posición.
#' @source Elaborado con `data-raw/04_robustez.py`.
"alertas_atipicos"

# ==========================================================================
# Progreso
# ==========================================================================

#' Concordancia entre rankings
#'
#' Correlación de Spearman entre las posiciones dentro del sector de cada par de
#' rankings, sobre las universidades ordenadas en ambos.
#'
#' @format Un data frame con 30 filas y 6 variables:
#' \describe{
#'   \item{sector}{`"Pública"` o `"Privada"`}
#'   \item{ranking_a,ranking_b}{Par de rankings}
#'   \item{n_comun}{Universidades ordenadas en ambos}
#'   \item{spearman}{Correlación de Spearman}
#'   \item{coincidencia_top10}{Universidades que están en el top 10 de ambos (dentro de las comunes)}
#' }
#' @source Elaborado con `data-raw/05_progreso.py`.
"concordancia"

#' Universidades ordenadas en cada ranking
#'
#' @format Un data frame con 14 filas y 3 variables:
#' \describe{
#'   \item{ranking_id}{Identificador del ranking}
#'   \item{gestion}{`"Pública"` o `"Privada"`}
#'   \item{n_ordenadas}{Universidades con puntaje en ese ranking y sector}
#' }
#' @source Elaborado con `data-raw/05_progreso.py`.
"universo"

#' Estratos en los rankings de investigación (grupo A)
#'
#' Posición dentro del sector y estrato de cada universidad en los rankings I (2018),
#' II-Web of Science (2020) y III histórico (2021).
#'
#' @format Un data frame con 89 filas y 10 variables:
#' \describe{
#'   \item{id_univ,nombre,gestion}{Ver [universidades]}
#'   \item{I_2018_general,II_2020_wos,III_2021_historico}{Posición dentro del sector}
#'   \item{estrato_I_2018_general,estrato_II_2020_wos,estrato_III_2021_historico}{`"1-5"`, `"6-10"`,
#'     `"11-20"`, `">20"` o `"sin producción / no listada"`}
#'   \item{patron_grupo_A}{`"siempre en el top 5"`, `"siempre en el top 10"`, `"entra a la lista
#'     (sin producción indexada en 2014-16)"`, `"estable fuera del top 10"`, `"rango amplio"` o
#'     `"cobertura incompleta"`}
#' }
#' @source Elaborado con `data-raw/05_progreso.py`.
"estratos_grupo_A"

#' Cambio de posición entre el IV y el V Informe
#'
#' Posición publicada e intervalo de posiciones (ver [robustez]) en el IV y el V, y si
#' el cambio resiste la ponderación.
#'
#' @format Un data frame con 87 filas y 13 variables:
#' \describe{
#'   \item{id_univ,nombre,sector}{Ver [universidades]}
#'   \item{posicion_publicada_IV,posicion_mejor_IV,posicion_peor_IV,posicion_mediana_IV}{Posiciones en el IV}
#'   \item{posicion_publicada_V,posicion_mejor_V,posicion_peor_V,posicion_mediana_V}{Posiciones en el V}
#'   \item{cambio_publicado}{`posicion_publicada_IV - posicion_publicada_V` (positivo = sube)}
#'   \item{clasificacion}{`"sube (robusto a la ponderación)"` si la peor posición del V es mejor que
#'     la mejor del IV; `"baja (robusto a la ponderación)"` en el caso inverso; si no, `"no concluyente"`;
#'     `"solo en V"` o `"solo en IV"`}
#' }
#' @details
#' Un cambio robusto a la ponderación no equivale a progreso: entre el IV y el V
#' cambiaron los propios indicadores, la fuente bibliométrica y la ventana de datos.
#' @source Elaborado con `data-raw/05_progreso.py`.
"cambio_IV_V"
