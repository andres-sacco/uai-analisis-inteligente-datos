import pandas as pd
import glob
import os
import gc

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

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
# Configuración gráficos
# ==================================================

plt.rcParams["figure.dpi"] = 100
plt.rcParams["savefig.dpi"] = 150

# ==================================================
# Procesar archivos
# ==================================================

for file in INPUT_FILES:

    print(f"\n📂 Procesando {file}")

    df = pd.read_csv(
        file,
        low_memory=False
    )

    print("\n📋 Columnas encontradas:")
    print(df.columns.tolist())

    base_name = os.path.basename(file)

    # ==================================================
    # Variables numéricas para análisis
    # ==================================================

    variables_plot = [
        "numero_total_de_victimas",
        "hora_siniestro",
        "comuna_siniestro"
    ]

    titulos = [
        "Total de víctimas",
        "Hora del siniestro",
        "Comuna"
    ]

    color_uai = "#7B1C2E"

    # ==================================================
    # Verificar columnas
    # ==================================================

    available_variables = [
        col
        for col in variables_plot
        if col in df.columns
    ]

    available_titles = [
        titulos[variables_plot.index(col)]
        for col in available_variables
    ]

    if len(available_variables) == 0:

        print(
            "⚠️ No se encontraron "
            "columnas numéricas esperadas"
        )

        continue

    # ==================================================
    # HISTOGRAMAS
    # ==================================================

    print("📊 Generando histogramas")

    fig, axes = plt.subplots(
        1,
        len(available_variables),
        figsize=(
            5 * len(available_variables),
            4
        )
    )

    if len(available_variables) == 1:
        axes = [axes]

    for i, (var, titulo) in enumerate(
        zip(
            available_variables,
            available_titles
        )
    ):

        axes[i].hist(
            df[var].dropna(),
            bins=30,
            color=color_uai,
            edgecolor="black",
            alpha=0.8
        )

        axes[i].set_title(
            titulo,
            fontsize=11,
            fontweight="bold"
        )

        axes[i].set_xlabel(var)

        axes[i].set_ylabel(
            "Frecuencia"
        )

        axes[i].grid(
            True,
            alpha=0.3
        )

    plt.suptitle(
        "Distribución de variables numéricas de siniestros viales",
        fontsize=13,
        fontweight="bold",
        y=1.02
    )

    plt.tight_layout()

    histogram_output = (
        f"{OUTPUT_DIR}/"
        f"{base_name.replace('.csv', '_histograms.png')}"
    )

    plt.savefig(
        histogram_output,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"✅ Histogramas guardados: "
        f"{histogram_output}"
    )

    # ==================================================
    # BOXPLOTS
    # ==================================================

    print("📦 Generando boxplots")

    fig, axes = plt.subplots(
        1,
        len(available_variables),
        figsize=(
            5 * len(available_variables),
            5
        )
    )

    if len(available_variables) == 1:
        axes = [axes]

    for i, (var, titulo) in enumerate(
        zip(
            available_variables,
            available_titles
        )
    ):

        axes[i].boxplot(
            df[var].dropna(),
            patch_artist=True,
            boxprops=dict(
                facecolor=color_uai,
                alpha=0.7
            ),
            medianprops=dict(
                color="white",
                linewidth=2
            ),
            flierprops=dict(
                marker="o",
                markerfacecolor="#A52A4A",
                markersize=3,
                alpha=0.5
            ),
            tick_labels=[""]
        )

        axes[i].set_title(
            titulo,
            fontsize=11,
            fontweight="bold"
        )

        axes[i].set_ylabel(var)

        axes[i].grid(
            True,
            alpha=0.3,
            axis="y"
        )

    plt.suptitle(
        "Boxplots de variables de siniestros viales",
        fontsize=13,
        fontweight="bold",
        y=1.02
    )

    plt.tight_layout()

    boxplot_output = (
        f"{OUTPUT_DIR}/"
        f"{base_name.replace('.csv', '_boxplots.png')}"
    )

    plt.savefig(
        boxplot_output,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"✅ Boxplots guardados: "
        f"{boxplot_output}"
    )

    # ==================================================
    # VARIABLES CATEGÓRICAS
    # ==================================================

    print(
        "📊 Generando gráficos categóricos"
    )

    categorical_columns = [
        "gravedad_siniestro",
        "modo_desplazamiento_victima",
        "contraparte_siniestro"
    ]

    for column in categorical_columns:

        if column not in df.columns:
            continue

        plt.figure(
            figsize=(12, 5)
        )

        (
            df[column]
            .fillna("DESCONOCIDO")
            .value_counts()
            .head(15)
            .plot(kind="bar")
        )

        plt.title(
            column
            .replace("_", " ")
            .title()
        )

        plt.ylabel("Cantidad")
        plt.xlabel("")

        plt.tight_layout()

        output_file = (
            f"{OUTPUT_DIR}/"
            f"{base_name.replace('.csv', '')}"
            f"_{column}.png"
        )

        plt.savefig(
            output_file,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"✅ Guardado: "
            f"{output_file}"
        )

    # ==================================================
    # NORMALIZACIÓN
    # ==================================================

    normalization_column = (
        "numero_total_de_victimas"
    )

    if normalization_column in df.columns:

        print(
            "📏 Generando normalización"
        )

        min_value = (
            df[normalization_column]
            .min()
        )

        max_value = (
            df[normalization_column]
            .max()
        )

        df["victimas_minmax"] = (
            (
                df[normalization_column]
                - min_value
            )
            /
            (
                max_value
                - min_value
            )
        )

        mean_value = (
            df[normalization_column]
            .mean()
        )

        std_value = (
            df[normalization_column]
            .std()
        )

        df["victimas_zscore"] = (
            (
                df[normalization_column]
                - mean_value
            )
            /
            std_value
        )

        fig, axes = plt.subplots(
            1,
            3,
            figsize=(15, 5)
        )

        axes[0].boxplot(
            df[normalization_column].dropna(),
            patch_artist=True,
            boxprops=dict(
                facecolor="#7B1C2E",
                alpha=0.7
            ),
            medianprops=dict(
                color="white",
                linewidth=2
            ),
            tick_labels=[""]
        )

        axes[0].set_title(
            "Original"
        )

        axes[1].boxplot(
            df["victimas_minmax"].dropna(),
            patch_artist=True,
            boxprops=dict(
                facecolor="#A52A4A",
                alpha=0.7
            ),
            medianprops=dict(
                color="white",
                linewidth=2
            ),
            tick_labels=[""]
        )

        axes[1].set_title(
            "Min-Max"
        )

        axes[2].boxplot(
            df["victimas_zscore"].dropna(),
            patch_artist=True,
            boxprops=dict(
                facecolor="#C44569",
                alpha=0.7
            ),
            medianprops=dict(
                color="white",
                linewidth=2
            ),
            tick_labels=[""]
        )

        axes[2].set_title(
            "Z-Score"
        )

        plt.suptitle(
            "Comparación de métodos de normalización — Número total de víctimas",
            fontsize=13,
            fontweight="bold",
            y=1.02
        )

        plt.tight_layout()

        normalization_output = (
            f"{OUTPUT_DIR}/"
            f"{base_name.replace('.csv', '_normalization.png')}"
        )

        plt.savefig(
            normalization_output,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"✅ Normalización guardada: "
            f"{normalization_output}"
        )

    # ==================================================
    # Liberar memoria
    # ==================================================

    del df

    gc.collect()

    print("🧹 Memoria liberada")

print("\n🎉 Visualización completada")