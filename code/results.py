"""Genera las tablas y numeros reportados en el paper.

Escribe CSVs en code/output/ y muestra un resumen por consola.
"""

from __future__ import annotations

import csv
import os
from typing import List

import model
import population

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

P_VALUES: List[float] = [0.001, 0.01, 0.05, 0.15]
N_VALUES: List[int] = [1, 2, 5, 10, 15, 20, 25, 30]
IAP_POOLS: List[float] = [1.0e5, 1.0e6, 5.0e6, 1.0e7, 5.0e7]
IAP_P: List[float] = [1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2]


def ensure_out() -> None:
    os.makedirs(OUT, exist_ok=True)


def write_naive() -> None:
    path = os.path.join(OUT, "table_naive.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["N", "individuos", "p", "P_no_homicida"])
        for N in N_VALUES:
            ind = model.total_individuals_naive(N)
            for p in P_VALUES:
                w.writerow([N, ind, p, f"{model.prob_no_killer_naive(p, N):.6e}"])


def write_pedigree() -> None:
    path = os.path.join(OUT, "table_pedigree.csv")
    Nmax = 40
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "casillas_2n", "poblacion", "antepasados_distintos"])
        for n in range(Nmax + 1):
            slots = float(2 ** n)
            pop = population.world_population_gen(n)
            distinct = min(slots, pop)
            w.writerow([n, f"{slots:.6e}", f"{pop:.6e}", f"{distinct:.6e}"])


def write_iap() -> None:
    path = os.path.join(OUT, "table_iap.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pool", "p", "P_desciende_de_homicida"])
        for pool in IAP_POOLS:
            for p in IAP_P:
                pr = model.prob_descends_from_killer_iap(p, pool)
                w.writerow([f"{pool:.0f}", p, f"{pr:.12f}"])


ISLAND_NE: List[float] = [50.0, 200.0, 1.0e3, 1.0e4, 1.0e6]


def write_island() -> None:
    """Tabla de poblaciones aisladas: generacion del IAP (Chang) y probabilidad
    de descender de un homicida, en funcion del tamano efectivo Ne."""
    path = os.path.join(OUT, "table_island.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Ne", "IAP_generaciones", "P_desc_p_1e-3", "P_desc_p_1e-2"])
        for Ne in ISLAND_NE:
            g = model.chang_iap_generations(Ne)
            p3 = model.prob_descends_from_killer_closed(1.0e-3, Ne)
            p2 = model.prob_descends_from_killer_closed(1.0e-2, Ne)
            w.writerow([f"{Ne:.0f}", f"{g:.2f}", f"{p3:.6f}", f"{p2:.6f}"])



def summary() -> None:
    print("=" * 64)
    print("RESUMEN DE RESULTADOS")
    print("=" * 64)
    iap_gen = model.iap_generation(6000.0)
    print(f"IAP ~6000 anios  ->  ~{iap_gen} generaciones (a 28 anios/gen)")
    print()
    print("Generaciones hasta saturar la poblacion (2^n >= pop):")
    for pop in (1.0e6, 1.0e8, 8.0e9):
        g = model.generations_until_saturation(pop)
        print(f"  poblacion {pop:>10.0e}  ->  n = {g}  (~{g*28} anios)")
    print()
    print("Modelo ingenuo, P(ningun antepasado homicida):")
    for N in (5, 10, 15, 20):
        ind = model.total_individuals_naive(N)
        ps = "  ".join(
            f"p={p}: {model.prob_no_killer_naive(p, N):.2e}" for p in P_VALUES
        )
        print(f"  N={N:>2} ({ind:>12,} indiv.)  {ps}")
    print()
    print("Argumento IAP (pool 5,000,000):")
    for p in IAP_P:
        pr = model.prob_descends_from_killer_iap(p, 5.0e6)
        print(f"  p={p:<7}  P(desciende de homicida) = {pr:.12f}")
    print()
    print("Poblaciones aisladas (efecto fundador, IAP ~1.77*log2(Ne)):")
    for Ne in ISLAND_NE:
        g = model.chang_iap_generations(Ne)
        p2 = model.prob_descends_from_killer_closed(1.0e-2, Ne)
        print(
            f"  Ne={Ne:>10.0f}  IAP~{g:5.1f} gen (~{g*28:5.0f} anios)"
            f"  P_desc(p=0.01)={p2:.6f}"
        )
    print("=" * 64)


def main() -> None:
    ensure_out()
    write_naive()
    write_pedigree()
    write_iap()
    write_island()
    print(f"CSVs escritos en {OUT}\n")
    summary()


if __name__ == "__main__":
    main()
