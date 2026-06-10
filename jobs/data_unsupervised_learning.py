import gc
import glob
import os

import pandas as pd

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# ==================================================
# CONFIGURACION
# ==================================================

INPUT_FILES = glob.glob(
    "data/processed/*.csv"
)

OUTPUT_DIR = "data/output/unsupervised_learning/"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==================================================
# Verificar archivos
# ==================================================

if not INPUT_FILES:

    print(
        "❌ No se encontró el archivo "
        "victimas_siniestros_viales_hechos_clean.csv"
    )

    exit(1)

print(
    f"✅ Archivos encontrados: "
    f"{len(INPUT_FILES)}"
)

# ==================================================
# Lectura
# ==================================================

print(
    "\n📂 Leyendo dataset"
)

df = pd.read_csv(
    INPUT_FILES[0],
    low_memory=False
)

print(
    f"📊 Registros: {len(df):,}"
)

print(
    f"📊 Columnas: {len(df.columns)}"
)

# ==================================================
# Variables para clustering
# ==================================================

NUMERIC_COLUMNS = [

    "numero_total_de_victimas",
    "numero_victimas_leve_siniestro",
    "numero_victimas_grave_siniestro",
    "numero_victimas_mortal_siniestro",
    "hora_siniestro",
    "comuna_siniestro",
    "latitud_siniestro",
    "longitud_siniestro",
    "dia_semana",
    "trimestre",
    "fin_de_semana"

]

CATEGORICAL_COLUMNS = [

    "tipo_de_via_siniestro",
    "modo_desplazamiento_victima",
    "contraparte_siniestro",
    "gravedad_siniestro"

]

# ==================================================
# Verificar columnas
# ==================================================

required_columns = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    print(
        f"❌ Faltan columnas: "
        f"{missing_columns}"
    )

    exit(1)

# ==================================================
# Selección de variables
# ==================================================

print(
    "\n🧠 Preparando variables"
)

cluster_df = df[
    required_columns
].copy()

# ==================================================
# Completar categóricas
# ==================================================

for col in CATEGORICAL_COLUMNS:

    cluster_df[col] = (

        cluster_df[col]
        .fillna("DESCONOCIDO")
        .astype(str)

    )

# ==================================================
# Imputar nulos numéricos
# ==================================================

imputer = SimpleImputer(
    strategy="median"
)

cluster_df[NUMERIC_COLUMNS] = (

    imputer.fit_transform(
        cluster_df[NUMERIC_COLUMNS]
    )

)

# ==================================================
# One Hot Encoding
# ==================================================

encoded_df = pd.get_dummies(
    cluster_df,
    columns=CATEGORICAL_COLUMNS,
    drop_first=False
)

# ==================================================
# Dataset final
# ==================================================

X = encoded_df.copy()

print(
    f"📊 Features utilizadas: "
    f"{X.shape[1]}"
)

# ==================================================
# Escalado
# ==================================================

print(
    "\n📏 Escalando variables"
)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ==================================================
# K-MEANS (FIJO = 3 CLUSTERS)
# ==================================================

print(
    "\n🤖 Ejecutando K-Means con 3 clusters"
)

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X_scaled)

result_df = df.copy()

result_df["cluster"] = clusters

# ==================================================
# PCA
# ==================================================

print(
    "\n📉 Aplicando PCA"
)

pca = PCA(n_components=2)

components = pca.fit_transform(X_scaled)

result_df["pca_1"] = components[:, 0]
result_df["pca_2"] = components[:, 1]

# ==================================================
# RESUMEN CLUSTERS
# ==================================================

print(
    "\n📊 RESUMEN CLUSTERS"
)

cluster_summary = (

    result_df
    .groupby("cluster")
    .agg(

        cantidad_siniestros=(
            "id_siniestro",
            "count"
        ),

        promedio_victimas=(
            "numero_total_de_victimas",
            "mean"
        ),

        promedio_hora=(
            "hora_siniestro",
            "mean"
        ),

        promedio_comuna=(
            "comuna_siniestro",
            "mean"
        )

    )

)

print(cluster_summary)

# ==================================================
# GUARDAR RESUMEN
# ==================================================

summary_output = (
    f"{OUTPUT_DIR}/kmeans_cluster_summary.csv"
)

cluster_summary.to_csv(summary_output)

print(
    f"\n💾 Resumen guardado: "
    f"{summary_output}"
)

# ==================================================
# DISTRIBUCIÓN
# ==================================================

