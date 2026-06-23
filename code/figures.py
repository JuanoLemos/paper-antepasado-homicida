"""Genera las figuras del paper en paper/figures/ (PDF vectorial).

Bilingue: genera cada figura en espanol (sufijo "") e ingles (sufijo "_en").
"""

from __future__ import annotations

import os
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import model
import population
import simulate

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.normpath(os.path.join(HERE, "..", "paper", "figures"))

P_VALUES: List[float] = [0.001, 0.01, 0.05, 0.15]

LANGS = {"es": "", "en": "_en"}

L: Dict[str, Dict[str, str]] = {
    "es": {
        "gen_back_N": "Generaciones hacia atras (N)",
        "gen_back_n": "Generaciones hacia atras (n)",
        "generations": "Generaciones",
        "p_no_killer": "P(ningun antepasado homicida)",
        "naive_title": "Colapso exponencial (modelo ingenuo)",
        "prob_individual": "prob. individual",
        "slots": "casillas ingenuas $2^n$",
        "world_pop": "poblacion mundial (aprox.)",
        "distinct": "antepasados distintos",
        "n_people": "Numero de personas",
        "pedigree_title": "Colapso de pedigri",
        "cbar": r"$\log_{10} P(\mathrm{ningun\ homicida})$",
        "p_xlabel": "p (prob. individual de ser homicida)",
        "heat_title": "Sensibilidad de P a (p, N)",
        "Ne_xlabel": "Tamano efectivo de la poblacion $N_e$",
        "iap_gen_ylabel": "Generaciones hasta el IAP",
        "iap_title": r"IAP $\approx 1.77\,\log_2 N_e$ (Chang 1999)",
        "gen_annot": "gen",
        "frac_killer": "Fraccion con antepasado homicida",
        "founder_title": "Efecto fundador (p = {p})",
        "island_size": "tamano isla",
        "herit_title": "Robustez a la independencia (p = {p})",
        "heritability": "heredabilidad",
    },
    "en": {
        "gen_back_N": "Generations back (N)",
        "gen_back_n": "Generations back (n)",
        "generations": "Generations",
        "p_no_killer": "P(no homicidal ancestor)",
        "naive_title": "Exponential collapse (naive model)",
        "prob_individual": "individual prob.",
        "slots": "naive slots $2^n$",
        "world_pop": "world population (approx.)",
        "distinct": "distinct ancestors",
        "n_people": "Number of people",
        "pedigree_title": "Pedigree collapse",
        "cbar": r"$\log_{10} P(\mathrm{no\ homicide})$",
        "p_xlabel": "p (individual prob. of being a killer)",
        "heat_title": "Sensitivity of P to (p, N)",
        "Ne_xlabel": "Effective population size $N_e$",
        "iap_gen_ylabel": "Generations to the IAP",
        "iap_title": r"IAP $\approx 1.77\,\log_2 N_e$ (Chang 1999)",
        "gen_annot": "gen",
        "frac_killer": "Fraction with a homicidal ancestor",
        "founder_title": "Founder effect (p = {p})",
        "island_size": "island size",
        "herit_title": "Robustness to independence (p = {p})",
        "heritability": "heritability",
    },
}


def ensure_dir() -> None:
    os.makedirs(FIGDIR, exist_ok=True)


def _save(fig, name: str, suffix: str) -> None:
    fig.savefig(os.path.join(FIGDIR, f"{name}{suffix}.pdf"))
    plt.close(fig)


def fig_naive_collapse(lang: str, suffix: str) -> None:
    t = L[lang]
    Ns = list(range(0, 26))
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for p in P_VALUES:
        ys = [model.prob_no_killer_naive(p, N) for N in Ns]
        ys = [max(y, 1e-300) for y in ys]
        ax.plot(Ns, ys, marker="o", markersize=3, label=f"p = {p}")
    ax.set_yscale("log")
    ax.set_ylim(1e-50, 2.0)
    ax.set_xlabel(t["gen_back_N"])
    ax.set_ylabel(t["p_no_killer"])
    ax.set_title(t["naive_title"])
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(title=t["prob_individual"])
    fig.tight_layout()
    _save(fig, "fig_naive_collapse", suffix)


