# make_datasets.R
# Construye los datasets del paquete (data/*.rda) y sus copias en CSV (inst/extdata/*.csv)
# a partir de las tablas intermedias que generan los scripts de Python en data-raw/tablas/.
#
# Orden completo de reconstrucción (desde la raíz del paquete):
#   python data-raw/01_extraer_rankings.py <carpeta_con_fuentes>
#   python data-raw/02_construir_serie.py
#   python data-raw/03_replicar_rankings.py
#   python data-raw/04_robustez.py
#   python data-raw/05_progreso.py
#   python data-raw/06_figuras.py
#   source("data-raw/make_datasets.R")
#   devtools::document()

tab <- function(f, ...) {
  utils::read.csv(file.path("data-raw", "tablas", f), fileEncoding = "UTF-8", encoding = "UTF-8",
                  stringsAsFactors = FALSE, check.names = FALSE, ...)
}
cc <- c(codigo_sunedu = "character", id_univ = "character", codigo = "character",
        codigo_publicado = "character")
tabc <- function(f) {
  h <- names(tab(f, nrows = 1))
  tab(f, colClasses = cc[names(cc) %in% h])
}

alias_universidades <- tabc("alias_universidades.csv")
id_de <- function(ranking, nombres) {
  a <- alias_universidades[alias_universidades$ranking_id == ranking, ]
  a$id_univ[match(nombres, a$nombre_fuente)]
}
sin_na <- function(x) { stopifnot(!anyNA(x)); x }

# ---------------------------------------------------------------- serie y catálogos
rankings <- tabc("serie_rankings_long.csv")
rankings_ancho <- tabc("serie_rankings_wide_posicion_en_sector.csv")
universidades <- tabc("universidades.csv")
metodologia_rankings <- tab("rankings_metodologia.csv")
metodologia_indicadores <- tab("indicadores_metodologia.csv")

# ---------------------------------------------------------------- tablas publicadas
ranking_I_2018 <- tab("I_2018_ranking_general.csv")
ranking_I_2018$id_univ <- sin_na(id_de("I_2018_general", ranking_I_2018$universidad))

w <- tab("II_2020_ranking_wos.csv");  w$base <- "Web of Science"
s <- tab("II_2020_ranking_scopus.csv"); s$base <- "Scopus"
w$id_univ <- id_de("II_2020_wos", w$universidad)
s$id_univ <- id_de("II_2020_scopus", s$universidad)
ranking_II_2020 <- rbind(w, s)[, c("base", setdiff(names(w), "base"))]
stopifnot(!anyNA(ranking_II_2020$id_univ))

h <- tab("III_2021_ranking_historico.csv");  h$ranking <- "Histórico (1980-2020)"
e <- tab("III_2021_ranking_excelencia.csv"); e$ranking <- "Excelencia 2021 (ARWU)"
h$id_univ <- id_de("III_2021_historico", h$universidad)
e$id_univ <- id_de("III_2021_excelencia", e$universidad)
ranking_III_2021 <- rbind(h, e)[, c("ranking", "posicion", "universidad", "puntaje", "id_univ")]
stopifnot(!anyNA(ranking_III_2021$id_univ))

ind4 <- tabc("IV_2025_indicadores.csv")
rk4 <- tabc("IV_2025_ranking.csv")
rk4$codigo <- substr(rk4$codigo_publicado, 1, 3)
ranking_IV_2025 <- merge(
  rk4[, c("codigo", "codigo_publicado", "universidad", "tipo_gestion", "puntaje", "posicion")],
  ind4[, c("codigo", "DE", "TPT", "PI", "PAC", "IN")], by = "codigo")
names(ranking_IV_2025)[names(ranking_IV_2025) == "codigo"] <- "id_univ"
ranking_IV_2025 <- ranking_IV_2025[order(ranking_IV_2025$tipo_gestion, ranking_IV_2025$posicion), ]
stopifnot(nrow(ranking_IV_2025) == 82)

v <- tab("V_2026_indicadores_y_replica.csv")
ranking_V_2026 <- v[, c("sector", "institucion", "puntaje", "posicion",
                        "PDD", "RED", "TC", "PIN", "PIC", "PAC", "DR", "DTC", "TPT", "TPB")]
names(ranking_V_2026)[1:2] <- c("tipo_gestion", "universidad")
ranking_V_2026$id_univ <- sin_na(id_de("V_2026", ranking_V_2026$universidad))
ranking_V_2026 <- ranking_V_2026[order(ranking_V_2026$tipo_gestion, ranking_V_2026$posicion), ]

