# Rubrica de Responsabilidades - Diego (Q1-Q2)

**Fecha de actualizacion:** 2026-02-11  
**Alcance evaluado:** responsabilidades de Diego en Fase 1 y Fase 2 (Q1-Q2), con base en evidencia local del repositorio.

## Criterios y evaluacion (estado actual)

| Criterio | Peso referencial | Evidencia | Estado | Puntaje |
|---|---:|---|---|---:|
| 1) Limpieza y consolidacion base de datos | 15 | `Lab 1/scripts/data_cleaning.py`, `Lab 1/scripts/build_q1_q2_clean.py`, `Lab 1/data/processed/*_clean_2009_2022.csv` | **Cumplido alto** para alcance Q1-Q2 (2009-2022). | 14/15 |
| 2) Descripcion de datos (variables, observaciones, tipos) | 10 | `Lab 1/notebooks/02_analisis_descriptivo.ipynb`, `Lab 1/docs/diccionario_datos.md`, `Lab 1/output/tables/03_estadisticas_descriptivas.csv` | **Cumplido**. | 10/10 |
| 3) Estadistica descriptiva, normalidad y frecuencias | 15 | `Lab 1/output/tables/04_stats_*.csv`, `05_tests_normalidad.csv`, `06_analisis_distribuciones.csv`, `07_freq_*.csv` | **Cumplido**. | 15/15 |
| 4) Q1 implementado y validado (tendencia mortalidad infantil) | 20 | `Lab 1/notebooks/03_hipotesis.ipynb`, `Lab 1/output/tables/q1_mortalidad_infantil_anual_2009_2022.csv`, `Lab 1/output/figures/q1_tendencia_mortalidad_infantil_2009_2022.png` | **Cumplido**. Serie anual 2009-2022 y cierre interpretativo en notebook. | 19/20 |
| 5) Q2 implementado y validado (disparidad geografica) | 20 | `Lab 1/notebooks/03_hipotesis.ipynb` (celdas Q2 de calculo, visualizacion y cierre) | **Cumplido**. Top 3 mejor/peor, brecha y robustez 2010-2022. | 19/20 |
| 6) Documentacion metodologica de hallazgos Q1-Q2 | 10 | `Lab 1/notebooks/03_hipotesis.ipynb` (`### Cierre Q1`, `### Cierre Q2`) | **Cumplido en notebook**. | 9/10 |
| 7) Reproducibilidad tecnica (dependencias y rutas) | 5 | `Lab 1/requirements.txt`, rutas relativas de notebook y scripts | **Cumplido**. | 5/5 |
| 8) Coherencia con lineamientos del curso en tu alcance | 5 | Q1-Q2 implementados y defendibles en periodo oficial 2009-2022 | **Parcial alto**. Pendiente integracion final al documento formal del curso. | 4/5 |

### Resultado global (alcance Diego)
- **Puntaje actual estimado:** **95/100**
- **Estado:** **Q1-Q2 tecnicamente completado**

## Evidencia de cobertura (Si / No)

| Entregable de tu parte | Evidencia | Cobertura |
|---|---|---|
| Consolidacion y datasets clean para Q1-Q2 | `Lab 1/data/processed/nacimientos_clean_2009_2022.csv`, `Lab 1/data/processed/defunciones_clean_2009_2022.csv` | Si |
| Analisis descriptivo completo Fase 1 | `Lab 1/output/tables/*.csv`, `Lab 1/output/figures/*.png` | Si |
| Q1 ejecutable y robusto | `Lab 1/notebooks/03_hipotesis.ipynb`, `Lab 1/output/tables/q1_mortalidad_infantil_anual_2009_2022.csv` | Si |
| Q2 completo (analisis + visual + interpretacion) | `Lab 1/notebooks/03_hipotesis.ipynb` | Si |
| Hallazgos narrativos Q1-Q2 en notebook | `Lab 1/notebooks/03_hipotesis.ipynb` | Si |

## Pendientes fuera de este cierre tecnico
1. Pasar la redaccion formal (situacion problematica, problema cientifico y objetivos) al documento externo del curso.
2. Integrar Q1-Q2 con el trabajo de Roberto (Q3-Q5 y clustering) en el informe final de equipo.
3. Verificar consistencia final entre Google Docs, PDF final y repositorio.

## Nota
Esta rubrica evalua el alcance de Diego (Q1-Q2).  
No reemplaza la evaluacion integral del proyecto de equipo.
