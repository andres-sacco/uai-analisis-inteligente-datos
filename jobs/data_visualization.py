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
    "data/processed/*.parquet"
)

OUTPUT_DIR = "data/graphics"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# Configuración gráficos
# ==================================================

plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 150

# ==================================================
# Procesar archivos
# ==================================================

for file in INPUT_FILES:

    print(f"\n📂 Procesando {file}")

    df = pd.read_parquet(file)

    base_name = os.path.basename(file)

    # ==================================================
    # Variables
    # ==================================================

    variables_plot = [

        'trip_distance',
        'fare_amount',
        'tip_amount'

    ]

    titulos = [

        'Distancia del viaje',
        'Tarifa base',
        'Propina'

    ]

    color_uai = '#7B1C2E'

    # ==================================================
    # HISTOGRAMAS
    # ==================================================

    print("📊 Generando histogramas")

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 4)
    )

    for i, (var, titulo) in enumerate(
        zip(variables_plot, titulos)
    ):

        axes[i].hist(

            df[var],

            bins=50,

            color=color_uai,

            edgecolor='black',

            alpha=0.8

        )

        axes[i].set_title(

            titulo,

            fontsize=11,

            fontweight='bold'
        )

        axes[i].set_xlabel(var)

        axes[i].set_ylabel(
            'Frecuencia'
        )

        axes[i].grid(
            True,
            alpha=0.3
        )

    plt.suptitle(

        'Distribución de variables numéricas (post-limpieza)',

        fontsize=13,

        fontweight='bold',

        y=1.02
    )

    plt.tight_layout()

    histogram_output = (

        f"{OUTPUT_DIR}/"

        f"{base_name.replace('.parquet', '_histograms.png')}"
    )

    plt.savefig(

        histogram_output,

        dpi=150,

        bbox_inches='tight'
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
        3,
        figsize=(15, 5)
    )

    for i, (var, titulo) in enumerate(
        zip(variables_plot, titulos)
    ):

        axes[i].boxplot(

            df[var],

            patch_artist=True,

            boxprops=dict(
                facecolor='#7B1C2E',
                alpha=0.7
            ),

            medianprops=dict(
                color='white',
                linewidth=2
            ),

            flierprops=dict(
                marker='o',
                markerfacecolor='#A52A4A',
                markersize=3,
                alpha=0.5
            ),

            tick_labels=['']

        )

        axes[i].set_title(

            titulo,

            fontsize=11,

            fontweight='bold'
        )

        axes[i].set_ylabel(var)

        axes[i].grid(
            True,
            alpha=0.3,
            axis='y'
        )

    plt.suptitle(

        'Boxplots de variables numéricas — Detección visual de outliers',

        fontsize=13,

        fontweight='bold',

        y=1.02
    )

    plt.tight_layout()

    boxplot_output = (

        f"{OUTPUT_DIR}/"

        f"{base_name.replace('.parquet', '_boxplots.png')}"
    )

    plt.savefig(

        boxplot_output,

        dpi=150,

        bbox_inches='tight'
    )

    plt.close()

    print(
        f"✅ Boxplots guardados: "
        f"{boxplot_output}"
    )

    # ==================================================
    # NORMALIZACIÓN
    # ==================================================

    print("📏 Generando normalización")

    # --------------------------------------------------
    # Min-Max Scaling
    # --------------------------------------------------

    min_value = df['trip_distance'].min()

    max_value = df['trip_distance'].max()

    df['trip_distance_minmax'] = (

        (df['trip_distance'] - min_value)

        /

        (max_value - min_value)

    )

    # --------------------------------------------------
    # Z-score Standardization
    # --------------------------------------------------

    mean_value = df['trip_distance'].mean()

    std_value = df['trip_distance'].std()

    df['trip_distance_zscore'] = (

        (df['trip_distance'] - mean_value)

        /

        std_value

    )

    # ==================================================
    # GRÁFICO NORMALIZACIÓN
    # ==================================================

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    # ==================================================
    # ORIGINAL
    # ==================================================

    axes[0].boxplot(

        df['trip_distance'],

        patch_artist=True,

        boxprops=dict(
            facecolor='#7B1C2E',
            alpha=0.7
        ),

        medianprops=dict(
            color='white',
            linewidth=2
        ),

        flierprops=dict(
            marker='o',
            markerfacecolor='#A52A4A',
            markersize=3,
            alpha=0.5
        ),

        tick_labels=['']
    )

    axes[0].set_title(

        'Original (millas)\nrango: 0 — 100',

        fontsize=11,

        fontweight='bold'
    )

    axes[0].set_ylabel('Valor')

    axes[0].grid(
        True,
        alpha=0.3,
        axis='y'
    )

    # ==================================================
    # MIN-MAX
    # ==================================================

    axes[1].boxplot(

        df['trip_distance_minmax'],

        patch_artist=True,

        boxprops=dict(
            facecolor='#A52A4A',
            alpha=0.7
        ),

        medianprops=dict(
            color='white',
            linewidth=2
        ),

        flierprops=dict(
            marker='o',
            markerfacecolor='#C44569',
            markersize=3,
            alpha=0.5
        ),

        tick_labels=['']
    )

    axes[1].set_title(

        'Min-Max Scaling\nrango: [0, 1]',

        fontsize=11,

        fontweight='bold'
    )

    axes[1].set_ylabel(
        'Valor normalizado'
    )

    axes[1].grid(
        True,
        alpha=0.3,
        axis='y'
    )

    # ==================================================
    # Z-SCORE
    # ==================================================

    axes[2].boxplot(

        df['trip_distance_zscore'],

        patch_artist=True,

        boxprops=dict(
            facecolor='#C44569',
            alpha=0.7
        ),

        medianprops=dict(
            color='white',
            linewidth=2
        ),

        flierprops=dict(
            marker='o',
            markerfacecolor='#7B1C2E',
            markersize=3,
            alpha=0.5
        ),

        tick_labels=['']
    )

    axes[2].set_title(

        'Z-score Standardization\nμ=0, σ=1',

        fontsize=11,

        fontweight='bold'
    )

    axes[2].set_ylabel(
        'Desvíos estándar'
    )

    axes[2].grid(
        True,
        alpha=0.3,
        axis='y'
    )

    # ==================================================
    # TÍTULO GENERAL
    # ==================================================

    plt.suptitle(

        'Comparación de métodos de normalización — variable trip_distance',

        fontsize=13,

        fontweight='bold',

        y=1.02
    )

    plt.tight_layout()

    normalization_output = (

        f"{OUTPUT_DIR}/"

        f"{base_name.replace('.parquet', '_normalization.png')}"
    )

    plt.savefig(

        normalization_output,

        dpi=150,

        bbox_inches='tight'
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