"""Modelo matematico nucleo del paper.

Formaliza la probabilidad de que un individuo NO tenga ningun antepasado
homicida, bajo tres niveles de modelado:

1. Modelo ingenuo: antepasados independientes que se duplican cada generacion.
2. Colapso de pedigri: los antepasados distintos saturan la poblacion de cada
   epoca, de modo que el conteo real esta acotado por la poblacion.
3. Punto de ancestros identicos (IAP): pasado cierto horizonte, el conjunto de
   antepasados coincide con toda la poblacion reproductora global; basta un solo
   homicida en ese acervo.

Todas las probabilidades muy pequenas se calculan en dominio logaritmico para
evitar underflow.

Definiciones:
- p : probabilidad de que UN individuo cualquiera haya causado la muerte de otro
      humano a lo largo de su vida (definicion amplia: guerra, defensa, etc.).
- N : numero de generaciones hacia atras consideradas.
"""

from __future__ import annotations

import math
from typing import Callable, List, Union

GEN_YEARS_DEFAULT: float = 28.0

PopulationSpec = Union[float, Callable[[int], float]]


def total_individuals_naive(N: int) -> int:
    """ego (gen 0) + todos los antepasados hasta la generacion N.

    sum_{k=0}^{N} 2^k = 2^(N+1) - 1.
    """
    return 2 ** (N + 1) - 1


def total_ancestors_naive(N: int) -> int:
    """Antepasados (excluyendo a ego) hasta la generacion N: 2^(N+1) - 2."""
    return 2 ** (N + 1) - 2


def log_prob_no_killer(p: float, count: float) -> float:
    """log de (1-p)^count, numericamente estable.

    Devuelve 0.0 si p<=0 y -inf si p>=1.
    """
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return -math.inf
    return count * math.log1p(-p)


def prob_no_killer(p: float, count: float) -> float:
    """(1-p)^count evaluado de forma estable."""
    return math.exp(log_prob_no_killer(p, count))


def prob_no_killer_naive(p: float, N: int) -> float:
    """Probabilidad de que ni ego ni ninguno de sus antepasados (modelo
    ingenuo, hasta generacion N) sea homicida."""
    return prob_no_killer(p, total_individuals_naive(N))


def prob_at_least_one_killer(p: float, count: float) -> float:
    """1 - (1-p)^count, estable via expm1."""
    return -math.expm1(log_prob_no_killer(p, count))


def generations_until_saturation(pop_size: float) -> int:
    """Menor n tal que 2^n >= pop_size (cuando las 'casillas' de antepasado
    igualan a la poblacion disponible)."""
    if pop_size <= 1:
        return 0
    return math.ceil(math.log2(pop_size))


def distinct_ancestors_per_gen(N: int, pop_size: PopulationSpec) -> List[float]:
    """Antepasados DISTINTOS en cada generacion bajo colapso de pedigri.

    En la generacion n las 'casillas' ingenuas son 2^n, pero no pueden exceder
    la poblacion reproductora de esa epoca. Modelo saturante:

        distinct(n) = min(2^n, pop(n)).

    pop_size puede ser un escalar (poblacion constante) o una funcion n -> pop.
    """
    out: List[float] = []
    for n in range(N + 1):
        slots = float(2 ** n)
        pop = pop_size(n) if callable(pop_size) else float(pop_size)
        out.append(min(slots, pop))
    return out


def total_distinct_ancestors(N: int, pop_size: PopulationSpec) -> float:
    """Suma de antepasados distintos por generacion (cota superior del numero
    de individuos involucrados; ver limitaciones en el paper)."""
    return float(sum(distinct_ancestors_per_gen(N, pop_size)))


def prob_no_killer_pedigree(p: float, N: int, pop_size: PopulationSpec) -> float:
    """Probabilidad de no tener antepasado homicida bajo colapso de pedigri."""
    return prob_no_killer(p, total_distinct_ancestors(N, pop_size))


def iap_generation(iap_years: float, gen_years: float = GEN_YEARS_DEFAULT) -> int:
    """Generacion correspondiente al punto de ancestros identicos."""
    return round(iap_years / gen_years)


def prob_descends_from_killer_iap(p: float, pool_size: float) -> float:
    """Bajo el argumento IAP: pasado el punto de ancestros identicos, el
    conjunto de antepasados de ego ES toda la poblacion reproductora global de
    esa epoca (tamano pool_size). La probabilidad de que ego descienda de al
    menos un homicida es 1 - (1-p)^pool_size."""
    return prob_at_least_one_killer(p, pool_size)


if __name__ == "__main__":
    demo_p = [0.001, 0.01, 0.05, 0.15]
    print("Modelo ingenuo: P(ningun antepasado homicida)")
    print(f"{'N':>4} {'individuos':>14} " + " ".join(f"p={p:<7}" for p in demo_p))
    for N in (5, 10, 15, 20, 30):
        row = [f"{N:>4}", f"{total_individuals_naive(N):>14,}"]
        for p in demo_p:
            row.append(f"{prob_no_killer_naive(p, N):>9.2e}")
        print(" ".join(row))

    print()
    iap_pool = 5_000_000.0
    print("Argumento IAP (pool reproductor global ~5M):")
    for p in (1e-6, 1e-4, 1e-3, 0.01):
        pr = prob_descends_from_killer_iap(p, iap_pool)
        print(f"  p={p:<8} P(desciende de homicida) = {pr:.12f}")
