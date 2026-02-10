# Proyecto de Analisis Exploratorio de Datos
## Estadisticas Vitales Guatemala (INE)

**Curso:** CC3074 - Mineria de Datos  
**Universidad:** Universidad del Valle de Guatemala  
**Semestre:** II - 2026  
**Fuente principal:** Instituto Nacional de Estadistica (INE), Guatemala

## Objetivo
Este repositorio documenta el trabajo de analisis exploratorio sobre estadisticas vitales de Guatemala, con enfoque en:
- limpieza y consolidacion de datos crudos;
- analisis descriptivo y formulacion de hipotesis;
- validacion/refutacion de preguntas de investigacion con tablas y graficas;
- preparacion de evidencia para informe academico.

## Alcance Temporal Oficial
Para el proyecto se usa **2009-2022** como periodo oficial.

Nota de calidad de fuente (snapshot local):
- los archivos `2023_*.csv` en `Lab 1/data/raw/csv/` corresponden a tablas resumen (`CONTENIDO`) y no microdato;
- los archivos `2024_*.csv` en `Lab 1/data/raw/csv/` estan vacios;
- por consistencia metodologica y trazabilidad se reporta 2009-2022.

## Estructura Real del Repositorio
```text
Lab 1/
├── config.py
├── requirements.txt
├── docs/
├── data/
│   ├── raw/csv/
│   ├── processed/
│   ├── interim/
│   └── sav/
├── notebooks/
│   ├── 01_exploracion_inicial.ipynb
│   ├── 02_analisis_descriptivo.ipynb
│   └── 03_hipotesis.ipynb
├── scripts/
│   ├── data_cleaning.py
│   └── convertir_sav_xlsx_a_csv.py
└── output/
    ├── figures/
    ├── tables/
    └── reports/
```

## Flujo de Trabajo
1. **Exploracion y consolidacion**: `Lab 1/notebooks/01_exploracion_inicial.ipynb`
2. **Analisis descriptivo**: `Lab 1/notebooks/02_analisis_descriptivo.ipynb`
3. **Hipotesis de investigacion**: `Lab 1/notebooks/03_hipotesis.ipynb`

## Variables y Tipos de Evento
En `master_dataset.csv` la columna `tipo` usa estos valores:
- `nacimientos`
- `defunciones`
- `matrimonios`
- `divorcios`
- `defunciones_fetales`

## Requisitos
Instalacion recomendada:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\\Scripts\\activate   # Windows
pip install -r "Lab 1/requirements.txt"
```

## Artefactos Generados
- Figuras: `Lab 1/output/figures/`
- Tablas: `Lab 1/output/tables/`
- Dataset consolidado: `Lab 1/data/processed/master_dataset.csv` (local, no versionado)

## Colaboracion (Resumen)
- **Diego:** Fase 1 + Preguntas Q1-Q2
- **Roberto:** Preguntas Q3-Q5 + clustering + sintesis

## Entregables Academicos
Segun la guia del curso:
- informe en Google Docs (con historial de cambios);
- informe final en PDF (sin codigo);
- script/notebooks usados para responder preguntas;
- enlace al repositorio.

## Nota
El proyecto mantiene archivos pesados fuera de Git mediante `.gitignore`.  
Este repositorio prioriza trazabilidad metodologica y evidencia reproducible del analisis.
