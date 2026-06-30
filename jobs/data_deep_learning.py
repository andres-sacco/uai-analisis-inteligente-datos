import pandas as pd
import glob
import os
import gc
import sys

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Input,
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ==================================================
# Configuración
# ==================================================

INPUT_FILES = glob.glob(
    "data/processed/*.csv"
)

OUTPUT_DIR = "data/graphics"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==================================================
# Verificar archivos
# ==================================================

if not INPUT_FILES:

    print("❌ No se encontraron archivos CSV")
    print("📂 Path buscado: data/processed/*.csv")

    sys.exit(1)

print(
    f"✅ Archivos encontrados: {len(INPUT_FILES)}"
)

EPOCHS = 25
BATCH_SIZE = 32
CLASS_WEIGHTS = {
    0: 1,
    1: 50
}

THRESHOLD = 0.5

# ==================================================
# Procesar archivos
# ==================================================

for file in INPUT_FILES:

    print("\n================================================")
    print(f"🔍 Verificando calidad: {file}")
    print("================================================")

    # ==================================================
    # Lectura del archivo
    # ==================================================

    df = pd.read_csv(
        file,
        low_memory=False,
        keep_default_na=True

    )

    # ==================================================
    # Preparación de datos
    # ==================================================

    TARGET = "hay_muerte"

    # Crear la variable objetivo si aún no existe
    if TARGET not in df.columns:
        df[TARGET] = (
                df["numero_victimas_mortal_siniestro"] > 0
        ).astype(int)

    # Variable objetivo
    y = df[TARGET]

    # Variables predictoras
    X = df.drop(
        columns=[
            TARGET,
            "numero_victimas_mortal_siniestro"  # Evita data leakage
        ],
        errors="ignore"
    )

    # Conservar únicamente columnas útiles
    X = X.dropna(axis=1, how="all")
    MAX_CATEGORIAS = 100

    categoricas = X.select_dtypes(include=["object"]).columns

    for col in categoricas:
        n = X[col].nunique()

        if n > MAX_CATEGORIAS:
            print(f"Eliminando {col}: {n} categorías")
            X = X.drop(columns=col)



    # Convertir variables categóricas a numéricas
    X = pd.get_dummies(
        X,
        drop_first=True,
        dtype="uint8"
    )
    X = X.astype("float32")

    # Reemplazar posibles valores faltantes
    X = X.fillna(0)

    print(f"Variables utilizadas: {len(X.columns)}")
    print(f"Clase 0: {(y == 0).sum():,}")
    print(f"Clase 1: {(y == 1).sum():,}")

    # ==================================================
    # Train / Test
    # ==================================================
    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42,

        stratify=y
    )

    del X
    gc.collect()

    # ==================================================
    # Escalado
    # ==================================================

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    ).astype("float32")

    X_test_scaled = scaler.transform(
        X_test
    ).astype("float32")

    del X_train
    del X_test
    gc.collect()

    # ==================================================
    # Construcción del modelo
    # ==================================================

    print("\n================================================")
    print("🧠 CONSTRUCCIÓN DEL MODELO")
    print("================================================")

    model = Sequential([

        Input(
            shape=(
                X_train_scaled.shape[1],
            )
        ),

        Dense(
            32,
            activation="relu"
        ),

        Dropout(
            0.2
        ),

        Dense(
            16,
            activation="relu"
        ),

        Dense(
            1,
            activation="sigmoid"
        )

    ])

    model.summary()

    # ==================================================
    # Compilación
    # ==================================================

    print("\n================================================")
    print("⚙️ COMPILACIÓN DEL MODELO")
    print("================================================")

    model.compile(

        optimizer="adam",

        loss="binary_crossentropy",

        metrics=[

            "accuracy",

            tf.keras.metrics.Recall(
                name="recall"
            )

        ]

    )

    # ==================================================
    # Entrenamiento
    # ==================================================

    print("\n================================================")
    print("🚀 ENTRENAMIENTO")
    print("================================================")

    history = model.fit(

        X_train_scaled,

        y_train,

        epochs=EPOCHS,

        batch_size=BATCH_SIZE,

        validation_split=0.1,

        class_weight=CLASS_WEIGHTS,

        verbose=1

    )

    # ==================================================
    # Predicciones
    # ==================================================

    print("\n================================================")
    print("🔮 PREDICCIONES")
    print("================================================")

    y_prob = model.predict(
        X_test_scaled
    )

    y_pred = (
        y_prob > THRESHOLD
    ).astype(int)

    # ==================================================
    # Reporte de clasificación
    # ==================================================

    print("\n================================================")
    print("📊 REPORTE DE CLASIFICACIÓN")
    print("================================================")

    reporte = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    pd.DataFrame(reporte).transpose().to_csv(
        os.path.join(OUTPUT_DIR, "classification_report.csv")
    )

    print(classification_report(y_test, y_pred))

    pd.DataFrame(
        history.history
    ).to_csv(
        os.path.join(
            OUTPUT_DIR,
            "history.csv"
        ),
        index=False
    )

    pd.DataFrame({

        "real": y_test.values,

        "probabilidad": y_prob.flatten(),

        "prediccion": y_pred.flatten()

    }).to_csv(

        os.path.join(
            OUTPUT_DIR,
            "predicciones.csv"
        ),

        index=False

    )

    # ==================================================
    # Matriz de confusión
    # ==================================================

    print("\n================================================")
    print("📌 MATRIZ DE CONFUSIÓN")
    print("================================================")

    cm = confusion_matrix(

        y_test,

        y_pred

    )

    disp = ConfusionMatrixDisplay(

        confusion_matrix=cm,

        display_labels=[

            "No Fatal",

            "Fatal"

        ]

    )

    disp.plot(
        cmap="Blues"
    )

    plt.title(
        "Matriz de Confusión - Deep Learning"
    )

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "confusion_matrix.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ==================================================
    # Distribución de probabilidades
    # ==================================================

    print("\n================================================")
    print("📈 DISTRIBUCIÓN DE PROBABILIDADES")
    print("================================================")

    plt.figure(
        figsize=(6, 4)
    )

    plt.hist(

        y_prob,

        bins=30

    )

    plt.title(
        "Distribución de Probabilidades"
    )

    plt.xlabel(
        "Probabilidad de Fatalidad"
    )

    plt.ylabel(
        "Cantidad de Casos"
    )

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "probabilidades.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ==================================================
    # Curvas de entrenamiento
    # ==================================================

    print("\n================================================")
    print("📈 CURVAS DE ENTRENAMIENTO")
    print("================================================")

    fig, ax = plt.subplots(

        1,

        2,

        figsize=(12, 4)

    )

    # Loss

    ax[0].plot(

        history.history["loss"],

        label="Entrenamiento"

    )

    ax[0].plot(

        history.history["val_loss"],

        label="Validación"

    )

    ax[0].set_title(
        "Loss"
    )

    ax[0].set_xlabel(
        "Épocas"
    )

    ax[0].set_ylabel(
        "Loss"
    )

    ax[0].legend()

    # Recall

    ax[1].plot(

        history.history["recall"],

        label="Entrenamiento"

    )

    ax[1].plot(

        history.history["val_recall"],

        label="Validación"

    )

    ax[1].set_title(
        "Recall"
    )

    ax[1].set_xlabel(
        "Épocas"
    )

    ax[1].set_ylabel(
        "Recall"
    )

    ax[1].legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "training_curves.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ==================================================
    # Resumen
    # ==================================================

    print("\n================================================")
    print("✅ RESUMEN")
    print("================================================")

    print(
        f"Épocas: {EPOCHS}"
    )

    print(
        f"Batch Size: {BATCH_SIZE}"
    )

    print(
        f"Threshold: {THRESHOLD}"
    )

    print(
        f"Pesos de clase: {CLASS_WEIGHTS}"
    )

    # ==================================================
    # Liberar memoria
    # ==================================================

    tf.keras.backend.clear_session()

    del model
    del history
    del y_prob
    del y_pred
    del cm

    gc.collect()

    print(
        "\n🧹 Memoria liberada"
    )