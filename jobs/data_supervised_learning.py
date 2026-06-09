import pandas as pd
import glob
import os
import gc

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    StandardScaler
)

from sklearn.neighbors import (
    KNeighborsClassifier
)

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,

    confusion_matrix,
    ConfusionMatrixDisplay,

    classification_report

)

# ==================================================
# CONFIGURACION
# ==================================================

INPUT_FILES = glob.glob(
    "data/processed/*.csv"
)

OUTPUT_DIR = "data/output/supervised_learning/"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==================================================
# CARGA DE DATOS
# ==================================================

if not INPUT_FILES:

    print(
        "❌ No se encontraron archivos"
    )

    exit(1)

dataframes = []

for file in INPUT_FILES:

    print(
        f"📂 Leyendo {file}"
    )

    df = pd.read_csv(
        file,
        low_memory=False
    )

    dataframes.append(df)

df = pd.concat(
    dataframes,
    ignore_index=True
)

print(
    f"📊 Registros: {len(df):,}"
)

# ==================================================
# CREAR VARIABLE OBJETIVO
# ==================================================

df["hay_muerte"] = (

    pd.to_numeric(
        df[
            "numero_victimas_mortal_siniestro"
        ],
        errors="coerce"
    )

    > 0

).astype(int)

print("\n📊 Distribución objetivo")

print(
    df["hay_muerte"]
    .value_counts()
)

# ==================================================
# FEATURES
# ==================================================

features = [

    "hora_siniestro",
    "comuna_siniestro",
    "dia_semana",
    "mes_siniestro",
    "latitud_siniestro",
    "longitud_siniestro",
    "numero_total_de_victimas"

]

# ==================================================
# LIMPIEZA
# ==================================================

for col in features:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

dataset = df[
    features +
    ["hay_muerte"]
].dropna()

print(
    f"\n📊 Registros utilizables: "
    f"{len(dataset):,}"
)

# ==================================================
# X / Y
# ==================================================

X = dataset[
    features
]

y = dataset[
    "hay_muerte"
]

# ==================================================
# TRAIN TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = (

    train_test_split(

        X,
        y,

        test_size=0.2,

        random_state=42,

        stratify=y

    )

)

print(
    f"Train: {len(X_train):,}"
)

print(
    f"Test : {len(X_test):,}"
)

# ==================================================
# NORMALIZACION
# ==================================================

print(
    "\n📏 Escalando variables"
)

scaler = StandardScaler()

X_train_scaled = (

    scaler.fit_transform(
        X_train
    )

)

X_test_scaled = (

    scaler.transform(
        X_test
    )

)

# ==================================================
# BUSQUEDA DEL MEJOR K
# ==================================================

print(
    "\n🔍 Buscando mejor K"
)

results = []

best_score = 0
best_k = 1

for k in range(1, 21):

    model = KNeighborsClassifier(
        n_neighbors=k
    )

    model.fit(
        X_train_scaled,
        y_train
    )

    predictions = model.predict(
        X_test_scaled
    )

    score = accuracy_score(
        y_test,
        predictions
    )

    results.append({

        "k": k,
        "accuracy": score

    })

    if score > best_score:

        best_score = score
        best_k = k

print(
    f"\n✅ Mejor K: {best_k}"
)

print(
    f"✅ Accuracy: {best_score:.4f}"
)

# ==================================================
# GRAFICO DEL K
# ==================================================

results_df = pd.DataFrame(
    results
)

plt.figure(
    figsize=(8, 5)
)

plt.plot(

    results_df["k"],
    results_df["accuracy"]

)

plt.title(
    "Accuracy por valor de K"
)

plt.xlabel(
    "K"
)

plt.ylabel(
    "Accuracy"
)

plt.grid(True)

plt.savefig(

    f"{OUTPUT_DIR}/knn_k_search.png",

    bbox_inches="tight"

)

plt.close()

# ==================================================
# MODELO FINAL
# ==================================================

print(
    "\n🤖 Entrenando modelo final"
)

knn = KNeighborsClassifier(
    n_neighbors=best_k
)

knn.fit(
    X_train_scaled,
    y_train
)

predictions = knn.predict(
    X_test_scaled
)

# ==================================================
# METRICAS
# ==================================================

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

print("\n📋 RESULTADOS")

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)

print(
    "\n📄 Classification Report"
)

print(

    classification_report(
        y_test,
        predictions,
        zero_division=0
    )

)

# ==================================================
# MATRIZ DE CONFUSION
# ==================================================

cm = confusion_matrix(
    y_test,
    predictions
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot()

plt.savefig(

    f"{OUTPUT_DIR}/knn_confusion_matrix.png",

    bbox_inches="tight"

)

plt.close()

# ==================================================
# GUARDAR METRICAS
# ==================================================

metrics = pd.DataFrame({

    "metric": [

        "accuracy",
        "precision",
        "recall",
        "f1"

    ],

    "value": [

        accuracy,
        precision,
        recall,
        f1

    ]

})

metrics.to_csv(

    f"{OUTPUT_DIR}/knn_metrics.csv",

    index=False

)

# ==================================================
# EJEMPLOS DE PREDICCION
# ==================================================

predictions_df = X_test.copy()

predictions_df["real"] = (
    y_test.values
)

predictions_df["predicho"] = (
    predictions
)

predictions_df.to_csv(

    f"{OUTPUT_DIR}/knn_predictions.csv",

    index=False

)

print(
    "\n💾 Archivos generados:"
)

print(
    "- knn_metrics.csv"
)

print(
    "- knn_predictions.csv"
)

print(
    "- knn_confusion_matrix.png"
)

print(
    "- knn_k_search.png"
)

gc.collect()

print(
    "\n🎉 KNN completado"
)
