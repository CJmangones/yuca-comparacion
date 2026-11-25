"""Partición balanceada (pedida en la revisión del día 7).

Se juntan todas las imágenes válidas y se reparten de nuevo:
  - prueba:      200 imágenes por clase (1.000 en total), balanceada
  - validación:  200 imágenes por clase (1.000 en total), balanceada
  - entrenamiento: todas las demás (desbalanceado, como el dataset)

Reglas para evitar fugas y etiquetas dudosas:
  1. Las fotos idénticas (mismo MD5) o casi idénticas (dHash) forman un "grupo".
     Un grupo entero va a UNA sola partición: nunca se reparte entre entrenamiento y prueba.
  2. Si un grupo tiene fotos con etiquetas distintas, se retira completo (etiqueta dudosa).
  3. De cada grupo con la misma etiqueta se conserva una sola copia.

Uso:  python -m src.particion
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.datos import CLASES

RUTA_SALIDA = Path("resultados/particion_balanceada.csv")


class _Grupos:
    """Une imágenes relacionadas (union-find): si A~B y B~C, A, B y C quedan juntas."""

    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}

    def raiz(self, e):
        while self.padre[e] != e:
            self.padre[e] = self.padre[self.padre[e]]
            e = self.padre[e]
        return e

    def unir(self, a, b):
        ra, rb = self.raiz(a), self.raiz(b)
        if ra != rb:
            self.padre[rb] = ra


def crear_particion_balanceada(inventario, casi_duplicados=None, por_clase_prueba=200,
                               por_clase_validacion=200, semilla=42):
    inv = inventario.copy()
    grupos = _Grupos(inv["ruta"])
    # 1a. fotos idénticas (mismo MD5)
    for _, g in inv.groupby("md5"):
        rutas = list(g["ruta"])
        for r in rutas[1:]:
            grupos.unir(rutas[0], r)
    # 1b. fotos casi idénticas
    if casi_duplicados is not None:
        for _, par in casi_duplicados.iterrows():
            if par["ruta_a"] in grupos.padre and par["ruta_b"] in grupos.padre:
                grupos.unir(par["ruta_a"], par["ruta_b"])
    inv["grupo"] = inv["ruta"].map(grupos.raiz)

    # 2. grupos con etiquetas distintas: se retiran completos
    etiquetas = inv.groupby("grupo")["clase"].nunique()
    conflictivos = set(etiquetas[etiquetas > 1].index)
    retiradas_conflicto = inv[inv["grupo"].isin(conflictivos)]
    inv = inv[~inv["grupo"].isin(conflictivos)]

    # 3. una sola copia por grupo
    antes = len(inv)
    inv = inv.sort_values("ruta").drop_duplicates("grupo", keep="first")
    copias_retiradas = antes - len(inv)

    # 4. reparto por clase con semilla fija
    rng = np.random.default_rng(semilla)
    filas = []
    for clase in CLASES:
        sub = inv[inv["clase"] == clase].sort_values("ruta")
        orden = rng.permutation(len(sub))
        sub = sub.iloc[orden]
        n_p, n_v = por_clase_prueba, por_clase_validacion
        if len(sub) < n_p + n_v + 1:
            raise ValueError(f"La clase {clase} solo tiene {len(sub)} imágenes válidas")
        asignacion = ["test"] * n_p + ["validation"] * n_v + ["train"] * (len(sub) - n_p - n_v)
        filas.append(sub.assign(particion_nueva=asignacion))
    nueva = pd.concat(filas)[["ruta", "clase", "particion", "particion_nueva", "md5", "grupo"]]
    resumen = {
        "imagenes_iniciales": len(inventario),
        "retiradas_por_etiqueta_contradictoria": len(retiradas_conflicto),
        "copias_retiradas": copias_retiradas,
        "imagenes_finales": len(nueva),
    }
    return nueva, resumen


def verificar_sin_fugas(nueva):
    """Comprueba que ningún grupo (foto idéntica o casi idéntica) aparezca en dos particiones."""
    cruces = nueva.groupby("grupo")["particion_nueva"].nunique()
    md5_cruces = nueva.groupby("md5")["particion_nueva"].nunique()
    return int((cruces > 1).sum()), int((md5_cruces > 1).sum())


def main():
    inventario = pd.read_csv("resultados/inventario.csv")
    ruta_casi = Path("resultados/eda/casi_duplicados.csv")
    casi = pd.read_csv(ruta_casi) if ruta_casi.exists() else None
    nueva, resumen = crear_particion_balanceada(inventario, casi)
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    nueva.to_csv(RUTA_SALIDA, index=False)
    print(resumen)
    print(pd.crosstab(nueva["clase"], nueva["particion_nueva"], margins=True))
    print("Grupos repartidos entre particiones:", verificar_sin_fugas(nueva))


if __name__ == "__main__":
    main()
