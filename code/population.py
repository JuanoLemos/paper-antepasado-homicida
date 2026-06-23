"""Serie poblacional mundial de largo plazo (datos citables).

Se usa para el colapso de pedigri: cuantos antepasados DISTINTOS puede tener
ego en cada generacion esta acotado por la poblacion reproductora de esa epoca.

FUENTE: Our World in Data, "Population Growth" (Ritchie et al., 2023), serie de
largo plazo basada en HYDE (2023), Gapminder (2022, 2023) y UN WPP (2024).
Hitos tomados de la serie publicada (CC-BY):
    10 000 a.C.  ~4 millones
    1700         595 millones
    1800         983 millones
    1900         1.6 mil millones
    2022         8 mil millones
Valor para el a.C. 1 (~190 millones) segun la serie HYDE de largo plazo.
Consultado: 2026-06.

Interpolacion log-lineal en anios antes del presente (BP). El presente se fija
en PRESENT_YEAR.
"""

from __future__ import annotations

import math
from typing import List, Tuple

GEN_YEARS_DEFAULT: float = 28.0
PRESENT_YEAR: int = 2025

SOURCE: str = (
    "Our World in Data (Ritchie et al., 2023), 'Population Growth'; "
    "serie de largo plazo HYDE (2023), Gapminder, UN WPP (2024). CC-BY."
)

# Anclas (anio en la era comun; negativo = a.C.) -> poblacion mundial.
ANCHORS_CE: List[Tuple[float, float]] = [
    (-10000.0, 4.0e6),
    (1.0, 1.9e8),
    (1700.0, 5.95e8),
    (1800.0, 9.83e8),
    (1900.0, 1.6e9),
    (2022.0, 8.0e9),
]

# Derivadas a "anios antes del presente" (BP), ordenadas de presente a pasado.
ANCHORS_BP: List[Tuple[float, float]] = sorted(
    ((float(PRESENT_YEAR) - y, p) for (y, p) in ANCHORS_CE),
    key=lambda t: t[0],
)


def world_population_bp(year_bp: float) -> float:
    """Poblacion mundial aproximada a 'year_bp' anios antes del presente."""
    if year_bp <= ANCHORS_BP[0][0]:
        return ANCHORS_BP[0][1]
    if year_bp >= ANCHORS_BP[-1][0]:
        return ANCHORS_BP[-1][1]
    for (y0, p0), (y1, p1) in zip(ANCHORS_BP, ANCHORS_BP[1:]):
        if y0 <= year_bp <= y1:
            t = (year_bp - y0) / (y1 - y0)
            log_p = math.log(p0) + t * (math.log(p1) - math.log(p0))
            return math.exp(log_p)
    return ANCHORS_BP[-1][1]


def world_population_gen(n: int, gen_years: float = GEN_YEARS_DEFAULT) -> float:
    """Poblacion mundial aproximada n generaciones atras."""
    return world_population_bp(n * gen_years)