def fig_pedigree_collapse(lang: str, suffix: str) -> None:
    t = L[lang]
    ns = list(range(0, 41))
    slots = [float(2 ** n) for n in ns]
    pops = [population.world_population_gen(n) for n in ns]
    distinct = [min(s, p) for s, p in zip(slots, pops)]
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot(ns, slots, "--", label=t["slots"])
    ax.plot(ns, pops, ":", label=t["world_pop"])
    ax.plot(ns, distinct, "-", linewidth=2.2, label=t["distinct"])
    ax.set_yscale("log")
    ax.set_xlabel(t["gen_back_n"])
    ax.set_ylabel(t["n_people"])
    ax.set_title(t["pedigree_title"])
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    _save(fig, "fig_pedigree_collapse", suffix)


def fig_sensitivity_heatmap(lang: str, suffix: str) -> None:
    t = L[lang]
    ps = np.linspace(0.0005, 0.05, 120)
    Ns = np.arange(1, 26)
    Z = np.zeros((len(Ns), len(ps)))
    for i, N in enumerate(Ns):
        ind = model.total_individuals_naive(int(N))
        for j, p in enumerate(ps):
            logp = model.log_prob_no_killer(float(p), ind) / np.log(10.0)
            Z[i, j] = max(logp, -300.0)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    mesh = ax.pcolormesh(ps, Ns, Z, shading="auto", cmap="viridis")
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label(t["cbar"])
    ax.set_xlabel(t["p_xlabel"])
    ax.set_ylabel(t["gen_back_N"])
    ax.set_title(t["heat_title"])
    fig.tight_layout()
    _save(fig, "fig_sensitivity_heatmap", suffix)


def fig_isolation(lang: str, suffix: str) -> None:
    t = L[lang]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.0))

    Ne = np.logspace(1, 7, 200)
    iap = [model.chang_iap_generations(float(n)) for n in Ne]
    ax1.plot(Ne, iap, "-", linewidth=2.0)
    ax1.set_xscale("log")
    ax1.set_xlabel(t["Ne_xlabel"])
    ax1.set_ylabel(t["iap_gen_ylabel"])
    ax1.set_title(t["iap_title"])
    ax1.grid(True, which="both", alpha=0.3)
    for n in (50, 1000, 1_000_000):
        g = model.chang_iap_generations(float(n))
        ax1.annotate(f"$N_e$={n:,}\n~{g:.0f} {t['gen_annot']}", xy=(n, g),
                     xytext=(n, g + 4), fontsize=7, ha="center",
                     arrowprops=dict(arrowstyle="->", lw=0.6))

    G = 22
    p = 0.01
    for M in (50, 200, 5000):
        frac = simulate.run_average(p, M, G, reps=30, base_seed=2024)
        ax2.plot(range(G), frac, marker="o", markersize=3, label=f"M = {M}")
    ax2.set_xlabel(t["generations"])
    ax2.set_ylabel(t["frac_killer"])
    ax2.set_title(t["founder_title"].format(p=p))
    ax2.grid(True, alpha=0.3)
    ax2.legend(title=t["island_size"])

    fig.tight_layout()
    _save(fig, "fig_isolation", suffix)


def fig_heritability(lang: str, suffix: str) -> None:
    t = L[lang]
    G = 30
    p = 0.01
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for h in (0.0, 0.3, 0.6, 0.9):
        frac, _ = simulate.run_average_heritable(p, h, M=2000, G=G, reps=40,
                                                  base_seed=777)
        ax.plot(range(G), frac, marker="o", markersize=3, label=f"h = {h}")
    ax.set_xlabel(t["generations"])
    ax.set_ylabel(t["frac_killer"])
    ax.set_title(t["herit_title"].format(p=p))
    ax.grid(True, alpha=0.3)
    ax.legend(title=t["heritability"])
    fig.tight_layout()
    _save(fig, "fig_heritability", suffix)


def main() -> None:
    ensure_dir()
    for lang, suffix in LANGS.items():
        fig_naive_collapse(lang, suffix)
        fig_pedigree_collapse(lang, suffix)
        fig_sensitivity_heatmap(lang, suffix)
        fig_isolation(lang, suffix)
        fig_heritability(lang, suffix)
    print(f"Figuras (es/en) escritas en {FIGDIR}")


if __name__ == "__main__":
    main()
