# Hipótesis previas

> Las redactan los integrantes **antes** de ejecutar cada experimento, con fecha. No se editan después de ver
> los resultados: si una hipótesis falla, se comenta en el informe (eso también suma).

Formato sugerido: *"Creemos que ___ porque ___. Si es cierto, esperamos ver ___."*

| Exp. | Hipótesis | Predicción concreta (qué número o comportamiento esperamos) | Autor | Fecha |
|---|---|---|---|---|
| E0 | Aun entrenada desde cero, una red pequeña con 5.600 fotos alcanza a aprender los patrones más visibles de las enfermedades. | Macro-F1 en prueba mayor que 0,55. | Camilo Ayazo | 2026-11-15 |
| E1 | Lo aprendido por ResNet18 en ImageNet (bordes, texturas, manchas) sirve directamente para ver lesiones en hojas, aunque solo se entrene la cabeza. | Macro-F1 al menos 0,20 por encima de E0 (es decir, mayor que 0,75 si E0 cumple su predicción). La clase más difícil (F1 más bajo) será cbsd, porque sus manchas amarillas difusas se parecen al mosaico y a hojas sanas. | Camilo Ayazo | 2026-11-15 |
| Pesos por clase (E0–E3) | Dar más peso en la pérdida a las clases escasas mejora su detección. | El recall de cbb y healthy será mayor que sin pesos, aunque cmd pierda un poco. | Camilo Ayazo | 2026-11-15 |
| E2 | Adaptar el último bloque de ResNet18 (layer4) a hojas de yuca permite aprender síntomas específicos que ImageNet no tenía. | Macro-F1 al menos 0,05 por encima de E1. | Camilo Ayazo | 2026-11-17 |
| E3 | Con el backbone congelado, MobileNetV2 y ResNet18 aportan características parecidas porque ambas aprendieron de ImageNet; MobileNetV2 fue diseñada para celulares. | Macro-F1 parecido a E1 (diferencia de ±0,03 o menos), con menor tiempo de inferencia y menor tamaño que E1. | Camilo Ayazo | 2026-11-17 |
| Adicional: brillo | Al aclarar, el amarillo se satura y las hojas se parecen más a las de cbb. | El macro-F1 de E1 y E3 cae más con brillo ×1,5 que con ×0,5. | Camilo Ayazo | 2026-11-17 |
| Adicional: augmentation | Ver variaciones de las mismas fotos ayuda a no memorizar detalles irrelevantes como el fondo. | E1 con augmentation obtiene un macro-F1 un poco mayor que E1 sin augmentation. | Camilo Ayazo | 2026-11-17 |

Preguntas para pensar (no son respuestas):
- ¿Qué clases creen que serán más difíciles y por qué? (miren la distribución del inventario y algunas fotos)
- ¿Cuánto esperan que mejore E1 sobre E0? ¿Por qué una red entrenada con fotos generales serviría para hojas?
- ¿Descongelar un bloque puede empeorar algo? ¿Qué costo tiene?
- ¿Cuál de las dos arquitecturas esperan que sea más rápida? ¿Y más precisa?

> Nota: la hipótesis sobre los pesos por clase solo se puede comprobar del todo con una ejecución sin pesos, que no está en el plan.
> Si no se hace, se analizará con el recall por clase de E1 y se declarará el límite.

## Contraste con los resultados (2026-11-15)

| Hipótesis | Resultado | ¿Se cumplió? | Lectura del equipo |
|---|---|---|---|
| E0: macro-F1 > 0,55 | 0,464 | No | Al reducir las fotos a 64×64 se pierde el detalle: desaparecen las manchas pequeñas que distinguen las enfermedades. |
| E1: al menos +0,20 sobre E0 | +0,195 (0,659 frente a 0,464) | Por 0,005 no alcanzó el umbral | Se cumplió en esencia: la transferencia mejoró mucho y 0,005 no cambia la conclusión; se reporta el número tal cual. |
| E1: cbsd será la clase más difícil | La más difícil fue cbb (F1 0,414); cbsd quedó en 0,692 | No | Ver análisis de errores. |
| Pesos por clase suben el recall de cbb y healthy | Recall E1: cbb 0,484, healthy 0,705; precisión de cbb solo 0,362 | No comprobable sin ejecución sin pesos | Posible efecto adverso: los pesos pudieron empujar al modelo a predecir cbb de más. No se puede confirmar sin una ejecución sin pesos. |

## Contraste E2, E3 y estabilidad (2026-11-18)

| Hipótesis | Resultado | ¿Se cumplió? | Lectura del equipo |
|---|---|---|---|
| E3: macro-F1 parecido a E1 (±0,03) | Semilla 42: 0,687 frente a 0,659 (+0,028). Promedio de 3 semillas: 0,681 ± 0,007 frente a 0,655 ± 0,009 (+0,026) | Sí, dentro del margen | E3 es mejor y la diferencia es real: es pequeña, pero la peor semilla de E3 (0,673) supera a la mejor de E1 (0,661), y la diferencia es mayor que la variación entre semillas. |
| E3: más rápida y más liviana que E1 | Tamaño 9,1 MB frente a 44,8 MB; inferencia 5,10 ms frente a 3,85 ms por imagen (GPU T4) | Más liviana sí; más rápida no | La GPU no aprovecha bien MobileNetV2: sus convoluciones separables son muchas operaciones pequeñas, y en GPU una red con capas más grandes como ResNet18 se ejecuta más rápido. En un celular o en CPU probablemente sería al revés (no medido). |
| E2: al menos +0,05 sobre E1 | 0,746 frente a 0,659 (+0,087); mejor época 5 de 5 | Sí | Vale la pena: es la mayor mejora del estudio y el costo extra son unos 4 minutos de GPU; la inferencia no cambia. |

