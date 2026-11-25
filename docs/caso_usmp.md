# El 2.º puesto de la Universidad de San Martín de Porres en el V Informe

## Resumen

El segundo lugar de la USMP entre las privadas del V Informe se explica **casi por completo por un solo indicador**: el impacto normalizado (PIN), definido como el FWCI promedio de sus publicaciones en Scopus de 2023–2024. La USMP tiene un PIN de **6,25**, es decir, sus publicaciones se citan en promedio 6,25 veces más que el promedio mundial de su campo. Es el valor más alto de las 87 universidades evaluadas, a **7,7 desviaciones estándar** de la media (0,70; mediana 0,55). En los demás indicadores la USMP está en torno al promedio o por debajo.

## Evidencia

**1. Descomposición del puntaje.** Al reproducir el índice del V sin bonificadores (`scripts/03_replicar_y_sensibilidad.py`; Spearman = 0,95 con el ranking publicado de privadas), la contribución de cada indicador (z × peso) para la USMP es:

| Indicador | Contribución |
|---|---|
| PIN (impacto normalizado) | **+0,987** |
| PIC (publicaciones ponderadas por citas) | +0,047 |
| RED (ratio estudiante-docente) | +0,027 |
| PAC (Q1–Q2) | +0,014 |
| TPT | +0,009 |
| TC | −0,002 |
| TPB | −0,014 |
| DTC | −0,030 |
| PDD (doctores) | −0,050 |
| DR (Renacyt) | −0,072 |
| **Total** | **+0,915** |
| **Total sin PIN** | **−0,072** |

Sin el PIN, el índice de la USMP queda por debajo del promedio del sistema.

**2. Sensibilidad** (posición entre privadas en la réplica; publicada: 2.ª; réplica base: 3.ª):

| Escenario | Posición USMP |
|---|---|
| Réplica base (sin bonificadores) | 3 |
| Sin el indicador PIN | 16 |
| PIN con tope de 3,0 | 3 |
| PIN con tope de 2,0 | 6 |
| PIN de la USMP = mediana de las privadas | 18 |
| PIN de la USMP = 1,0 (promedio mundial) | 15 |
| PIN ponderado por volumen (aproximación a la regla del IV) | 5 |

**3. Comparación con ediciones anteriores.** Entre las privadas, la USMP ocupó el puesto 7 (I), 7 (II-WoS), 8 (II-Scopus), 5 (III histórico) y 6 (IV). El salto al 2.º puesto coincide con el cambio de definición del impacto normalizado:

- En el **IV**, el indicador era "impacto normalizado × n.º de publicaciones". El cociente implícito IN/PI da el impacto medio por documento: USMP **1,06**, UPCH 1,34, PUCP 0,99. **El máximo entre las 82 universidades del IV era 1,41.**
- En el **V**, el indicador es el FWCI **promedio**, sin ponderar: USMP **6,25**, UPCH 3,36, PUCP 0,89.

El IV (SCImago, 2018–2022) y el V (SciVal, 2023–2024) usan fuentes y ventanas distintas, así que estos valores no son estrictamente comparables. Aun así, un salto de ~1 a 6,25 en el impacto medio de una universidad con unas 2 800 publicaciones ponderadas (PIC; la 10.ª entre las privadas) es extraordinario.

**4. La propia SUNEDU advierte el sesgo.** La ficha técnica del PIN dice: *"Puede sobredimensionar a universidades con baja producción científica, pero con altos niveles de impacto normalizado"*. La propuesta de mejora fue añadir un indicador de volumen (PIC). Pero el PIC tiene el mismo peso (12,86%) y no compensa un z-score de 7,7 en el PIN.

## Hipótesis (no verificable con los datos publicados)

El FWCI promedio es muy sensible a la cola derecha de la distribución de citas. Con una ventana corta (publicaciones de 2023–2024 con citas hasta fines de 2025), unos pocos artículos muy citados pueden dominar el promedio. Es el caso típico de los artículos de grandes consorcios internacionales con cientos de coautores, como los de carga global de enfermedad. El documento indica además que las autocitas no se tratan y que, con varias afiliaciones, una publicación cuenta para cada universidad. Para verificarlo habría que pedir a SUNEDU, o extraer de SciVal:

1. la distribución del FWCI por documento de la USMP (y de la UPCH y la USIL, que también tienen valores altos: 3,36 y 2,03);
2. el FWCI excluyendo el 1% de documentos más citados, o la mediana;
3. el número de documentos con más de 100 autores;
4. el puntaje con y sin el penalizador de revistas excluidas de Scopus, que el V descartó.

## Conclusión

El ranking no es "erróneo" en el sentido aritmético: aplica la regla que declara. Pero el resultado de la USMP es un **artefacto de diseño** (un promedio no robusto, con el mismo peso que los demás indicadores y estandarizado con z-score sin acotar) más que una señal de calidad institucional. Además, **no es comparable** con su posición en el IV, porque la definición del indicador decisivo cambió.
