# EVIDENCE — Trazabilidad de afirmaciones

Cada afirmación del paper se enlaza a su fuente primaria, con cita textual y DOI.
Estado Crossref verificado el 2026-06 contra `https://api.crossref.org/works/{doi}`.

| # | Afirmación en el paper | Fuente | DOI / URL | Cita textual | Crossref |
|---|---|---|---|---|---|
| 1 | `p ≈ 2%` de las muertes humanas se predicen por violencia interpersonal; similar en bandas/tribus prehistóricas. | Gómez, Verdú, González-Megías & Méndez (2016), *Nature* 538:233–237. | 10.1038/nature19758 | "The proportion of human deaths phylogenetically predicted to be caused by interpersonal violence stood at 2%. […] similar to the percentage seen in prehistoric bands and tribes." | OK |
| 2a | MRCA de *Homo sapiens* hace ~2.000–5.000 años. | Rohde, D. L. T. (2003), *On the common ancestors of all living humans* (preprint, sometido a *Am. J. Phys. Anthropol.*). | tedlab.mit.edu (Wayback 2015-01-22) | "our most recent common ancestor may have lived between 2,000 and 5,000 years ago." | n/a (preprint) |
| 2b | IAP humano hace ~5.000–15.000 años (cota conservadora 1.000–15.000). | Rohde (2003); Rohde, Olson & Chang (2004), *Nature* 431:562–566. | 10.1038/nature02842 | "The point beyond which everyone alive today shares the same set of ancestors […] most likely falls between 1,000 and 15,000 years ago." | OK |
| 3 | En población bien mezclada de tamaño N, el IAP está a ~1.77·log₂(N) generaciones. | Chang, J. T. (1999), *Adv. Appl. Probab.* 31:1002–1026. | 10.1239/aap/1029955256 | "we only have to go 1.77 log₂(N) generations in the past to find the time when everyone in the population (who left descendants) is an ancestor to the entire population." (vía resumen de la lit.) | OK |
| 4 | ~1.17×10¹¹ humanos han nacido en total (alt. ~1.08×10¹¹). | Kaneda & Haub (2022), Population Reference Bureau. | prb.org/articles/how-many-people-have-ever-lived-on-earth | "About 117 billion members of our species have ever been born on Earth" (117 020 448 575). OWID da ~108 mil millones. | n/a (informe) |
| 5 | Longitud generacional media ℓ ≈ 28 años. | Fenner, J. N. (2005), *Am. J. Phys. Anthropol.* 128(2):415–423. | 10.1002/ajpa.20188 | "Cross-cultural estimation of the human generation interval…" (estimación ampliamente citada ≈ 28 años). | OK |
| 6 | Serie poblacional mundial de largo plazo (10.000 a.C.: ~4 M; 1700: 595 M; 1800: 983 M; 1900: 1,6 mil M; 2022: 8 mil M). | Ritchie et al. (2023), *Our World in Data* — HYDE (2023), Gapminder, UN WPP (2024). | ourworldindata.org/population-growth | "As recently as 12,000 years ago, there were only 4 million people worldwide." Hitos de la serie de largo plazo (CC-BY). | n/a (dataset) |
| 7 | Distinción ascendencia genealógica vs. genética; multiplicidad de ancestros genealógicos. | Ralph & Coop (2013), *PLoS Biology* 11(5):e1001555. | 10.1371/journal.pbio.1001555 | "for every genetic common ancestor there are tens of millions of genealogical common ancestors […] at least thousands of distinct individuals." | OK |

## Notas de verificación

- **DOIs**: los 5 con DOI (Chang 1999, Rohde-Olson-Chang 2004, Ralph-Coop 2013,
  Gómez 2016, Fenner 2005) resuelven correctamente en Crossref con título, año y
  revista coincidentes.
- **Robustez frente a parámetros**: la conclusión es estable para
  `p ∈ [10⁻⁴, 0.15]` (ver Tablas 1–3 y Fig. 3 del paper), por lo que el valor
  exacto de `p` no es crítico.
- **Fuentes sin DOI** (PRB, OWID, preprint de Rohde 2003) son públicas y citables;
  se identifican por URL/repositorio.
- **No se ha inventado ninguna cifra**: cada número del paper proviene de una de
  las fuentes anteriores o se deriva de ellas mediante el código en `code/`.
