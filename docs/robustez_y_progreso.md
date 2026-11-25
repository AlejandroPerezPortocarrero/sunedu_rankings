# Robustez de los rankings y lo que dicen (y no dicen) sobre el progreso

Un ranking resume muchas dimensiones en una sola posición. Si cambia la posición de una universidad entre dos ediciones, hay tres explicaciones posibles: (a) cambió su desempeño, (b) cambió la metodología, o (c) cambió el conjunto de universidades evaluadas. Este documento trata de separar esas tres fuentes con lo que SUNEDU publicó. Los cálculos están en `scripts/04_robustez.py` y `scripts/05_progreso.py`.

## 1. El universo evaluado cambia en cada edición

Universidades efectivamente ordenadas (con puntaje), por sector:

| Ranking | Privadas | Públicas |
|---|---|---|
| I 2018 | 19 | 13 |
| II 2020 WoS | 28 | 17 |
| II 2020 Scopus | 28 | 25 |
| III 2021 histórico | 33 | 25 |
| IV 2025 | 43 | 39 |
| V 2026 | 45 | 42 |

Entre el I y el III el universo crece porque más universidades empiezan a publicar en revistas indexadas. Desde el IV se ordenan todas las licenciadas con datos completos. Ser 10.ª de 19 no es lo mismo que ser 10.ª de 45. Por eso la serie incluye `percentil_en_sector`, aunque el percentil tampoco corrige el problema de fondo: cambia quién está en la lista.

## 2. ¿Cuánto coinciden los rankings entre sí?

Correlación de Spearman de las posiciones dentro del sector, calculada sobre las universidades presentes en ambos rankings (`data/processed/concordancia_rankings.csv`; figura `output/concordancia_rankings.png`):

- **Dentro del grupo A (I, II y III; solo investigación)** la concordancia es alta: entre 0,88 y 0,96 en privadas y entre 0,79 y 0,95 en públicas. Aunque cambiaron los indicadores, los tres miden esencialmente lo mismo: la producción científica indexada.
- **Entre el grupo A y el grupo B** baja a 0,48–0,83.
- **Entre el IV y el V**, las dos ediciones multidimensionales, es de solo **0,75 en privadas y 0,50 en públicas**. Dos ediciones consecutivas del mismo tipo de ranking concuerdan menos que rankings de investigación separados por tres años.

## 3. ¿Cuánto depende cada posición de las decisiones metodológicas?

Para el IV y el V se recalculó el índice con 17 especificaciones alternativas en el V y 12 en el IV. Todas usan los mismos indicadores publicados y solo cambian decisiones que cualquier evaluador podría tomar de otra forma:

- acotar los z-scores a ±3;
- winsorizar los indicadores en los percentiles 5 y 95;
- normalizar por percentiles o por min-max en lugar de z-score;
- dar el mismo peso a cada ámbito o a cada indicador;
- quitar un indicador a la vez.

Las réplicas oficiales reproducen bien los rankings publicados (Spearman ≥ 0,95), así que el ejercicio es informativo. Resultados (`data/processed/robustez_resumen.csv`; figuras `output/robustez_V_2026.png` y `output/robustez_IV_2025.png`):

- **Los primeros puestos son estables**: las tres primeras posiciones de cada sector y edición casi no se mueven. Las excepciones son el 2.º puesto de las privadas en el V, que puede variar 14 puestos (ver §5), y en menor medida el 2.º de las públicas, que varía 6.
- **El resto del ranking es frágil**: la mediana del intervalo de posiciones es de 8 a 10 puestos, y entre el 36% y el 56% de las universidades se mueven 10 puestos o más según la especificación. Diferencias de pocos puestos en la zona media **no son informativas**.

## 4. ¿Hubo progreso?

### Grupo A (2018–2021): un núcleo estable

En los tres rankings de investigación, estas universidades estuvieron **siempre en el top 5 de su sector**:

- **Privadas**: Cayetano Heredia, Católica del Perú y Científica del Sur.
- **Públicas**: San Marcos, Agraria La Molina, Ingeniería y San Antonio Abad del Cusco.

Siempre estuvieron en el top 10:

- **Privadas**: UPC, San Martín de Porres, Piura y Pacífico.
- **Públicas**: Amazonía Peruana, San Agustín, Trujillo y Altiplano.

Lo que más cambió en este periodo es la **entrada** de nuevas universidades: 28 universidades sin producción indexada en 2014–2016 aparecen en el ranking histórico de 2021. Esto es coherente con el aumento de publicaciones tras el licenciamiento que documenta el propio III Informe. Pero no permite comparar posiciones, porque el I mide 3 años y el III, 41.

### Grupo B (IV → V): pocos cambios robustos

Se considera que un cambio de posición entre el IV y el V **resiste la ponderación** solo si el intervalo de posiciones del V no se superpone con el del IV (`data/processed/grupoB_cambio_IV_V.csv`):

