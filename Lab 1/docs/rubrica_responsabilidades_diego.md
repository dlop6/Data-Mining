# Rubrica de Responsabilidades - Diego (Q1-Q2)

**Fecha de evaluacion:** 2026-02-10  
**Alcance evaluado:** responsabilidades de Diego en Fase 1 y Fase 2 (Q1-Q2), con base en evidencia del repositorio local.

## Criterios y Evaluacion

| Criterio | Peso referencial | Evidencia | Estado | Puntaje |
|---|---:|---|---|---:|
| 1) Limpieza y consolidacion base de datos | 15 | `Lab 1/scripts/data_cleaning.py`, `Lab 1/notebooks/01_exploracion_inicial.ipynb`, `Lab 1/data/processed/master_dataset.csv` | **Parcial alto**. Existe consolidacion y dataset maestro, pero hay limitaciones de fuente 2023-2024 y una celda con crash historico en notebook 01. | 12/15 |
| 2) Descripcion de datos (variables, observaciones, tipos) | 10 | `Lab 1/notebooks/02_analisis_descriptivo.ipynb`, `Lab 1/output/tables/03_estadisticas_descriptivas.csv`, `Lab 1/docs/diccionario_datos.md` | **Cumplido** para 2009-2022. | 10/10 |
| 3) Estadistica descriptiva, normalidad y frecuencias | 15 | `Lab 1/output/tables/04_stats_*.csv`, `05_tests_normalidad.csv`, `06_analisis_distribuciones.csv`, `07_freq_*.csv` | **Cumplido**. Hay evidencia tabular y graficas de soporte. | 15/15 |
| 4) Q1 implementado y validado (tendencia mortalidad infantil) | 20 | `Lab 1/notebooks/03_hipotesis.ipynb`, `Lab 1/data/processed/q1_mortalidad_infantil_anual.csv`, `Lab 1/output/figures/q1_tendencia_mortalidad_infantil.png` | **Parcial**. Implementacion existe, pero resultado actual en CSV tiene 1 fila y requiere correccion de filtros `tipo` y criterio temporal. | 9/20 |
| 5) Q2 implementado y validado (disparidad geografica) | 20 | `Lab 1/notebooks/03_hipotesis.ipynb` | **No cubierto**. Solo esta el encabezado de Q2; faltan analisis, tabla, grafica e interpretacion. | 0/20 |
| 6) Documentacion metodologica de hallazgos Q1-Q2 | 10 | `Lab 1/notebooks/03_hipotesis.ipynb`, `README.md` | **Parcial bajo**. Falta cerrar markdown de hallazgos y conclusion de hipotesis Q1/Q2. | 4/10 |
| 7) Reproducibilidad tecnica (dependencias y rutas) | 5 | `Lab 1/requirements.txt`, `README.md` | **Cumplido** tras actualizar dependencias (`scipy`, `pyreadstat`) y rutas reales en README. | 5/5 |
| 8) Coherencia con lineamientos del curso en tu alcance | 5 | `README.md`, `Lab 1/docs/Proyecto. Análisis Exploratorio. 2026.docx` | **Parcial alto**. Se alinea el periodo oficial 2009-2022; faltan Q2 completo y texto final de validacion/refutacion. | 4/5 |

### Resultado global (tu alcance)
- **Puntaje actual:** **59/100**
- **Estado:** **En progreso** (base fuerte en Fase 1, Fase 2 incompleta por Q2 y cierre de Q1)

## Evidencia de Cobertura (Si / No)

| Entregable de tu parte | Evidencia | Cobertura |
|---|---|---|
| Consolidacion y dataset maestro | `Lab 1/data/processed/master_dataset.csv` | Si |
| Analisis descriptivo completo Fase 1 | `Lab 1/output/tables/*.csv`, `Lab 1/output/figures/*.png` | Si |
| Q1 ejecutable y robusto | `Lab 1/notebooks/03_hipotesis.ipynb` + `q1_mortalidad_infantil_anual.csv` | No (parcial) |
| Q2 completo (analisis + visual + interpretacion) | `Lab 1/notebooks/03_hipotesis.ipynb` | No |
| Hallazgos narrativos Q1-Q2 listos para informe | markdown en notebook 03 | No (parcial) |

## Brechas Prioritarias para cerrar
1. Corregir filtros de `tipo` en Q1 (`defunciones` / `nacimientos`, no singular).
2. Cerrar criterio temporal oficial 2009-2022 para Q1-Q2 y documentarlo en notebook.
3. Reejecutar Q1 y validar salida multianual (no una sola fila).
4. Implementar Q2 completo por `depreg` con top 3 mejor/peor.
5. Escribir interpretaciones finales Q1 y Q2 en markdown para el informe.