## Contraste del experimento adicional: brillo (2026-11-18)

Macro-F1 en prueba según el factor de brillo (×1,0 reproduce exactamente el resultado original, lo que confirma que el brillo es lo único que cambia):

| Brillo | E1 (ResNet18) | E3 (MobileNetV2) | Recall healthy E1 / E3 |
|---|---|---|---|
| ×0,50 | 0,604 (−0,055) | 0,628 (−0,059) | 0,86 / 0,87 |
| ×0,75 | 0,650 | 0,675 | 0,78 / 0,82 |
| ×1,00 | 0,659 | 0,687 | 0,70 / 0,70 |
| ×1,25 | 0,647 | 0,675 | 0,59 / 0,57 |
| ×1,50 | 0,618 (−0,041) | 0,616 (−0,071) | 0,49 / 0,42 |

| Hipótesis | ¿Se cumplió? | Lectura del equipo |
|---|---|---|
| El macro-F1 cae más al aclarar (×1,5) que al oscurecer (×0,5) | Parcialmente: sí en E3, no en E1 | Los dos modelos reaccionan distinto a la luz. Al aclarar, el recall de healthy se desploma y al oscurecer sube: aclarar puede simular síntomas (amarillamiento), el modelo pudo aprender el atajo "verde intenso = sana" y, en general, muestra poca robustez a cambios de luz que en campo son comunes. |

## Contraste del experimento adicional: augmentation (2026-11-18)

| | Macro-F1 | Accuracy | F1 cbb | F1 cbsd | F1 cgm | F1 cmd | F1 healthy | F1 entrenamiento (última época) |
|---|---|---|---|---|---|---|---|---|
| E1 | 0,659 | 0,741 | 0,414 | 0,692 | 0,648 | 0,871 | 0,670 | 0,627 |
| E1_aug | 0,576 | 0,642 | 0,409 | 0,564 | 0,583 | 0,807 | 0,518 | 0,554 |

| Hipótesis | ¿Se cumplió? | Lectura del equipo |
|---|---|---|
| E1 con augmentation obtiene un macro-F1 un poco mayor que E1 | No: bajó 0,083 y empeoró en las cinco clases | Con fotos que cambian en cada época la tarea es más difícil y 10 épocas no alcanzan; con el backbone congelado solo aprende la cabeza (2.565 parámetros), que no puede adaptarse a tanta variación; y los recortes de hasta el 70 % pueden dejar fuera la lesión. El F1 de entrenamiento también bajó, lo que indica que al modelo le cuesta más aprender, no que memorice. |

## Hipótesis de la revisión del día 7 (registrada antes de ejecutar, 2026-11-21)

| Exp. | Hipótesis | Predicción concreta | Autor | Fecha |
|---|---|---|---|---|
| E4 | ResNet50 es una arquitectura más grande y sus características de ImageNet son mejores. | Con el backbone congelado y el mismo entrenamiento, E4 obtiene un macro-F1 mayor que E1 y que E3 en la partición balanceada. | Equipo | 2026-11-21 |

### Contraste de la hipótesis E4 (partición balanceada, semilla 42) — decisión del equipo 2026-11-25
| Exp. | Macro-F1 prueba | Macro-F1 validación |
|---|---|---|
| B_E1 (ResNet18) | 0,6838 | 0,7062 |
| B_E3 (MobileNetV2) | 0,7125 | 0,7187 |
| B_E4 (ResNet50) | 0,7350 | 0,7185 |

**Resultado registrado por el equipo:** se cumple. E4 supera a E1 (+0,051) y a E3 (+0,0225) en macro-F1 de prueba.
Datos que acompañan el resultado: en validación E4 y E3 obtienen prácticamente lo mismo; es una sola semilla (se ejecutan las semillas 1 y 2 para medir la estabilidad); E4 es el modelo más lento (8,33 ms/img) y pesado (94,29 MB).

### Estabilidad en la partición balanceada (semillas 42, 1 y 2) — 2026-11-25
| Exp. | Semilla 42 | Semilla 1 | Semilla 2 | Media ± desv. | Mín – máx |
|---|---|---|---|---|---|
| B_E1 (ResNet18) | 0,6838 | 0,6856 | 0,6603 | 0,6766 ± 0,0141 | 0,6603 – 0,6856 |
| B_E3 (MobileNetV2) | 0,7125 | 0,7240 | 0,7202 | 0,7189 ± 0,0059 | 0,7125 – 0,7240 |
| B_E4 (ResNet50) | 0,7350 | 0,7404 | 0,7320 | 0,7358 ± 0,0042 | 0,7320 – 0,7404 |

Diferencia E4 − E3 con la misma semilla: +0,0225 (42), +0,0164 (1), +0,0118 (2). El peor resultado de E4 (0,7320) supera al mejor de E3 (0,7240).
