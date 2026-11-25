# Bitácora grupal

Proyecto: Comparación experimental de modelos preentrenados para reconocer enfermedades de la yuca.
Formato: **problema encontrado → alternativas → decisión → prueba → resultado → revisión de la decisión.**

> Las razones de cada decisión las dio el integrante que la tomó. "Revisión de la decisión" se llena días después, cuando ya se sabe si fue acertada.

---

## 2026-11-14 · Entorno de trabajo y estructura del proyecto
- **Quién:** Camilo Ayazo.
- **Problema encontrado:** el equipo no tenía definido dónde ejecutar los experimentos ni cómo organizar el código, y no tiene experiencia con terminales ni con instalación de bibliotecas.
- **Alternativas consideradas:** (a) Google Colab + Google Drive + GitHub por la página web; (b) instalación local con Visual Studio Code y terminal.
- **Decisión:** opción (a). Motivos: nuestros computadores no tienen GPU y Colab ofrece una gratuita; no tenemos experiencia instalando bibliotecas ni usando la terminal y Colab ya trae todo listo; y los tres podemos abrir y ejecutar lo mismo desde cualquier computador.
- **Prueba realizada:** se creó la estructura del proyecto (`src/`, `notebooks/`, `configs/`, `docs/`, `bitacora/`, `resultados/`).
- **Resultado:** proyecto listo para subir al repositorio.
- **Revisión de la decisión:** pendiente (se revisa después de ejecutar los experimentos).

## 2026-11-14 · Creación del repositorio y primera subida
- **Quién:** Camilo Ayazo.
- **Problema encontrado:** al subir el proyecto a GitHub por la página web, en la lista solo aparecieron los cuatro archivos sueltos (`.gitignore`, `ESTADO.md`, `README.md`, `requirements.txt`); las carpetas no se habían agregado.
- **Alternativas consideradas:** (a) repetir la carga arrastrando también las carpetas desde el Explorador de archivos; (b) usar el enlace "choose your files" de la página, que solo permite elegir archivos sueltos.
- **Decisión:** opción (a), porque es la única que conserva la estructura de carpetas, y hacerlo con la cuenta propia para aprender el procedimiento, que se repetirá en cada avance.
- **Prueba realizada:** se seleccionó todo el contenido de la carpeta y se arrastró a la página de carga de GitHub.
- **Resultado:** repositorio `CamiloAyazo/yuca-comparacion` con dos commits: "Initial commit" (14-nov, 11:40 p. m.) y "Estructura inicial del proyecto" (15-nov, 12:00 a. m.). Quedaron 36 archivos. No se subieron la carpeta `resultados` (estaba vacía y GitHub no sube carpetas vacías) ni `.gitignore`.
- **Revisión de la decisión:** pendiente (se revisa después de ejecutar los experimentos).

## 2026-11-15 · Error al ejecutar el notebook 01 en Colab
- **Quién:** Camilo Ayazo.
- **Problema encontrado:** la primera celda del notebook 01 falló con `ModuleNotFoundError: No module named 'src'`, aunque los permisos de Google Drive se habían aceptado.
- **Alternativas consideradas:** (a) que faltara algún permiso de Drive; (b) que la carpeta no estuviera en "Mi unidad"; (c) que hubiera una carpeta dentro de otra.
- **Decisión:** diagnosticar antes de cambiar nada, listando el contenido de la carpeta desde una celda de Colab.
- **Prueba realizada:** `os.listdir('/content/drive/MyDrive/yuca-comparacion')` mostró que adentro solo había otra carpeta `yuca-comparacion` con el proyecto. Era el caso (c).
- **Resultado:** se movió el contenido un nivel hacia arriba con una celda (`shutil.move`) y se eliminó la carpeta interna vacía. El proyecto quedó en `/content/drive/MyDrive/yuca-comparacion`.
- **Revisión de la decisión:** fue acertado diagnosticar antes de cambiar algo. Aprendimos dos cosas: (1) después de descomprimir un archivo hay que revisar la estructura de carpetas antes de subirla, porque puede quedar una carpeta dentro de otra; (2) las rutas importan: el código busca los archivos en una ubicación exacta y, si la carpeta queda en otro nivel, deja de funcionar aunque los archivos estén completos.

