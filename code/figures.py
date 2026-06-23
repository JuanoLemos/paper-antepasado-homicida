"""Genera las figuras del paper en paper/figures/ (PDF vectorial)."""

from __future__ import annotations

import os
from typing import List

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


def ensure_dir() -> None:
    os.makedirs(FIGDIR, exist_ok=True)


def fig_naive_collapse() -> None:
    Ns = list(range(0, 26))
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for p in P_VALUES:
        ys = [model.prob_no_killer_naive(p, N) for N in Ns]
        ys = [max(y, 1e-300) for y in ys]
        ax.plot(Ns, ys, marker="o", markersize=3, label=f"p = {p}")
    ax.set_yscale("log")
    ax.set_ylim(1e-50, 2.0)
    ax.set_xlabel("Generaciones hacia atras (N)")
    ax.set_ylabel("P(ningun antepasado homicida)")
    ax.set_title("Colapso exponencial (modelo ingenuo)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(title="prob. individual")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_naive_collapse.pdf"))
    plt.close(fig)


def fig_pedigree_collapse() -> None:
    ns = list(range(0, 41))
    slots = [float(2 ** n) for n in ns]
    pops = [population.world_population_gen(n) for n in ns]
    distinct = [min(s, p) for s, p in zip(slots, pops)]
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot(ns, slots, "--", label="casillas ingenuas $2^n$")
    ax.plot(ns, pops, ":", label="poblacion mundial (aprox.)")
    ax.plot(ns, distinct, "-", linewidth=2.2, label="antepasados distintos")
    ax.set_yscale("log")
    ax.set_xlabel("Generaciones hacia atras (n)")
    ax.set_ylabel("Numero de personas")
    ax.set_title("Colapso de pedigri")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_pedigree_collapse.pdf"))
    plt.close(fig)


def fig_sensitivity_heatmap() -> None:
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
    cbar.set_label(r"$\log_{10} P(\mathrm{ningun\ homicida})$")
    ax.set_xlabel("p (prob. individual de ser homicida)")
    ax.set_ylabel("Generaciones hacia atras (N)")
    ax.set_title("Sensibilidad de P a (p, N)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_sensitivity_heatmap.pdf"))
    plt.close(fig)


def fig_isolation() -> None:
    """Poblaciones aisladas: (a) generacion del IAP vs tamano efectivo Ne
    (Chang 1999); (b) fraccion con antepasado homicida vs generacion para
    poblaciones cerradas de distinto tamano M (efecto fundador)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.0))

    Ne = np.logspace(1, 7, 200)
    iap = [model.chang_iap_generations(float(n)) for n in Ne]
    ax1.plot(Ne, iap, "-", linewidth=2.0)
    ax1.set_xscale("log")
    ax1.set_xlabel("Tamano efectivo de la poblacion $N_e$")
    ax1.set_ylabel("Generaciones hasta el IAP")
    ax1.set_title(r"IAP $\approx 1.77\,\log_2 N_e$ (Chang 1999)")
    ax1.grid(True, which="both", alpha=0.3)
    for n in (50, 1000, 1_000_000):
        g = model.chang_iap_generations(float(n))
        ax1.annotate(f"$N_e$={n:,}\n~{g:.0f} gen", xy=(n, g),
                     xytext=(n, g + 4), fontsize=7, ha="center",
                     arrowprops=dict(arrowstyle="->", lw=0.6))

    G = 22
    p = 0.01
    for M in (50, 200, 5000):
        frac = simulate.run_average(p, M, G, reps=30, base_seed=2024)
        ax2.plot(range(G), frac, marker="o", markersize=3, label=f"M = {M}")
    ax2.set_xlabel("Generaciones")
    ax2.set_ylabel("Fraccion con antepasado homicida")
    ax2.set_title(f"Efecto fundador (p = {p})")
    ax2.grid(True, alpha=0.3)
    ax2.legend(title="tamano isla")

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_isolation.pdf"))
    plt.close(fig)


def fig_heritability() -> None:
    """Robustez a la independencia: fraccion con antepasado homicida vs
    generacion para distintos niveles de heredabilidad/correlacion h
    (prevalencia marginal p fija)."""
    G = 30
    p = 0.01
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for h in (0.0, 0.3, 0.6, 0.9):
        frac, _ = simulate.run_average_heritable(p, h, M=2000, G=G, reps=40,
                                                  base_seed=777)
        ax.plot(range(G), frac, marker="o", markersize=3, label=f"h = {h}")
    ax.set_xlabel("Generaciones")
    ax.set_ylabel("Fraccion con antepasado homicida")
    ax.set_title(f"Robustez a la independencia (p = {p})")
    ax.grid(True, alpha=0.3)
    ax.legend(title="heredabilidad")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_heritability.pdf"))
    plt.close(fig)




def main() -> None:
    ensure_dir()
    fig_naive_collapse()
    fig_pedigree_collapse()
    fig_sensitivity_heatmap()
    fig_isolation()
    fig_heritability()
    print(f"Figuras escritas en {FIGDIR}")


if __name__ == "__main__":
    main()
