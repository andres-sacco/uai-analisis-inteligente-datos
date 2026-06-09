# 📊 Análisis Inteligente de Datos — Siniestros Viales Analytics

Proyecto orientado al procesamiento, análisis y modelado de datos de siniestros viales utilizando Python, Pandas y Docker.

El objetivo principal es construir un pipeline completo de ingeniería de datos capaz de:

* procesar datasets reales de siniestros viales
* limpiar información inconsistente o incompleta
* generar métricas descriptivas de los eventos
* detectar anomalías en variables críticas
* visualizar distribuciones espaciales y temporales
* realizar agregaciones sobre incidentes viales
* aplicar técnicas de Machine Learning no supervisado para segmentación de siniestros

---

# 🚀 Tecnologías Utilizadas

* Python
* Pandas
* Scikit-Learn
* Matplotlib
* Docker
* Docker Compose
* CSV

---

# 📂 Estructura del Proyecto

```text
.
├── data
│   ├── raw
│   ├── processed
│   ├── output
│   ├── graphics
│   └── reports
│
├── docker
│
├── jobs
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── data_quality.py
│   ├── data_visualization.py
│   ├── data_supervised_learning.py
│   └── data_unsupervised_learning.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 📥 Dataset Utilizado

Se utiliza un dataset público de siniestros viales.

## Siniestros Viales Dataset

Dataset con información sobre incidentes de tránsito que incluye características temporales, geográficas y de severidad.

Incluye información sobre:

* siniestros registrados
* cantidad de víctimas
* gravedad del incidente
* ubicación geográfica (latitud / longitud)
* fecha y hora del evento
* tipo de vía
* modo de desplazamiento de la víctima
* contraparte involucrada
* segmentación temporal (día, mes, año, trimestre)

El dataset permite realizar análisis exploratorios, detección de patrones espaciales y temporales, y modelos de clustering para identificar perfiles de siniestros.

---

# 🧠 Objetivos del Proyecto

El pipeline implementa:

* Data Ingestion
* Data Cleaning
* Data Quality Validation
* Data Visualization
* Machine Learning Unsupervised
* Machine Learning Supervised

---

# 🔄 Pipeline de Datos

```text
data_ingestion
      ↓
data_cleaning
      ↓
data_quality
      ↓
data_visualization
      ↓
data_supervised_learning
      ↓
data_unsupervised_learning
```

---

# 🐳 Ejecución con Docker

## Construir containers

```bash
docker compose build
```

## Ejecutar pipeline completo

```bash
docker compose up
```

---

# 📥 Data Ingestion

El pipeline carga automáticamente datasets de siniestros viales.

Los archivos originales se almacenan en:

```text
data/raw
```

---

# 🧹 Data Cleaning

El proceso de limpieza incluye:

* eliminación de registros inválidos o incompletos
* tratamiento de valores extremos
* imputación de valores nulos
* eliminación de duplicados
* normalización de variables temporales
* validación de consistencia geográfica
* generación de variables derivadas (día, mes, trimestre, fin de semana)

Los archivos procesados se almacenan en:

```text
data/processed
```

---

# ✅ Data Quality

El pipeline ejecuta validaciones posteriores a la limpieza para verificar:

* porcentaje de valores nulos
* duplicados restantes
* tipos de datos
* valores fuera de rango
* consistencia de variables temporales
* cardinalidad de variables categóricas
* integridad general del dataset

Los reportes se almacenan en:

```text
data/reports
```

---

# 📉 Data Visualization

El proyecto genera visualizaciones automáticas para analizar distribuciones, detectar anomalías y validar patrones en siniestros viales.

Las visualizaciones incluyen:

* histogramas de variables numéricas
* boxplots para detección de outliers
* distribución de variables categóricas
* análisis de severidad de siniestros
* normalización de variables críticas
* visualización de clustering

Estos gráficos permiten:

* entender distribución de accidentes
* detectar patrones de riesgo
* analizar comportamiento temporal
* validar limpieza de datos
* visualizar agrupamientos

---

## 📂 Ubicación de los gráficos

Todos los gráficos se almacenan en:

```text
data/graphics
```


---

# 🤖 Data Machine Learning: No Supervisado

El proyecto implementa técnicas de Machine Learning para identificar patrones en siniestros viales.

## Técnicas utilizadas

### K-Means Clustering

Permite segmentar siniestros en grupos según:

* cantidad de víctimas
* severidad del accidente
* ubicación geográfica
* variables temporales
* tipo de vía
* contraparte involucrada

Los resultados permiten identificar perfiles de siniestros de alto riesgo, patrones urbanos y comportamientos recurrentes.

---

## Ubicación de resultados

Todos los resultados se almacenan en:

```text
data/output/unsupervised_learning
```
---

# 🤖 Data Machine Learning: Supervisado

El proyecto implementa técnicas de Machine Learning supervisado para predecir la ocurrencia de siniestros con víctimas fatales a partir de variables temporales, geográficas y estructurales del evento.

## Técnicas utilizadas

### K-Nearest Neighbors (KNN)

Se utiliza el algoritmo KNN como modelo de clasificación supervisada para predecir la variable objetivo:

> **hay_muerte (0/1)** → indica si el siniestro tuvo al menos una víctima mortal.

El modelo aprende patrones a partir de eventos históricos y clasifica nuevos registros en función de su similitud con casos anteriores.

---

## Variables utilizadas (features)

El modelo utiliza variables del contexto del siniestro:

* hora del siniestro
* comuna del siniestro
* día de la semana
* mes del año
* ubicación geográfica (latitud / longitud)
* número total de víctimas

Estas variables permiten capturar patrones temporales, espaciales y de severidad del accidente.

---

## Ubicación de resultados

Todos los resultados se almacenan en:

```text
data/output/supervised_learning
```
---


# 🚀 Ejecución Local

## Crear entorno virtual

```bash
python -m venv .venv
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecutar scripts manualmente

## Ingesta de datos

```bash
python jobs/data_ingestion.py
```

## Limpieza de datos

```bash
python jobs/data_cleaning.py
```

## Calidad de datos

```bash
python jobs/data_quality.py
```

## Visualización

```bash
python jobs/data_visualization.py
```

## Machine Learning: Supervised

```bash
python jobs/data_supervised_learning.py
```

## Machine Learning: Unsupervised

```bash
python jobs/data_unsupervised_learning.py
```


---

# 🧠 Justificación Tecnológica

## Python

Python fue seleccionado por su simplicidad, legibilidad y amplio ecosistema en análisis de datos y machine learning.

## Pandas

Pandas se utilizó como herramienta principal para manipulación y transformación de datos tabulares de siniestros viales.

## Matplotlib

Matplotlib permite generar visualizaciones estadísticas para analizar distribuciones, outliers y patrones espaciales/temporales.

## Scikit-Learn

Scikit-Learn se utilizó para aplicar técnicas de clustering no supervisado como K-Means, además de escalado y reducción de dimensionalidad.

## Docker

Docker permite ejecutar el pipeline en un entorno reproducible y aislado, garantizando consistencia entre ejecuciones.

## No utilización de Airflow

No se utilizó Apache Airflow debido a que el pipeline no requiere orquestación compleja ni scheduling distribuido, manteniéndose una arquitectura simple y reproducible.

---

# 📖 Referencias

* [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
* [https://scikit-learn.org/stable/documentation.html](https://scikit-learn.org/stable/documentation.html)
* [https://matplotlib.org/stable/index.html](https://matplotlib.org/stable/index.html)
* [https://docs.docker.com/](https://docs.docker.com/)

