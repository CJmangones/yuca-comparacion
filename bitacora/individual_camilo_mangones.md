# Bitácora individual · Camilo José Mangones Florez

Escrita por el integrante, con sus palabras. Sirve para la defensa individual: qué implementé, por qué tomé una decisión y qué dificultad resolví.

---

## 2026-11-17
- **Qué hice hoy:**
  - Creé el repositorio del equipo, `CJmangones/yuca-comparacion`, y subí el proyecto (código, configuración, notebooks, documentos, resultados y bitácoras).
  - Subí a mi Google Drive la carpeta del proyecto para poder ejecutar los notebooks desde mi cuenta.
  - Ejecuté el notebook 03 en Colab con GPU T4: volví a entrenar E0 y E1.
  - Subí al repositorio las hipótesis de E2, E3 y del experimento adicional antes de ejecutarlos.
- **Qué archivo toqué / qué ejecuté:** `notebooks/03_E0_E1.ipynb`; en GitHub, todo el proyecto y luego `docs/03_hipotesis.md` y `docs/02_protocolo.md`.
- **Qué decidí y por qué:** volver a entrenar E0 y E1 desde mi cuenta en vez de usar los resultados que ya existían, para comprobar que el proyecto es reproducible (que otra persona, en otra cuenta, obtiene lo mismo) y para conocer el entorno de Colab, porque tengo que explicarlo en la sustentación.
- **Qué dificultad tuve y cómo la resolví:**
  - Al subir los archivos a GitHub, la primera vez solo cargaron los archivos sueltos; arrastré también las carpetas `src` y `configs`. Además, el mensaje del commit lo había escrito en la casilla de descripción y lo pasé a la casilla del título.
  - En Colab, la primera celda falló con `FileNotFoundError: /content/drive/MyDrive/yuca-comparacion`, porque al descomprimir el ZIP la carpeta quedó dentro de otra (`yuca-comparacion-final`). Lo resolví ubicando la carpeta del proyecto en "Mi unidad".
- **Resultado:** E0 dio macro-F1 0,4638 y E1 0,6590, exactamente igual que el 15 de noviembre, época por época. Solo cambió el tiempo de entrenamiento en unos segundos.

## 2026-11-18
- **Qué hice hoy:**
  - Ejecuté el notebook 04: E3 (MobileNetV2), E2 (ajuste fino de ResNet18) y E1 y E3 con las semillas 1 y 2.
  - Ejecuté el notebook 05: experimento de brillo, E1 con augmentation, análisis de errores y Grad-CAM.
- **Qué archivo toqué / qué ejecuté:** `notebooks/04_E2_E3.ipynb` y `notebooks/05_adicional_y_analisis.ipynb`.
- **Resultados que obtuve:** E2 macro-F1 0,746; E3 0,687; estabilidad E1 0,655 ± 0,009 y E3 0,681 ± 0,007. En el brillo, el macro-F1 cae entre 0,04 y 0,07 en los extremos; E1 con augmentation bajó a 0,576.
- **Qué decidí y por qué:** cuando Colab se desconectó en el notebook 05, reconstruí solo la preparación (conectar Drive, entrar a la carpeta y descomprimir las fotos) y ejecuté lo que faltaba, en vez de volver a correr todo el notebook, para ahorrar tiempo de GPU: lo que ya estaba guardado en Drive no hacía falta repetirlo.
- **Qué dificultad tuve y cómo la resolví:**
  - E1 con augmentation no se había ejecutado en la primera pasada.
  - Después de la desconexión, las celdas fallaron primero con `No module named 'src'` y luego con `FileNotFoundError` en el cargador de datos, porque la sesión nueva había perdido la carpeta de trabajo y las fotos descomprimidas (estaban en el disco temporal de Colab, no en Drive). Lo resolví volviendo a montar Drive, entrando a la carpeta del proyecto y descomprimiendo los datos antes de entrenar.
- **Qué no entiendo todavía:** por qué MobileNetV2 fue más lenta por imagen en la GPU (5,1 ms frente a 3,8 ms de ResNet18) si es cinco veces más pequeña.
