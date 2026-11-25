# Ficha del conjunto de datos

> Los campos marcados **[por completar]** se llenan con la salida real del notebook 01 o los verifica el equipo.
> No escribir cifras que no hayamos obtenido nosotros.

| Campo | Valor | Cómo se verificó |
|---|---|---|
| Nombre | Cassava (iCassava 2019) | Catálogo de TensorFlow Datasets |
| Página del catálogo | https://www.tensorflow.org/datasets/catalog/cassava | Documento del profesor |
| Archivo descargado | https://storage.googleapis.com/emcassavadata/cassavaleafdata.zip | Código fuente de TFDS (`cassava.py`) |
| Versión | 0.1.0 (versión del constructor en TFDS) | Código fuente de TFDS |
| Origen | Competencia iCassava 2019 (página: https://www.kaggle.com/c/cassava-disease/overview) | Código fuente de TFDS |
| Referencia | Mwebaze et al. (2019), *iCassava 2019 Fine-Grained Visual Categorization Challenge*, arXiv:1908.02900 | Código fuente de TFDS |
| Licencia | No se encontró una licencia explícita en el artículo ni en la página del desafío. Los datos se publicaron para la competencia iCassava 2019 en Kaggle; se usan solo con fines académicos y se cita el artículo. Queda como punto a verificar en las reglas de la competencia | Búsqueda 2026-11-15 |
| Procedencia de las fotos | Uganda. Fotos tomadas durante un censo regular, en su mayoría por los propios agricultores en sus cultivos, y etiquetadas por expertos del National Crops Resources Research Institute (NaCRRI) con el laboratorio de IA de la Universidad Makerere (Kampala). Cada hoja se etiquetó solo con la enfermedad más significativa | Página del desafío iCassava 2019 (FGVC6) y artículo arXiv:1908.02900 |
| Imágenes etiquetadas | 9.430 publicadas · encontradas: 9.430 | notebook 01 (2026-11-15) |
| Particiones | train 5.656 · validación 1.889 · prueba 1.885 publicadas · encontradas: iguales | notebook 01 (2026-11-15) |
| Clases | 5: `cbb`, `cbsd`, `cgm`, `cmd`, `healthy` | Código fuente de TFDS |
| Distribución por clase | cmd 4.431 (47,0 %) · cbsd 2.406 (25,5 %) · cgm 1.289 (13,7 %) · cbb 777 (8,2 %) · healthy 527 (5,6 %); misma proporción en las tres particiones | notebook 01 |
| Resolución | Variable. Ancho 420–1.622 px (mediana 543), alto 347–1.240 px (mediana 500); las más comunes 500×500, 666×500 y 500×666 | notebook 02 |
| Archivos ilegibles | Ninguno | notebook 01 |
| Duplicados | 68 archivos en 26 grupos idénticos; en 18 grupos la misma foto tiene etiquetas distintas (sobre todo cbb, cbsd y cgm); 17 grupos cruzan particiones. Además, 29 pares casi idénticos, 20 entre particiones | notebook 02 |
| Criterios de exclusión | Ver protocolo D11: se retiran 68 imágenes de entrenamiento/validación; la prueba no se toca | notebook 02 |
| Identificadores de planta/finca | **[por completar]** – revisar si el dataset los trae; si no, declararlo como limitación | |

## Significado de las clases

| Sigla | Nombre |
|---|---|
| cbb | Tizón bacteriano de la yuca (Cassava Bacterial Blight) |
| cbsd | Enfermedad del estriado marrón (Cassava Brown Streak Disease) |
| cgm | Ácaro verde de la yuca (Cassava Green Mite) |
| cmd | Enfermedad del mosaico (Cassava Mosaic Disease) |
| healthy | Hoja sana |

Las etiquetas son categorías de referencia para un ejercicio académico, no una validación agronómica.

## Hallazgo del control de duplicados
Hay fotos idénticas byte a byte guardadas con etiquetas distintas (por ejemplo, el mismo archivo como `cbb`, `cbsd` y `cgm`).
Esto indica errores de etiquetado en el conjunto publicado. En la prueba quedan unas 10 fotos así, que no se retiran
para conservar la partición publicada; se declara como limitación.

## Nota sobre las cantidades
El artículo original informa 9.436 imágenes etiquetadas; la versión de TensorFlow Datasets que descargamos tiene 9.430.
La diferencia (6 imágenes) viene de la versión publicada, no de nuestra descarga.

## Formato, resolución y peso (revisión del día 7, 2026-11-21)
- **Formato:** las 9.430 imágenes son JPG. **Color:** las 9.430 están en RGB.
- **Resolución:** 669 tamaños distintos; los más comunes son 500×666 (2.369), 888×500 (1.328), 625×500 (1.073), 666×500 (1.070) y 500×500 (719). Ninguna mide menos de 224 px en algún lado, así que al llevarlas a 224×224 nunca se agrandan.
- **Megapíxeles por clase (mediana):** 0,31–0,33 en todas las clases.
- **Peso del archivo por clase (mediana):** cbb 96 KB · cbsd 134 KB · cgm 120 KB · cmd 163 KB · healthy 61 KB. Con la misma resolución, las fotos sanas pesan menos de la mitad que las de cmd. Puede deberse a que las hojas con síntomas tienen más detalle y comprimen peor, o a diferencias en cómo se tomaron o guardaron las fotos de cada clase; queda como posible atajo a vigilar.

## Comparación con otras fuentes de imágenes de yuca (revisión del día 7, 2026-11-24)
El profesor pidió verificar que no se trate del mismo dataset. Se revisaron las cuatro fuentes indicadas:

| Fuente | Imágenes | Clases | Origen | ¿Se usó? |
|---|---|---|---|---|
| TensorFlow Datasets – cassava (iCassava 2019) | 9.430 (5.656 / 1.889 / 1.885) | 5: cbb, cbsd, cgm, cmd, healthy | Uganda, Makerere AI Lab y NaCRRI | **Sí** |
| Kaggle 2020 – Cassava Leaf Disease Classification | 21.367 | 5 (las mismas) | Uganda, mismo laboratorio | No (otra competencia) |
| Mendeley Data 2021 (Divyanth et al.) | No indicado | 3: sana, CBB, mosaico | India (Tamil Nadu), IIT Kharagpur | No |
| Harvard Dataverse 2022 (Tusubira et al.) | ≈9.100 | 3: healthy, cbsd, cmd (detección con cajas) | Uganda, Makerere | No |

**Conclusión:** el proyecto usa solo el conjunto de TensorFlow Datasets (iCassava 2019). Mendeley es de otro país y otras clases. Kaggle 2020 y Harvard Dataverse son del mismo laboratorio y podrían compartir algunas fotos con el nuestro; eso no se comprobó porque exige descargarlos y compararlos archivo por archivo. Dentro de nuestro conjunto sí se comprobó que ninguna foto idéntica o casi idéntica quede a la vez en entrenamiento y prueba.