distribution = (
    result_df["cluster"]
    .value_counts()
    .sort_index()
)

print("\n📈 Distribución")
print(distribution)

distribution_output = (
    f"{OUTPUT_DIR}/cluster_distribution.csv"
)

distribution.to_csv(distribution_output)

# ==================================================
# PCA PLOT
# ==================================================

print("\n📊 Generando gráfico PCA")

plt.figure(figsize=(12, 8))

scatter = plt.scatter(
    result_df["pca_1"],
    result_df["pca_2"],
    c=result_df["cluster"],
    alpha=0.6
)

plt.title(
    "Segmentación de Siniestros Viales mediante K-Means",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")

plt.grid(True, alpha=0.3)

plt.colorbar(scatter, label="Cluster")

graphic_output = (
    f"{OUTPUT_DIR}/kmeans_siniestros_segmentation.png"
)

plt.savefig(
    graphic_output,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print(
    f"💾 Gráfico guardado: "
    f"{graphic_output}"
)

# ==================================================
# DISTRIBUCIÓN HORARIA POR CLUSTER
# ==================================================

print("\n🕒 Generando distribución horaria por cluster")

fig, ax = plt.subplots(figsize=(12, 5))

N_CLUSTERS = kmeans.n_clusters

for i in range(N_CLUSTERS):

    datos_hora = result_df[
        result_df["cluster"] == i
    ]["hora_siniestro"]

    ax.hist(
        datos_hora,
        bins=24,
        alpha=0.5,
        label=f"Cluster {i}",
        edgecolor="white"
    )

ax.set_title(
    "Distribución horaria por cluster",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Hora del siniestro")
ax.set_ylabel("Cantidad")
ax.set_xticks(range(0, 24))
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()

hora_output = (
    f"{OUTPUT_DIR}/cluster_hour_distribution.png"
)

plt.savefig(
    hora_output,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print(
    f"💾 Gráfico guardado: "
    f"{hora_output}"
)

# ==================================================
# DISTRIBUCIÓN DE GRAVEDAD POR CLUSTER
# ==================================================

if "gravedad_siniestro" in result_df.columns:

    print(
        "\n⚠️ Generando distribución "
        "de gravedad por cluster"
    )

    fig, axes = plt.subplots(
        1,
        N_CLUSTERS,
        figsize=(5 * N_CLUSTERS, 5),
        sharey=True
    )

    if N_CLUSTERS == 1:
        axes = [axes]

    for i in range(N_CLUSTERS):

        datos_cluster = (
            result_df[
                result_df["cluster"] == i
            ]["gravedad_siniestro"]
            .value_counts()
        )

        datos_cluster.plot(
            kind="bar",
            ax=axes[i],
            color=plt.cm.viridis(
                i / N_CLUSTERS
            )
        )

        axes[i].set_title(
            f"Cluster {i}",
            fontweight="bold"
        )

        axes[i].set_xlabel(
            "Gravedad"
        )

        axes[i].tick_params(
            axis="x",
            rotation=45
        )

    axes[0].set_ylabel(
        "Cantidad de siniestros"
    )

    fig.suptitle(
        "Distribución de gravedad por cluster",
        fontsize=14,
        fontweight="bold"
    )

    plt.tight_layout()

    gravedad_output = (
        f"{OUTPUT_DIR}/cluster_gravity_distribution.png"
    )

    plt.savefig(
        gravedad_output,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"💾 Gráfico guardado: "
        f"{gravedad_output}"
    )

# ==================================================
# DATASET FINAL
# ==================================================

segmentation_output = (
    f"{OUTPUT_DIR}/siniestros_clusterizados.csv"
)

result_df.to_csv(
    segmentation_output,
    index=False
)

print(
    f"💾 Dataset guardado: "
    f"{segmentation_output}"
)

# ==================================================
# CENTROIDES
# ==================================================

centroids = pd.DataFrame(
    kmeans.cluster_centers_,
    columns=X.columns
)

centroids_output = (
    f"{OUTPUT_DIR}/cluster_centroids.csv"
)

centroids.to_csv(
    centroids_output,
    index=False
)

print(
    f"💾 Centroides guardados: "
    f"{centroids_output}"
)

# ==================================================
# LIBERAR MEMORIA
# ==================================================

del df
del cluster_df
del encoded_df
del X
del X_scaled
del result_df

gc.collect()

print("\n🎉 Clustering completado")