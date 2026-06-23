"""Simulacion Monte Carlo de ascendencia genealogica y homicidio.

Construye una poblacion de M individuos por generacion a lo largo de G
generaciones con emparejamiento aleatorio (cada individuo toma 2 progenitores
al azar de la generacion previa). Cada individuo es 'homicida' de forma
independiente con probabilidad p. Se propaga hacia adelante el indicador
"tiene al menos un antepasado homicida" y se mide la fraccion de la poblacion
presente que lo cumple.

Resultado esperado: incluso con p pequenas y poblaciones finitas, la fraccion
tiende a 1 en pocas generaciones, en linea con el argumento del paper.
"""

from __future__ import annotations

import csv
import os
from typing import List

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")


def run_once(p: float, M: int, G: int, seed: int) -> np.ndarray:
    """Devuelve la fraccion, por generacion, de individuos con >=1 antepasado
    homicida."""
    rng = np.random.default_rng(seed)
    killer = rng.random((G, M)) < p
    has_killer_ancestor = np.zeros((G, M), dtype=bool)
    descends_or_is = np.zeros((G, M), dtype=bool)
    descends_or_is[0] = killer[0]
    for g in range(1, G):
        p1 = rng.integers(0, M, M)
        p2 = rng.integers(0, M, M)
        prev = descends_or_is[g - 1]
        has_killer_ancestor[g] = prev[p1] | prev[p2]
        descends_or_is[g] = killer[g] | has_killer_ancestor[g]
    return has_killer_ancestor.mean(axis=1)


def run_average(p: float, M: int, G: int, reps: int, base_seed: int) -> np.ndarray:
    acc = np.zeros(G)
    for r in range(reps):
        acc += run_once(p, M, G, base_seed + r)
    return acc / reps


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    M = 5000
    G = 30
    reps = 20
    p_values: List[float] = [0.0001, 0.001, 0.01]

    rows = []
    print("Simulacion Monte Carlo")
    print(f"  M={M} individuos/gen, G={G} generaciones, reps={reps}")
    print()
    for p in p_values:
        frac = run_average(p, M, G, reps, base_seed=1234)
        print(f"p = {p}")
        for g in (1, 2, 5, 10, 15, 20, G - 1):
            print(f"  gen {g:>2}: fraccion con antepasado homicida = {frac[g]:.6f}")
        print(f"  -> presente (gen {G-1}): {frac[G-1]:.6f}")
        print()
        for g in range(G):
            rows.append([p, g, f"{frac[g]:.8f}"])

    path = os.path.join(OUT, "simulation.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["p", "generacion", "fraccion_con_antepasado_homicida"])
        w.writerows(rows)
    print(f"Resultados de simulacion escritos en {path}")


if __name__ == "__main__":
    main()