## 2026-11-15 · Fuente de datos, descarga e inventario
- **Quién:** Camilo Ayazo.
- **Problema encontrado:** había que elegir la fuente de datos entre las tres propuestas por el profesor y comprobar que la descarga funcionara.
- **Alternativas consideradas:** (a) TensorFlow Datasets – Cassava (9.430 imágenes, particiones publicadas); (b) Kaggle 2020 (≈21.397 imágenes, requiere partición propia); (c) Mendeley (India, 3 clases).
- **Decisión:** opción (a). Motivo: tamaño manejable. Con 15 días de plazo y la GPU gratuita de Colab, 9.430 imágenes se pueden entrenar varias veces en poco tiempo; Kaggle 2020 tiene más del doble.
- **Prueba realizada:** notebook `01_descarga_inventario.ipynb` en Google Colab. Descarga del archivo `cassavaleafdata.zip` desde la fuente que usa TensorFlow Datasets.
- **Resultado:**
  - Descarga completa: 1.354 MB en 46 segundos.
  - 9.430 imágenes inventariadas, sin avisos de archivos ilegibles.
  - Particiones encontradas: entrenamiento 5.656, validación 1.889, prueba 1.885. Coinciden con las publicadas.
  - Distribución total: cmd 4.431 (47,0 %), cbsd 2.406 (25,5 %), cgm 1.289 (13,7 %), cbb 777 (8,2 %), healthy 527 (5,6 %). La proporción es la misma en las tres particiones.
  - Las resoluciones no son uniformes (por ejemplo 666×500, 500×500 y 500×666).
- **Revisión de la decisión:** pendiente (se revisa después de ejecutar los experimentos).

## 2026-11-15 · EDA y control de duplicados (notebook 02)
- **Quién:** Camilo Ayazo.
- **Problema encontrado:** el control de duplicados mostró 26 grupos de archivos idénticos (68 archivos). En 18 de esos grupos la misma foto tiene etiquetas distintas, por ejemplo el mismo archivo guardado como `cbb`, `cbsd` y `cgm`. Además aparecieron 29 pares de fotos casi idénticas, 20 de ellos en particiones distintas; revisamos los 6 que dibuja el notebook y son la misma foto. La regla inicial de exclusión conservaba una copia con una de sus etiquetas, elegida por orden alfabético.
- **Alternativas consideradas:** (1) para los casi duplicados: retirarlos o dejarlos y declararlo como limitación; (2) para las fotos con etiquetas contradictorias: retirar todas sus copias de entrenamiento y validación, o mantener la regla inicial; (3) para la prueba: no tocarla, o retirar las fotos dudosas en todos los experimentos.
- **Decisión:** retirar los casi duplicados entre particiones, para reducir la fuga de información; retirar todas las copias de las fotos con etiquetas contradictorias, para que el modelo no aprenda de una etiqueta dudosa; y no tocar la prueba, declarando como limitación que unas 10 fotos tienen etiqueta dudosa.
- **Prueba realizada:** se agregó a `generar_exclusiones` (en `src/eda.py`) la opción `retirar_conflictivas` y se volvió a ejecutar el notebook 02 completo.
- **Resultado:** se retiran 68 imágenes (56 de entrenamiento y 12 de validación). Particiones finales: entrenamiento 5.600, validación 1.877, prueba 1.885. El brillo promedio por clase quedó entre 114,5 y 124,0 (escala 0–255).
- **Revisión de la decisión:** pendiente (se revisa después de ejecutar los experimentos).

## 2026-11-15 · Protocolo, hipótesis y primeros experimentos: E0 y E1 (notebook 03)
- **Quién:** Camilo Ayazo.
- **Problema encontrado:** antes de entrenar había que cerrar el protocolo y escribir las hipótesis, como exige el profesor. Además, la configuración guardada en Drive todavía tenía los valores de la propuesta inicial.
- **Alternativas consideradas:** Backbone A = MobileNetV2 o ResNet18; una semilla o tres; con o sin pesos por clase; presupuesto propuesto, E0 lineal o menos épocas.
- **Decisión:** A = ResNet18 y B = MobileNetV2; tres semillas en E1 y E3; pesos por clase; presupuesto propuesto. Se registraron las hipótesis de E0 y E1 antes de ejecutar (`docs/03_hipotesis.md`). Se actualizó `configs/config.yaml` en Drive.
- **Prueba realizada:** notebook `03_E0_E1.ipynb` en Colab con GPU Tesla T4, semilla 42.
- **Resultado (prueba, 1.885 imágenes):**
  - E0 (CNN pequeña, 64×64): macro-F1 0,464 · accuracy 0,597 · mejor época 8 · entrenamiento 348 s · 0,58 ms por imagen · 0,1 MB.
  - E1 (ResNet18 congelada): macro-F1 0,659 · accuracy 0,741 · mejor época 8 · entrenamiento 543 s · 3,72 ms por imagen · 44,8 MB.
  - F1 por clase en E1: cmd 0,870 · cbsd 0,692 · healthy 0,670 · cgm 0,648 · cbb 0,414.
  - 92 de 481 fotos de cbsd se clasificaron como cbb. En los 8 errores de mayor confianza de E1, 6 fueron predichos como cbb, casi todos en hojas muy amarillas o marchitas con puntos oscuros; dos de ellos (`test-cgm-136` y `test-cgm-102`) son fotos de prueba cuya copia idéntica tenía otra etiqueta.
  - La demostración en vivo funcionó: carga de un lote (8, 3, 224, 224), inferencia de una foto, macro-F1 a mano igual al de scikit-learn (0,659) y cambio de brillo.
