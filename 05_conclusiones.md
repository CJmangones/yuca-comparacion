# Conclusiones (2026-11-18)

> Lecturas elegidas por el equipo a partir de los resultados reales.

## Pregunta de investigación
¿Qué arquitectura preentrenada ofrece el mejor equilibrio entre desempeño por clase, generalización y costo computacional?

## Respuesta del equipo: depende del uso
- **Si lo que más importa es acertar:** E2 (ResNet18 con ajuste fino). Macro-F1 0,746, el mejor del estudio y el mejor F1 en las cinco clases, con el mismo tiempo de inferencia que E1. El ajuste fino vale la pena: es la mayor mejora (+0,087) y cuesta unos 4 minutos más de GPU.
- **Si el modelo debe ir en un dispositivo con poca memoria:** E3 (MobileNetV2). Supera a E1 en extracción de características (0,681 frente a 0,655 en promedio de tres semillas, diferencia mayor que la variación entre semillas) y pesa 5 veces menos (9,1 MB).
- En la GPU T4, MobileNetV2 fue más lenta por imagen (5,1 ms frente a 3,8 ms). La explicación del equipo es que la GPU no aprovecha sus convoluciones separables; en CPU o celular podría ser al revés, pero no lo medimos.

## Experimento adicional
- **Brillo:** ningún modelo es robusto a la luz. Con brillo ×0,5 o ×1,5 el macro-F1 cae entre 0,04 y 0,07, y la clase sana es la más afectada: al aclarar, su recall baja de 0,70 a 0,42–0,49. El equipo lo atribuye a que aclarar simula amarillamiento, a un posible atajo de "verde intenso = sana" y a poca robustez a la luz.
- **Augmentation:** con el backbone congelado y 10 épocas empeoró (0,659 → 0,576). No conviene usarlo así; habría que probarlo con más épocas o junto con el ajuste fino.

## Errores
- La confusión dominante es hacia cbb en hojas muy amarillas o necrosadas (6 de los 8 errores más seguros de E1). El equipo lo atribuye a síntomas parecidos en etapa avanzada.
- El Grad-CAM muestra que el modelo mira la hoja y no el fondo, pero en los errores se guía por el color amarillo o marrón más que por la forma de la lesión.
- E1 y E3 fallan en fotos distintas en 367 casos: los modelos se complementan.

## Lo que no se puede concluir
- Las fotos son de Uganda; no se sabe cómo rinden estos modelos con cultivos colombianos.
- Comparar E2 con E3 no mide solo la arquitectura: E2 además entrena parte del backbone.
- cbb sigue siendo la clase más difícil (F1 0,58 en el mejor modelo), en parte por etiquetas dudosas en el conjunto de datos.
