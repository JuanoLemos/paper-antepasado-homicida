# Sobre la inevitabilidad de un antepasado homicida

*Paper y código reproducible: por qué es prácticamente imposible no tener un
antepasado homicida. Argumento genealógico-probabilístico (colapso de pedigrí +
punto de ancestros idénticos) con simulación Monte Carlo.*

[![DOI](https://zenodo.org/badge/1277539649.svg)](https://doi.org/10.5281/zenodo.20806914)

**Idiomas:** Español · [English](README.en.md)

Preprint (estilo arXiv) que formaliza y cuantifica la siguiente afirmación:

> Todo ser humano vivo tiene, con probabilidad esencialmente igual a 1, al menos
> un antepasado que causó la muerte de otro ser humano.

El argumento combina dos hechos:

1. **Crecimiento exponencial de antepasados** y **colapso de pedigrí**: el número
   de antepasados genealógicos crece como `2^n` por generación hasta saturar la
   población reproductora de cada época.
2. **Punto de ancestros idénticos (IAP)**: pasado cierto horizonte (~5.000–7.000
   años; Rohde, Olson & Chang, 2004), el conjunto de antepasados de cualquier
   persona viva coincide con *toda* la población reproductora global de entonces.
   Basta un solo homicida en ese acervo para que sea ancestro de todos.

Además se analizan **poblaciones aisladas** (islas, fundaciones por pocos
colonos): el efecto fundador adelanta el IAP (`~1.77·log₂(N_e)` generaciones) y
se muestra por qué el aislamiento no es una vía de escape a la tesis. También se
verifica la **robustez al supuesto de independencia**: introduciendo
heredabilidad/correlación `h` de la violencia (preservando la prevalencia
marginal), la conclusión se mantiene (apenas retrasa una generación).

## Estructura

```
paper/        Documento LaTeX (main.tex) y bibliografía (refs.bib)
  figures/    Figuras generadas por code/figures.py
code/         Modelo, figuras y simulación en Python
  model.py    Fórmulas núcleo (modelo ingenuo, colapso, IAP)
  figures.py  Genera las figuras del paper
  simulate.py Simulación Monte Carlo de ascendencia + homicidio
  results.py  Tablas y números reportados en el paper
  output/     CSVs de resultados (generado)
```

## Reproducir

```powershell
# 1. Dependencias Python
pip install -r code/requirements.txt

# 2. Generar resultados y figuras
python code/results.py
python code/figures.py
python code/simulate.py

# 3. Compilar el PDF (requiere Tectonic)
tectonic paper/main.tex
```

## Definiciones clave

- **Asesino / homicida**: cualquier persona que causó la muerte de otro ser
  humano (incluye guerra, defensa propia, etc.). Definición amplia y deliberada,
  que maximiza la robustez del resultado.
- **Antepasado**: ancestro *genealógico* (lineal), no genético.

## Licencias

- **Código** (`code/`): MIT — ver `LICENSE`.
- **Paper, figuras y datos** (`paper/`): CC-BY-4.0 — ver `paper/LICENSE-CC-BY-4.0.txt`.

## Cómo citar

Metadatos de cita en `CITATION.cff`. Cita sugerida:

> Juan Manuel Lemos (2026), *Sobre la inevitabilidad de un antepasado homicida:
> un argumento genealógico-probabilístico*. Zenodo. CC-BY-4.0.
> DOI: [10.5281/zenodo.20806914](https://doi.org/10.5281/zenodo.20806914)

## Disponibilidad de datos y código

Todo el código, datos derivados y fuentes están en este repositorio. La
trazabilidad de cada afirmación a su fuente primaria (con DOI y cita textual) se
documenta en `EVIDENCE.md`.

## Publicar en Zenodo (Fase C, requiere tu cuenta)

```powershell
# 1. Crear el repo en GitHub (con gh, o manualmente en github.com)
#    gh repo create JuanoLemos/paper-antepasado-homicida --public --source . --push

# 2. En zenodo.org: iniciar sesión con GitHub y activar el repo
#    (Settings -> GitHub -> flip ON para este repositorio).

# 3. Crear un GitHub Release (tag v1.0.0).
#    Zenodo detecta el release y emite el DOI automáticamente.

# 4. Completar los placeholders TODO(Fase C) con la URL/DOI definitivos en:
#    CITATION.cff, .zenodo.json y paper/main.tex
```

## Estado

- [x] Andamiaje
- [x] Modelo y figuras
- [x] Simulación
- [x] Paper en español
- [x] Verificación de fuentes (ver `EVIDENCE.md`)
- [x] Empaquetado para publicación (licencias, `CITATION.cff`, `.zenodo.json`)
- [x] Depósito en Zenodo + DOI: [10.5281/zenodo.20806914](https://doi.org/10.5281/zenodo.20806914)
- [x] Traducción al inglés (`paper/main-en.tex`, ver [README.en.md](README.en.md))
