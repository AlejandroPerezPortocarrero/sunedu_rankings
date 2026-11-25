# sunedurankings 1.0.0

Primera versión estable (25/11/2026).

## Datasets

* `rankings`, `rankings_ancho`: serie histórica de los siete rankings de los
  cinco Informes Bienales (2018-2026), con posición y puntaje publicados y
  posición dentro del sector.
* `universidades`, `alias_universidades`: identificador único por universidad
  (código SUNEDU cuando existe) y equivalencia con los nombres de cada fuente.
* `metodologia_rankings`, `metodologia_indicadores`: ficha de cada ranking y
  de cada indicador.
* Tablas publicadas: `ranking_I_2018`, `ranking_II_2020`, `ranking_III_2021`,
  `ranking_IV_2025`, `ranking_V_2026`, `analisis_indicador_V_2026`.
* Réplica y robustez: `replicas`, `contribuciones`, `robustez`,
  `robustez_especificaciones`, `alertas_atipicos`.
* Progreso: `concordancia`, `universo`, `estratos_grupo_A`, `cambio_IV_V`.

## Comprobaciones de la construcción

* El puntaje general del I Informe se reproduce exactamente desde los seis
  puntajes por área; las 32 universidades del Anexo F coinciden con el
  Cuadro 4.40 (verificado a mano).
* El II (Web of Science) y el IV se reproducen a partir de los indicadores
  publicados con un error medio de 0,07 y 0,7 puntos; el II (Scopus), con
  uno de 0,8 puntos.
* El V se reproduce sin bonificadores con una correlación de Spearman de 0,95
  (privadas) y 0,99 (públicas).
* Las posiciones de todas las tablas son secuenciales y los puntajes,
  monótonos.

## Limitaciones conocidas

* Los bonificadores del V no se publicaron por universidad; su réplica es
  aproximada.
* El III no publicó los componentes de sus rankings.
* 55 universidades no tienen código SUNEDU.
* Las anomalías de las fuentes se documentan en `metodologia_rankings$notas`,
  no se corrigen.
