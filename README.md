# Sobre la inevitabilidad de un antepasado homicida

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
> un argumento genealógico-probabilístico*. CC-BY-4.0.

(El DOI definitivo se añadirá tras el depósito en Zenodo.)

## Disponibilidad de datos y código

Todo el código, datos derivados y fuentes están en este repositorio. La
trazabilidad de cada afirmación a su fuente primaria (con DOI y cita textual) se
documenta en `EVIDENCE.md`.

## Publicar en Zenodo (Fase C, requiere tu cuenta)

```powershell
# 1. Crear el repo en GitHub (con gh, o manualmente en github.com)
#    gh repo create JuanoLemos/paper-antepasado-asesino --public --source . --push

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
- [ ] Depósito en Zenodo + DOI (Fase C)
- [ ] Traducción al inglés
