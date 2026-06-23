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


def run_once_heritable(p: float, h: float, M: int, G: int, seed: int):
    """Como run_once pero con transmision/correlacion del rasgo homicida.

    El estatus de homicida ya no es i.i.d.: depende de los progenitores via
        p_hijo = p + h * (f - p),
    donde f es la fraccion de los 2 progenitores que fueron homicidas y
    h in [0,1] mide la heredabilidad/transmision. Este modelo preserva la
    prevalencia marginal en esperanza (E[f]=p => E[p_hijo]=p), de modo que se
    compara i.i.d. (h=0) contra agrupado (h>0) a igual violencia media.

    Devuelve (fraccion_con_antepasado_homicida_por_gen, prevalencia_por_gen).
    """
    rng = np.random.default_rng(seed)
    killer = np.zeros((G, M), dtype=bool)
    killer[0] = rng.random(M) < p
    has_killer_ancestor = np.zeros((G, M), dtype=bool)
    descends_or_is = np.zeros((G, M), dtype=bool)
    descends_or_is[0] = killer[0]
    for g in range(1, G):
        p1 = rng.integers(0, M, M)
        p2 = rng.integers(0, M, M)
        prevk = killer[g - 1]
        f = (prevk[p1].astype(np.float64) + prevk[p2].astype(np.float64)) / 2.0
        p_child = p + h * (f - p)
        np.clip(p_child, 0.0, 1.0, out=p_child)
        killer[g] = rng.random(M) < p_child
        prev = descends_or_is[g - 1]
        has_killer_ancestor[g] = prev[p1] | prev[p2]
        descends_or_is[g] = killer[g] | has_killer_ancestor[g]
    return has_killer_ancestor.mean(axis=1), killer.mean(axis=1)


def run_average_heritable(p: float, h: float, M: int, G: int, reps: int,
                          base_seed: int):
    """Promedio sobre reps de run_once_heritable.

    Devuelve (fraccion_media_por_gen, prevalencia_media_por_gen).
    """
    frac = np.zeros(G)
    prev = np.zeros(G)
    for r in range(reps):
        fr, pv = run_once_heritable(p, h, M, G, base_seed + r)
        frac += fr
        prev += pv
    return frac / reps, prev / reps


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


def main_island() -> None:
    """Variante de poblaciones aisladas: poblaciones cerradas de tamano M
    (efecto fundador). Cuanto menor es M, antes satura la fraccion con
    antepasado homicida (IAP mas temprano)."""
    os.makedirs(OUT, exist_ok=True)
    G = 30
    reps = 30
    M_values = [50, 200, 1000, 5000]
    p_values: List[float] = [0.001, 0.01, 0.05]

    rows = []
    print("\nSimulacion Monte Carlo -- poblaciones aisladas (cerradas)")
    print(f"  G={G} generaciones, reps={reps}")
    for M in M_values:
        for p in p_values:
            frac = run_average(p, M, G, reps, base_seed=2024)
            cross = next((g for g in range(G) if frac[g] >= 0.999), None)
            cross_s = f"gen {cross}" if cross is not None else ">G"
            print(
                f"  M={M:>5}  p={p:<6}  fraccion gen{G-1}={frac[G-1]:.4f}"
                f"  (>=0.999 en {cross_s})"
            )
            for g in range(G):
                rows.append([M, p, g, f"{frac[g]:.8f}"])

    path = os.path.join(OUT, "simulation_island.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["M", "p", "generacion", "fraccion_con_antepasado_homicida"])
        w.writerows(rows)
    print(f"Resultados de simulacion (isla) escritos en {path}")


def main_heritability() -> None:
    """Robustez a la independencia: correlacion/heredabilidad h del rasgo
    homicida (preservando la prevalencia marginal). Muestra que aun con h alto
    la fraccion con antepasado homicida converge a 1."""
    os.makedirs(OUT, exist_ok=True)
    M = 2000
    G = 30
    reps = 40
    p = 0.01
    h_values = [0.0, 0.3, 0.6, 0.9]

    rows = []
    print("\nSimulacion Monte Carlo -- heredabilidad/correlacion (p=%.3f)" % p)
    print(f"  M={M}, G={G}, reps={reps}")
    for h in h_values:
        frac, prev = run_average_heritable(p, h, M, G, reps, base_seed=777)
        cross = next((g for g in range(G) if frac[g] >= 0.999), None)
        cross_s = f"gen {cross}" if cross is not None else ">G"
        print(
            f"  h={h:<4} fraccion gen{G-1}={frac[G-1]:.4f} (>=0.999 en {cross_s})"
            f"  prevalencia media={prev.mean():.4f} (objetivo {p})"
        )
        for g in range(G):
            rows.append([h, p, g, f"{frac[g]:.8f}", f"{prev[g]:.8f}"])

    path = os.path.join(OUT, "simulation_heritability.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["h", "p", "generacion", "fraccion_con_antepasado_homicida",
                    "prevalencia"])
        w.writerows(rows)
    print(f"Resultados de simulacion (heredabilidad) escritos en {path}")


if __name__ == "__main__":
    main()
    main_island()
    main_heritability()

