# 📊 Analisis Inteligente de Datos

Proyecto orientado al procesamiento y análisis de datos utilizando Python, Pandas y Docker.

El objetivo principal es construir un pipeline simple de ingeniería de datos capaz de:

* descargar datasets reales
* limpiar información inconsistente
* generar métricas descriptivas
* realizar agregaciones sobre grandes volúmenes de datos

# 🚀 Tecnologías Utilizadas

* Python
* Pandas
* Docker
* Docker Compose
* Parquet
* CSV

---

# 📂 Estructura del Proyecto

```text id="gh5l2x"
.
├── data
│   ├── raw
│   ├── processed
│   ├── output
│   └── reports
│
├── docker
│
├── jobs
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── data_aggregation.py
│   └── data_profiling.py
│
├── docker-compose.yml
└── README.md
```

---

# 📥 Dataset Utilizado

Se utilizan datasets públicos del sistema de taxis de NYC.

## NYC TLC Trip Record Data

[NYC Taxi & Limousine Commission Dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page?utm_source=chatgpt.com)

Los datasets incluyen:

* viajes
* distancias
* tarifas
* propinas
* timestamps
* zonas geográficas
* métodos de pago

---

# 🧠 Objetivos del Proyecto

El pipeline implementa:

* Data Ingestion
* Data Cleaning
* Data Profiling
* Data Aggregation

---

# 🔄 Pipeline de Datos

```text id="ey3x9u"
data_ingestion
      ↓
data_cleaning
      ↓
data_profiling
      ↓
data_aggregation
```

---

# 🐳 Ejecución con Docker

## Construir containers

```bash id="n7r3kt"
docker compose build
```

## Ejecutar pipeline completo

```bash id="h2w8cv"
docker compose up
```

---

# 📥 Data Ingestion

El proyecto permite descargar automáticamente datasets según un año.

Ejemplo:

```yaml id="h8j5mt"
environment:
  - YEAR=2025
```
---

# 📊 Data Profiling

El proyecto genera reportes automáticos de profiling para cada archivo procesado.

Las métricas incluyen:

* media
* mediana
* desviación estándar
* skewness
* kurtosis
* percentiles
* outliers
* porcentaje de nulos
* cardinalidad
* valores únicos
* memoria utilizada
* tiempo de procesamiento

Los reportes se almacenan en:

```text id="x6c9wr"
data/reports
```

---

# 🧹 Data Cleaning

El proceso de limpieza incluye:

* eliminación de registros inválidos
* manejo de valores nulos
* eliminación de duplicados
* validación de rangos
* filtrado de outliers
* normalización de columnas

Los archivos procesados se almacenan en:

```text id="z4m1kq"
data/processed
```

---

# 📈 Data Aggregation

El pipeline genera métricas agregadas como:

* viajes por hora
* revenue total
* distancia promedio
* propina promedio
* duración promedio
* cantidad de viajes
* análisis temporal

Los resultados se almacenan en:

```text id="u2k5np"
data/output
```

---

# 🚀 Ejecución Local

## Crear entorno virtual

```bash id="q8v2md"
python -m venv .venv
```


## Instalar dependencias

```bash id="f5j1cw"
pip install -r requirements.txt
```

---

## Ejecutar scripts manualmente

### Descargar datos

```bash id="m7t2qk"
python jobs/download_data.py
```

### Limpiar datos

```bash id="w3c8nr"
python jobs/clean_data.py
```

### Generar profiling

```bash id="g6p1vf"
python jobs/data_profiling.py
```

### Ejecutar agregaciones

```bash id="b9x4ku"
python jobs/aggregation_data.py
```

---

# 📖 Referencias

* [Apache Spark](https://spark.apache.org?utm_source=chatgpt.com)
* [Pandas Documentation](https://pandas.pydata.org/docs/?utm_source=chatgpt.com)
* [Docker Documentation](https://docs.docker.com/?utm_source=chatgpt.com)
