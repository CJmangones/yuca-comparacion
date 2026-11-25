# Análisis de errores reales

> Lo redacta el equipo mirando las galerías del notebook 05. Mínimo 8 errores.
> Criterio de selección usado: los errores de mayor confianza en el conjunto de prueba.

| # | Modelo | Archivo | Real | Predicha | Confianza | Qué se ve en la foto | Hipótesis del error (equipo) |
|---|---|---|---|---|---|---|---|
| 1 | E1 | test/cbsd/test-cbsd-311.jpg | cbsd | cbb | 0,99 | Hojas muy amarillas con puntos oscuros pequeños | Síntomas parecidos: en etapa avanzada cbsd y cbb producen amarillamiento y manchas similares |
| 2 | E1 | test/cgm/test-cgm-136.jpg | cgm | cbb | 0,99 | Hoja amarilla y marrón, marchita. Tiene una copia idéntica etiquetada como cbb y cbsd | Hoja muy dañada: la necrosis avanzada borra el moteado típico del ácaro |
| 3 | E1 | test/cbsd/test-cbsd-88.jpg | cbsd | cbb | 0,98 | Hoja amarilla caída con manchas oscuras | Síntomas parecidos (como #1) |
| 4 | E1 | test/cgm/test-cgm-102.jpg | cgm | cbb | 0,97 | Hoja amarilla y marrón con necrosis. Tiene una copia idéntica etiquetada como cbb y cbsd | Hoja muy dañada (como #2) |
| 5 | E1 | test/cbsd/test-cbsd-215.jpg | cbsd | cbb | 0,97 | Hoja amarilla verdosa con lesiones marrones | Síntomas parecidos (como #1) |
| 6 | E1 | test/cbsd/test-cbsd-331.jpg | cbsd | cbb | 0,96 | Hojas amarillas con puntos oscuros pequeños | Síntomas parecidos (como #1) |
| 7 | E1 | test/cgm/test-cgm-87.jpg | cgm | cmd | 0,93 | Varias hojas con moteado claro y blanquecino | La foto muestra muchas hojas y el síntoma no está en una sola hoja centrada; además cmd es la clase mayoritaria (47 %) y ante la duda el modelo tiende a elegirla |
| 8 | E1 | test/cmd/test-cmd-294.jpg | cmd | cgm | 0,93 | Hojas angostas con moteado fino | Moteado parecido entre mosaico leve y ácaro; la lesión es pequeña y sin deformación marcada, así que el modelo no la reconoce como cmd |

Criterio de selección: los 8 errores de E1 con mayor confianza en el conjunto de prueba (`resultados/E1/errores_inspeccionados.csv`, `resultados/E1/galeria_errores.png`).

## Patrones que observamos
**E1 (2026-11-15).** La confusión más frecuente es cbsd → cbb (92 de 481 fotos de cbsd). En los 8 errores de mayor confianza,
6 fueron predichos como cbb y casi todos son hojas muy amarillas o marchitas con puntos oscuros. Dos de ellos
(`test-cgm-136`, `test-cgm-102`) son fotos de prueba cuya copia idéntica tenía otra etiqueta.

Hipótesis del equipo (Camilo Ayazo):
- **Síntomas parecidos:** en etapas avanzadas, cbb y cbsd producen amarillamiento y necrosis similares.
- **Posible atajo visual:** el modelo pudo aprender que "hoja amarilla y seca" significa cbb, sin mirar el tipo de lesión.
- **Etiquetas dudosas:** hay fotos idénticas etiquetadas como cbb, cbsd y cgm; esa confusión de etiquetas pasa al modelo.

**E1 frente a E3 (2026-11-18).** En las 1.885 fotos de prueba: ambos aciertan 1.229, ambos fallan 289, solo E1 acierta 168 y solo E3 acierta 199.
Lectura del equipo: los modelos se complementan; fallan en fotos distintas en 367 casos, así que cada arquitectura ve cosas diferentes.

Los 8 errores de mayor confianza de E3 siguen el mismo patrón que E1: 5 son predicciones de cbb (sobre fotos de cbsd y cgm), y aparecen de nuevo `test-cgm-102` y `test-cgm-136`, las fotos de prueba con etiqueta contradicha por una copia idéntica.

## Grad-CAM (4 imágenes de E1)
- Dos aciertos de cmd (100 % de confianza): el calor está sobre la hoja deformada y moteada, en la zona con síntomas.
- cbsd predicha como cbb (99 %): calor en la parte baja de las hojas amarillas.
- cgm predicha como cbb (99 %): calor sobre la zona marrón y necrosada.

Lectura del equipo: el modelo mira la hoja y no el suelo, así que no usa el fondo como atajo; pero en los errores parece guiarse por el color amarillo o marrón más que por la forma de la lesión.
El Grad-CAM indica dónde se concentró el modelo; no demuestra causalidad ni que haya reconocido la enfermedad.

## Posibles atajos visuales
