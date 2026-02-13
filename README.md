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
│   ├── csv/                               # Datos crudos (2009-2022)
│   ├── processed/                         # Datasets limpios
│   └── sav/                               # Archivos SPSS originales
├── notebooks/
│   ├── 01_exploracion_inicial.ipynb       # Consolidación y master_dataset
│   ├── 02_analisis_descriptivo.ipynb      # Estadística descriptiva
│   └── 03_hipotesis.ipynb                 # Q1-Q5 + clustering
├── scripts/
│   ├── build_q1_q2_clean.py              # Pipeline de limpieza reproducible
│   ├── data_cleaning.py                   # Funciones auxiliares de limpieza
│   └── convertir_sav_xlsx_a_csv.py       # Conversión SAV → CSV
└── output/
    ├── figures/                           # 60+ visualizaciones (PNG)
    └── tables/                            # 30 tablas de resultados (CSV)
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
- **Informe formal:** `Lab 1/docs/informe_analisis_exploratorio.md`
- **Figuras:** `Lab 1/output/figures/` (60+ gráficos: heatmaps, histogramas, Q-Q, barras, dispersión)
- **Tablas:** `Lab 1/output/tables/` (30 CSVs: estadísticas descriptivas, normalidad, Q1-Q5)
- **Dataset consolidado:** `Lab 1/data/processed/master_dataset.csv` (local, no versionado)
- **Datasets clean:** `Lab 1/data/processed/nacimientos_clean_2009_2022.csv`, `defunciones_clean_2009_2022.csv`

## Preguntas de Investigación
| # | Pregunta | Responsable | Resultado |
|---|---|---|---|
| Q1 | Tendencia de mortalidad infantil 2009-2022 | Diego | Tendencia creciente (R²=0.723), hipótesis de mejora **rechazada** |
| Q2 | Disparidades geográficas entre departamentos | Diego | Brecha 10.4× entre Guatemala y Zacapa, **confirmada** |
| Q3 | Patrones estacionales intraanuales | Roberto | Julio es mes más crítico (1.07×1,000), **confirmada** |
| Q4 | Variación por variables demográficas | Roberto | Sobremortalidad masculina +23.4%, efecto urbano 5.7×, **confirmada** |
| Q5 | Clustering departamental | Roberto | k=2, silueta=0.469: "Baja tasa estable" (18) vs "Intermedia con oscilación" (4) |

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
