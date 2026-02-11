# Guia rapida del repo (companero)

## 1) Punto de partida
- Proyecto y rubricas del curso: [`Lab 1/docs/Proyecto.md`](./Proyecto.md)
- Estado operativo de tareas: [`TAREAS.md`](../../TAREAS.md)
- Contexto general del repo: [`README.md`](../../README.md)

## 2) Estructura que si importa para trabajar
- Notebook exploracion inicial: [`Lab 1/notebooks/01_exploracion_inicial.ipynb`](../notebooks/01_exploracion_inicial.ipynb)
- Notebook descriptivo: [`Lab 1/notebooks/02_analisis_descriptivo.ipynb`](../notebooks/02_analisis_descriptivo.ipynb)
- Notebook hipotesis (Q1-Q2 ya implementado): [`Lab 1/notebooks/03_hipotesis.ipynb`](../notebooks/03_hipotesis.ipynb)
- Scripts de preparacion:
  - [`Lab 1/scripts/convertir_sav_xlsx_a_csv.py`](../scripts/convertir_sav_xlsx_a_csv.py)
  - [`Lab 1/scripts/data_cleaning.py`](../scripts/data_cleaning.py)
  - [`Lab 1/scripts/build_q1_q2_clean.py`](../scripts/build_q1_q2_clean.py)
- Datos procesados clave:
  - [`Lab 1/data/processed/nacimientos_clean_2009_2022.csv`](../data/processed/nacimientos_clean_2009_2022.csv)
  - [`Lab 1/data/processed/defunciones_clean_2009_2022.csv`](../data/processed/defunciones_clean_2009_2022.csv)
  - [`Lab 1/data/processed/q1q2_control_calidad_2009_2022.csv`](../data/processed/q1q2_control_calidad_2009_2022.csv)
- Evidencia tabular/figuras:
  - [`Lab 1/output/tables/`](../output/tables)
  - [`Lab 1/output/figures/`](../output/figures)

## 3) Alcance de datos (importante)
- Periodo oficial para analisis: **2009-2022**.
- Para trabajo analitico actual, usar **solo**:
  - `nacimientos_clean_2009_2022.csv`
  - `defunciones_clean_2009_2022.csv`
- En este repo, `build_q1_q2_clean.py` solo genera clean de esos 2 tipos.
- Existen CSV de `matrimonios`, `divorcios` y `defunciones_fetales`, pero no estan en pipeline clean equivalente a Q1-Q2.

## 4) Flujo recomendado para trabajar
1. Crear entorno e instalar dependencias de [`Lab 1/requirements.txt`](../requirements.txt).
2. Abrir y correr notebooks en orden:
   - `01_exploracion_inicial.ipynb`
   - `02_analisis_descriptivo.ipynb`
   - `03_hipotesis.ipynb`
3. Si necesitas regenerar clean Q1-Q2, correr:
   - `python "Lab 1/scripts/build_q1_q2_clean.py"`
4. Validar resultados en:
   - `Lab 1/data/processed/q1q2_control_calidad_2009_2022.csv`
   - `Lab 1/output/tables/q1_mortalidad_infantil_anual_2009_2022.csv`

## 5) Preguntas de investigacion (scope vigente)
- Q1 (Diego): Cual es la tendencia de la mortalidad infantil en Guatemala entre 2009 y 2022.
- Q2 (Diego): Existen disparidades geograficas significativas en mortalidad infantil entre departamentos.
- Q3 (Roberto): Existen patrones temporales intraanuales de mortalidad infantil (por mes y ano) durante 2009-2022.
- Q4 (Roberto): Como varia la mortalidad infantil segun variables demograficas disponibles en nacimientos y defunciones (analisis descriptivo, no causal).
- Q5 (Roberto): Se pueden identificar grupos de departamentos con perfiles similares de mortalidad infantil mediante clustering.

## 6) Estado actual resumido
- Q1 y Q2 estan implementadas en [`Lab 1/notebooks/03_hipotesis.ipynb`](../notebooks/03_hipotesis.ipynb).
- Fase tecnica Q1-Q2: completa.
- Pendiente principal: integracion narrativa final en documento externo (Google Docs/PDF), segun [`TAREAS.md`](../../TAREAS.md).

## 7) Reglas practicas para no romper coherencia
- No mezclar periodo 2009-2022 con 2023/2024 para resultados formales.
- No cambiar definicion operativa de Q1/Q2 sin acordarlo en equipo.
- Si se agregan nuevas preguntas, documentar variables, periodo y criterio de validacion/refutacion.