## Nota
Esta rubrica evalua solo el alcance de Diego.  
Las tareas de Q3-Q5 y clustering corresponden a Roberto y deben integrarse al entregable final del equipo.

---

## Rubrica V2 (alineada puntualmente a la guia oficial)

**Objetivo de esta V2:** mantener los **6 bloques oficiales** de evaluacion del curso y medirlos dentro del alcance de Diego (Q1-Q2), sin perder visibilidad de riesgos de equipo.

### 1) Matriz oficial -> alcance Diego

| Bloque oficial (guia) | Peso oficial | Alcance de Diego (Q1-Q2) | Evidencia local actual | Estado Diego |
|---|---:|---|---|---|
| Situacion problematica | 10 | Redaccion del contexto de mortalidad infantil y justificacion del analisis Q1-Q2. | `Lab 1/notebooks/03_hipotesis.ipynb` (hipotesis), README general | Parcial |
| Problema cientifico | 10 | Formular problema medible para Q1-Q2 (tendencia + disparidad geografica). | Hipotesis en notebook 03, sin enunciado formal final | Parcial |
| Objetivos (1 general + 2 especificos) | 10 | Objetivos para responder Q1 y Q2 con criterios verificables. | Hay enfoque implicito, falta seccion formal de objetivos | Parcial |
| Descripcion de datos (incluye limpieza) | 15 | Describir fuentes 2009-2022, variables clave y decisiones de limpieza para Q1-Q2. | `Lab 1/notebooks/01_exploracion_inicial.ipynb`, `Lab 1/notebooks/02_analisis_descriptivo.ipynb`, `Lab 1/docs/diccionario_datos.md` | Parcial alto |
| Analisis exploratorio | 35 | Estadistica descriptiva y validacion/refutacion de Q1-Q2 con tablas y graficas. | Fase 1 fuerte en `output/tables` y `output/figures`; Q1 parcial; Q2 pendiente | Parcial |
| Hallazgos y conclusiones | 20 | Sintesis de hallazgos Q1-Q2, conclusion y siguientes pasos en informe. | Falta cierre narrativo final en notebook 03 e informe | Parcial bajo |

### 2) Evaluacion V2 (solo alcance Diego)

| Bloque oficial | Peso oficial | Puntaje actual (Diego) | Justificacion breve |
|---|---:|---:|---|
| Situacion problematica | 10 | 6 | Existe marco tematico, pero falta redaccion final compacta para informe. |
| Problema cientifico | 10 | 5 | Hipotesis definidas, pero no hay enunciado formal consolidado y validable en texto final. |
| Objetivos | 10 | 6 | Hay direccion analitica, faltan objetivos explicitos (general y especificos). |
| Descripcion de datos | 15 | 13 | Muy buena evidencia de estructura/calidad/EDA; falta cerrar limpieza especifica de Q1-Q2 en una seccion unica. |
| Analisis exploratorio | 35 | 19 | Fase 1 cubierta; Q1 necesita correccion metodologica final; Q2 aun no implementado. |
| Hallazgos y conclusiones | 20 | 7 | Falta redactar resultados finales Q1-Q2 y su decision de hipotesis (confirmada/rechazada). |

### Resultado V2 (alcance Diego)
- **Puntaje actual:** **56/100**
- **Lectura:** base tecnica fuerte, pero la nota cae por cierre incompleto de Fase 2 (Q1 final + Q2 completo + redaccion formal).

### 3) Riesgos de equipo frente a la guia (fuera de alcance directo de Diego)

| Requisito oficial | Dependencia principal | Riesgo actual |
|---|---|---|
| Clustering + silueta + interpretacion de grupos | Roberto | Alto si no se integra a tiempo al informe conjunto |
| Sintesis integrada Q1-Q5 + conclusiones finales de equipo | Ambos | Medio-Alto |
| Coherencia final entre informe, notebooks y repositorio | Ambos | Medio |

### 4) Cierre minimo para subir nota de Diego
1. Corregir y reejecutar Q1 con criterio temporal 2009-2022 y filtros `tipo` correctos.
2. Implementar Q2 completo (tabla, visualizacion, interpretacion, top 3 mejores/peores).
3. Redactar en notebook 03: situacion problematica, problema cientifico, objetivos, hallazgos y conclusion Q1-Q2.
4. Transferir esos resultados al Google Docs y PDF final.
