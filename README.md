# 📊 Análisis Inteligente de Datos — Siniestros Viales Analytics

Proyecto orientado al procesamiento, análisis y modelado de datos de siniestros viales utilizando Python, Pandas y Docker.

El objetivo principal es construir un pipeline completo de ingeniería de datos capaz de:

* ingesta automatizada de datasets de siniestros viales
* limpieza y transformación de los datos
* validación de calidad e integridad de la información
* generación de variables derivadas para el análisis
* análisis exploratorio mediante estadísticas descriptivas y visualizaciones
* entrenamiento y evaluación de un modelo de Deep Learning para la predicción de siniestros con víctimas fatales
* generación automática de reportes, métricas y gráficos para el análisis de resultados

---

# 🚀 Tecnologías Utilizadas

* Python 
* TensorFlow / Keras
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Great Expectations
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
│   └── data_deep_learning.py
│
├── docker-compose.yml
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
* Data Deep Learning

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
data_deep_learning
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

# 📉 Data Deep Learning

El pipeline incorpora un modelo de Deep Learning desarrollado con TensorFlow/Keras para predecir la probabilidad de que un siniestro vial tenga víctimas fatales a partir de las variables disponibles en el conjunto de datos.

El proceso incluye:

- preparación y selección de variables predictoras
- codificación de variables categóricas
- normalización de variables numéricas
- división del dataset en entrenamiento y prueba
- entrenamiento de una red neuronal multicapa (MLP)
- evaluación del modelo mediante métricas de clasificación
- generación de visualizaciones del proceso de entrenamiento

Durante la ejecución se generan automáticamente los siguientes artefactos:

- reporte de clasificación
- matriz de confusión
- historial del entrenamiento
- curvas de pérdida (Loss)
- curvas de Recall
- distribución de probabilidades predichas
- predicciones del conjunto de prueba

---

## 📂 Ubicación de los gráficos

Todos los gráficos se almacenan en:

```text
data/graphics
```




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

## Deep Learning

```bash
python jobs/data_deep_learning.py
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