- **Revisión de la decisión:** pendiente (se revisa con E2 y E3).

## 2026-11-17/18 · Repositorio del equipo, reproducción de E0/E1 y experimentos E2 y E3 (notebooks 03 y 04)
- **Quién:** Camilo Mangones.
- **Problema encontrado:** el repositorio del equipo debía quedar en una cuenta compartida por los integrantes, y E2 necesitaba el modelo E1 guardado, que no estaba en el repositorio. Al ejecutar desde la cuenta de Camilo Mangones apareció `FileNotFoundError: /content/drive/MyDrive/yuca-comparacion`, porque la carpeta no estaba directamente en "Mi unidad".
- **Alternativas consideradas:** usar el Drive de Camilo Ayazo o montar el proyecto en el Drive de Camilo Mangones y volver a entrenar E0 y E1.
- **Decisión:** se creó el repositorio `CJmangones/yuca-comparacion`, se montó el proyecto en el Drive de Camilo Mangones (moviendo la carpeta a "Mi unidad") y se volvieron a ejecutar E0 y E1 antes de E2 y E3. Las hipótesis de E2, E3 y del experimento adicional se registraron antes de ejecutar.
- **Prueba realizada:** notebooks 03 y 04 en Colab con GPU Tesla T4.
- **Resultado:**
  - **Reproducibilidad:** E0 y E1 dieron exactamente los mismos valores que el 15 de noviembre en cada época (E0 macro-F1 0,4638; E1 0,6590); solo cambió el tiempo en unos segundos.
  - E2 (ResNet18 con `layer4` descongelado, 8,4 M de parámetros entrenables): macro-F1 0,746 · accuracy 0,817 · mejor época 5 de 5 · 263 s (695 s acumulado con E1).
  - E3 (MobileNetV2 congelada): macro-F1 0,687 · accuracy 0,758 · 526 s · 5,10 ms por imagen · 9,1 MB.
  - Estabilidad: E1 0,655 ± 0,009 y E3 0,681 ± 0,007 en tres semillas (42, 1 y 2).
  - F1 por clase en E2: cmd 0,903 · cbsd 0,806 · healthy 0,725 · cgm 0,719 · cbb 0,575. cbb sigue siendo la clase más difícil en todos los experimentos.
- **Revisión de la decisión:** volver a entrenar E0 y E1 fue acertado: además de habilitar E2, demostró que el proyecto es reproducible desde otra cuenta.

## 2026-11-18 · Experimento adicional, Grad-CAM y análisis de errores (notebook 05)
- **Quién:** Camilo Mangones.
- **Problema encontrado:** el experimento de augmentation no se ejecutó en la primera pasada del notebook 05 y, tras una desconexión de Colab, las celdas fallaron con `No module named 'src'` y luego con `FileNotFoundError` en el cargador de datos, porque la sesión nueva había perdido la carpeta de trabajo y las fotos descomprimidas.
- **Alternativas consideradas:** volver a ejecutar todo el notebook o reconstruir solo la preparación (montar Drive, entrar a la carpeta y descomprimir los datos) y ejecutar lo pendiente.
- **Decisión:** reconstruir solo la preparación y ejecutar E1_aug y el Grad-CAM en una celda, sin repetir lo que ya estaba guardado.
- **Prueba realizada:** notebook 05 en Colab con GPU Tesla T4.
- **Resultado:**
  - Brillo (×0,5 / ×1,0 / ×1,5): E1 0,604 / 0,659 / 0,618; E3 0,628 / 0,687 / 0,616. Con ×1,0 se reproduce exactamente el resultado original. El recall de healthy baja a 0,49 (E1) y 0,42 (E3) al aclarar.
  - E1_aug: macro-F1 0,576 frente a 0,659 de E1; empeoró en las cinco clases.
  - E1 frente a E3: ambos aciertan 1.229 fotos, ambos fallan 289, solo E1 acierta 168 y solo E3 acierta 199.
  - Grad-CAM de 4 imágenes de E1 y análisis de los 8 errores de mayor confianza (`docs/04_analisis_errores.md`).