analisis_indicador_V_2026 <- tab("V_analisis_por_indicador_long.csv")

# ---------------------------------------------------------------- réplica y robustez
# identificador para las tablas de análisis (IV: nombre de la tabla de indicadores -> código)
id_analisis <- function(edicion, institucion) {
  ifelse(edicion == "IV_2025",
         ind4$codigo[match(institucion, ind4$universidad)],
         id_de("V_2026", institucion))
}

r4 <- tabc("IV_2025_indicadores_y_replica.csv"); r4$edicion <- "IV_2025"
r5 <- tab("V_2026_indicadores_y_replica.csv");   r5$edicion <- "V_2026"
cols <- c("edicion", "sector", "institucion", "puntaje", "posicion", "replica", "posicion_replica")
replicas <- rbind(r4[, cols], r5[, cols])
replicas$id_univ <- sin_na(id_analisis(replicas$edicion, replicas$institucion))

largo <- function(d, edicion) {
  ind <- setdiff(names(d), c("sector", "institucion", "indice"))
  data.frame(edicion = edicion,
             sector = rep(d$sector, length(ind)),
             institucion = rep(d$institucion, length(ind)),
             indicador = rep(ind, each = nrow(d)),
             contribucion = unlist(d[ind], use.names = FALSE))
}
contribuciones <- rbind(largo(tab("IV_2025_contribuciones_por_indicador.csv"), "IV_2025"),
                        largo(tab("V_2026_contribuciones_por_indicador.csv"), "V_2026"))
contribuciones$id_univ <- sin_na(id_analisis(contribuciones$edicion, contribuciones$institucion))

robustez <- tab("robustez_resumen.csv")
robustez$id_univ <- sin_na(id_analisis(robustez$edicion, robustez$institucion))

rp <- tab("robustez_posiciones.csv")
esp <- setdiff(names(rp), c("edicion", "sector", "institucion", "posicion_publicada"))
robustez_especificaciones <- data.frame(
  edicion = rep(rp$edicion, length(esp)), sector = rep(rp$sector, length(esp)),
  institucion = rep(rp$institucion, length(esp)),
  especificacion = rep(esp, each = nrow(rp)),
  posicion = unlist(rp[esp], use.names = FALSE))
robustez_especificaciones <- robustez_especificaciones[!is.na(robustez_especificaciones$posicion), ]
robustez_especificaciones$id_univ <- sin_na(id_analisis(robustez_especificaciones$edicion,
                                                        robustez_especificaciones$institucion))

alertas_atipicos <- tab("alertas_valores_atipicos.csv")
alertas_atipicos$id_univ <- sin_na(id_analisis(alertas_atipicos$edicion, alertas_atipicos$institucion))

# ---------------------------------------------------------------- progreso
concordancia <- tab("concordancia_rankings.csv")
u <- tab("universo_por_ranking.csv")
universo <- data.frame(ranking_id = rep(u$ranking_id, 2),
                       gestion = rep(c("Privada", "Pública"), each = nrow(u)),
                       n_ordenadas = c(u$Privada, u[["Pública"]]))
estratos_grupo_A <- tabc("grupoA_estratos.csv")
cambio_IV_V <- tabc("grupoB_cambio_IV_V.csv")

# ---------------------------------------------------------------- guardar
datasets <- c("rankings", "rankings_ancho", "universidades", "alias_universidades",
              "metodologia_rankings", "metodologia_indicadores",
              "ranking_I_2018", "ranking_II_2020", "ranking_III_2021", "ranking_IV_2025",
              "ranking_V_2026", "analisis_indicador_V_2026",
              "replicas", "contribuciones", "robustez", "robustez_especificaciones",
              "alertas_atipicos", "concordancia", "universo", "estratos_grupo_A", "cambio_IV_V")
dir.create("data", showWarnings = FALSE)
dir.create(file.path("inst", "extdata"), recursive = TRUE, showWarnings = FALSE)
for (d in datasets) {
  x <- get(d)
  rownames(x) <- NULL
  assign(d, x)
  save(list = d, file = file.path("data", paste0(d, ".rda")), compress = "xz")
  utils::write.csv(x, file.path("inst", "extdata", paste0(d, ".csv")), row.names = FALSE,
                   fileEncoding = "UTF-8", na = "")
}
message("Guardados ", length(datasets), " datasets en data/ e inst/extdata/")
