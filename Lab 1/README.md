# Análisis Exploratorio de Datos - Lab 1
## Estadísticas Vitales Guatemala (INE)

**Curso:** Minería de Datos CC3074  
**Sección:** 20  
**Estudiante:** Diego López - 23747  
**Año:** 2026

---

## Descripción del Proyecto

Análisis exploratorio de datos de estadísticas vitales de Guatemala (2009-2022) proporcionados por el Instituto Nacional de Estadística (INE). 

**Dataset consolidado:**
- 📊 Total registros: 7,295,381
- 📋 Total columnas: 95
- 📁 Tamaño master_dataset.csv: 1.7 GB
- ⏱️ Años procesados: 2009-2022 (14 años)

**Tipos de datos (5):**
- 🔹 Nacimientos (~5.1M)
- 🔹 Defunciones (~1M)
- 🔹 Matrimonios (~997K)
- 🔹 Divorcios (~78K)
- 🔹 Defunciones Fetales (~38K)

---

## Estructura del Proyecto

```
Lab 1/
├── docs/                    # Documentación del proyecto
├── data/
│   ├── raw/                 # Datos originales (NO MODIFICAR)
│   ├── processed/           # Datos limpios y normalizados
│   └── interim/             # Datos intermedios
├── notebooks/               # Jupyter Notebooks del análisis
├── scripts/                 # Código Python reutilizable
├── output/                  # Resultados (gráficas, tablas, reportes)
└── tests/                   # Tests unitarios
```

---

## Instalación

```bash
# Crear ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## Uso

### 1. Cargar y limpiar datos

```python
from scripts.data_cleaning import consolidar_todos_tipos
from pathlib import Path

# Cargar los 5 tipos de datos normalizados
tipos = ['defunciones', 'defunciones_fetales', 'divorcios', 'matrimonios', 'nacimientos']
csv_dir = Path("data/raw/csv")

dfs_por_tipo, master = consolidar_todos_tipos(
    tipos_lista=tipos,
    años_rango=(2009, 2023),
    csv_dir=csv_dir
)
```

### 2. Ejecutar análisis

Los notebooks están numerados en orden lógico:

1. `01_exploracion_inicial.ipynb` - Exploración inicial y detección de problemas
2. `02_limpieza_datos.ipynb` - Proceso de limpieza documentado
3. `03_analisis_preguntas.ipynb` - Respuestas a preguntas de investigación
4. `04_visualizaciones.ipynb` - Gráficas finales para informe

---

## Preguntas de Investigación

1. ¿Cómo ha evolucionado la vacunación infantil en Guatemala (2009-2022)?
2. ¿Cuál es la tendencia de mortalidad infantil por departamento?
3. ¿Qué factores están asociados con bajo peso al nacer?
4. ¿Cómo se distribuyen las defunciones por edad y sexo?
5. ¿Existen patrones estacionales en nacimientos y defunciones?

---

## Datos

**Fuente:** Instituto Nacional de Estadística (INE) - Guatemala  
**Periodo:** 2009-2022 (14 años)  
**Total registros:** ~1,000,000+ eventos vitales  

**Tipos de datos:**
- 70 archivos CSV (5 tipos × 14 años)
- Columnas normalizadas a lowercase
- Valores nulos documentados

---

## Tecnologías

- Python 3.13
- pandas (manipulación de datos)
- matplotlib/seaborn (visualización)
- jupyter (notebooks interactivos)

---

## Resultados

Los resultados generados se encuentran en:
- `output/figures/` - Gráficas en formato PNG/SVG
- `output/tables/` - Tablas resumen en CSV
- `output/reports/` - Reportes en Markdown

---

## 💾 Gestión de Archivos Grandes en Git

**IMPORTANTE:** Los archivos grandes NO están incluidos en el repositorio.

### Archivos ignorados (especificados en `.gitignore`):

| Ruta | Tamaño | Razón |
|------|--------|-------|
| `data/raw/csv/*.csv` | ~4-5 GB | Datos crudos del INE |
| `data/processed/master_dataset.csv` | 1.7 GB | Dataset consolidado |
| `output/figures/*.png` | ~100 MB | Gráficas generadas |

**Resultado:** Repositorio en GitHub = ~200 KB (vs 6+ GB localmente)

### Cómo regenerar datos localmente

```bash
# 1. Descargar CSVs desde INE (manual)
# Colocar en: data/raw/csv/

# 2. Ejecutar notebook
jupyter notebook notebooks/01_exploracion_inicial.ipynb

# Genera automáticamente:
# - data/processed/master_dataset.csv
```

---

## Licencia

Este proyecto es con fines académicos para el curso de Minería de Datos de la Universidad del Valle de Guatemala.