- **Revisión de la decisión:** ejecutar solo lo pendiente ahorró volver a entrenar E1_aug y el resto del notebook.

---

## 2026-11-21 · Observaciones del control del día 7
- **Quién:** equipo (decisiones). Ejecución en Colab: Camilo Mangones.
- **Problema encontrado:** en el control del día 7 el profesor pidió: tercer modelo, verificar que no sea el mismo dataset, verificar el formato y la resolución de las imágenes, y una prueba de 1.000 imágenes bien repartidas (unas 8.000 para el resto). La prueba publicada tiene 1.885 fotos desbalanceadas (cmd 886, healthy 105).
- **Alternativas consideradas:** (1) tercer modelo: ResNet50 u otra arquitectura preentrenada de torchvision; (2) validación de la partición nueva: 200 por clase (healthy entrena con 124) o 100 por clase (healthy entrena con 224); (3) resolución: solo verificarla o además entrenar con otra resolución; (4) qué experimentos repetir: solo los preentrenados o E0 a E4.
- **Decisión:** ResNet50 congelada como E4, con la hipótesis "mejor que E1 y E3" escrita antes de ejecutar; partición nueva con 200 por clase en prueba y en validación y el resto en entrenamiento, aceptando que healthy entrena con 124 fotos; resolución solo verificada; repetir E0 a E4 en la partición nueva.
- **Prueba realizada:** verificación de formato y resolución sobre el inventario; revisión de las cuatro fuentes de datos indicadas; `src/particion.py` crea la partición agrupando duplicados y comprueba que ningún grupo quede en dos particiones; notebook `06_revision_dia7.ipynb`.
- **Resultado:** las 9.430 fotos son JPG en RGB, ninguna mide menos de 224 px; las fotos sanas pesan menos de la mitad que las de cmd (posible atajo). Usamos solo TensorFlow Datasets (iCassava 2019); las otras fuentes son conjuntos distintos. Partición nueva: 9.337 fotos (7.337 / 1.000 / 1.000), sin grupos repartidos entre particiones.
- **Revisión de la decisión:** ver la entrada del 25 de noviembre.

## 2026-11-25 · Resultados en la partición balanceada y semillas de E4
- **Quién:** equipo. Ejecución en Colab: Camilo Mangones.
- **Problema encontrado:** con la semilla 42, E4 superó a E3 por solo 0,0225 de macro-F1 en la prueba, y en validación obtuvieron prácticamente lo mismo (0,7185 frente a 0,7187). Con una sola semilla no se sabía si la ventaja era real.
- **Alternativas consideradas:** (a) entregar con una sola semilla y declararlo como limitación; (b) ejecutar las semillas 1 y 2 de E1, E3 y E4 (alrededor de una hora más de GPU).
- **Decisión:** opción (b), y registrar la hipótesis de E4 como cumplida con los datos de la semilla 42.
- **Prueba realizada:** notebook 06 con la partición balanceada: E0, E1, E3, E4 y E2 con semilla 42; luego E1, E3 y E4 con semillas 1 y 2 (GPU Tesla T4).
- **Resultado:** macro-F1 con semilla 42: E0 0,448 · E1 0,684 · E2 0,733 · E3 0,713 · E4 0,735. Con tres semillas: E1 0,677 ± 0,014 · E3 0,719 ± 0,006 · E4 0,736 ± 0,004. E4 superó a E3 con cada semilla (+0,022, +0,016 y +0,012).
- **Revisión de la decisión:** ejecutar las semillas fue acertado: confirmó que la ventaja de E4 sobre E3 no depende de la semilla. Mantener 200 fotos por clase en validación dejó a healthy con 124 fotos de entrenamiento; aun así, healthy fue la clase con mejor F1 en E3 y E4. Recomendación del equipo: depende del uso (E4 o E2 si importa el acierto, E3 si se necesita un modelo liviano).

## Plantilla para las siguientes entradas

## AAAA-MM-DD · título corto
- **Quién:**
- **Problema encontrado:**
- **Alternativas consideradas:**
- **Decisión:**
- **Prueba realizada:**
- **Resultado:**
- **Revisión de la decisión:**