| | Privadas | Públicas |
|---|---|---|
| Sube (robusto a la ponderación) | 6 | 6 |
| Baja (robusto a la ponderación) | 6 | 8 |
| No concluyente | 31 | 25 |
| Solo en el V | 2 | 3 |

- **Tres de cada cuatro cambios no son concluyentes.** De los 27 cambios publicados de 10 o más puestos, 8 desaparecen al variar la ponderación.
- Incluso un cambio "robusto" **no equivale a progreso**. Entre el IV y el V cambiaron los indicadores mismos: de volumen a proporciones, del ratio docente-estudiante a una batería formativa, de SCImago a SciVal y de 2018–2022 a 2023–2024. La clasificación solo indica que el cambio no depende de la ponderación elegida dentro de cada edición.
- **El único indicador aproximadamente comparable** entre el IV y el V es la relación entre estudiantes y docentes (ratio docente-estudiante en el IV, su inversa en el V). Aun así difieren el periodo y el redondeo (el IV publica dos decimales).

**Conclusión**: con lo publicado, los rankings de SUNEDU permiten identificar un **núcleo de universidades líderes que es estable** con cualquier metodología. **No permiten medir el progreso** de la mayoría de universidades entre ediciones. Para hacerlo haría falta que SUNEDU publique series de indicadores con definiciones constantes, aunque el índice compuesto cambie.

## 5. Casos que requieren atención

El análisis marca dos tipos de alerta, con criterios iguales para todas las universidades:

**a) Dependencia de un solo indicador**: el indicador de mayor aporte (z × peso > 0,30) convierte un índice que, sin él, estaría bajo el promedio en uno alto.

| Edición | Universidad | Posición publicada | Intervalo | Indicador |
|---|---|---|---|---|
| V | **Universidad de San Martín de Porres** (privada) | **2** | 2–16 | Impacto normalizado (PIN = 6,25; z = 7,7) |
| V | Universidad César Vallejo (privada) | 7 | 2–19 | Publicaciones ponderadas (PIC) |
| V | Universidad Privada del Norte (privada) | 17 | 16–43 | Publicaciones ponderadas (PIC) |
| V | Facultad de Teología Pontificia y Civil de Lima (privada) | 29 | 4–44 | Ratio estudiante-docente (z = 6,2) |
| V | U. N. Intercultural de la Amazonía (pública) | 24 | 18–36 | Docentes con doctorado |
| IV | Universidad Antonio Ruiz de Montoya (privada) | 21 | 10–40 | Ratio docente-estudiante |
| IV | Universidad Autónoma de Ica (privada) | 18 | 13–32 | Tiempo de titulación |
| IV | U. Privada de Huancayo Franklin Roosevelt (privada) | 30 | 20–43 | Tiempo de titulación |

El caso más llamativo es el de la **USMP en el V**: es el 2.º puesto de las privadas y descansa casi por completo en el impacto normalizado. Es el valor más alto de las 87 universidades evaluadas: el promedio es 0,70 y la mediana 0,55. La contribución de ese indicador a su índice es +0,99, y la suma de todos los demás es −0,07. Sin él, su posición en la réplica pasa del 3.º al 16.º puesto. Dos elementos sugieren que se trata de un **artefacto de la definición**:

- En el IV, la misma universidad tenía un impacto medio implícito de 1,06 (máximo del sistema: 1,41), cuando el indicador se ponderaba por volumen.
- La ficha técnica del V reconoce que el promedio "puede sobredimensionar a universidades con baja producción científica, pero con altos niveles de impacto normalizado".

Una explicación plausible, que **no se puede verificar con los datos publicados**, es que unos pocos artículos de grandes consorcios internacionales muy citados dominen el promedio en una ventana de citas corta. La UPCH (3,36) y la USIL (2,03) también tienen valores altos en este indicador, pero su posición no depende de él. Verificarlo exige la distribución del FWCI por documento, que SUNEDU no publica.

**b) Datos faltantes.** Tres universidades públicas (Huancavelica, Ucayali y Del Santa) tienen 0 en los cuatro indicadores que dependen del número de docentes, y la Autónoma de Chota tiene una tasa de continuidad de 0. Lo más probable es que falte información en el SIU y no que sea desempeño, pero el ranking las ordena en los últimos puestos sin advertirlo.

**c) Valores extremos que no son alertas.** Los z-scores altos de la UPCH, la PUCP, San Marcos o La Molina en indicadores de volumen reflejan su liderazgo real en producción científica y son consistentes con todas las ediciones. El tiempo de titulación de la César Vallejo (5,6 meses frente a una mediana de 21) y el de bachillerato de la UPC (2,1 frente a 10,2) sí son atípicos y merecerían revisión, aunque no determinan su posición. La lista completa está en `data/processed/alertas_valores_atipicos.csv`.
