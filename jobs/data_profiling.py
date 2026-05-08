import pandas as pd
import glob
import os
import sys
import gc
import time

INPUT_FILES = glob.glob("data/raw/*.parquet")

OUTPUT_DIR = "data/reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# Verificar archivos
# ==================================================

if not INPUT_FILES:

    print("❌ No se encontraron archivos parquet")
    print("📂 Path buscado: data/raw/*.parquet")

    sys.exit(1)

print(f"✅ Archivos encontrados: {len(INPUT_FILES)}")

# ==================================================
# Procesar archivo por archivo
# ==================================================

for file in INPUT_FILES:

    start_time = time.time()

    print("\n==============================")
    print(f"📂 Procesando {file}")
    print("==============================")

    # ==================================================
    # Leer parquet
    # ==================================================

    df = pd.read_parquet(file)

    print(f"📊 Total registros: {len(df)}")

    # ==================================================
    # Uso memoria
    # ==================================================

    memory_usage_mb = (
        df.memory_usage(deep=True).sum()
        / 1024**2
    )

    print(f"🧠 Memoria usada: {memory_usage_mb:.2f} MB")

    # ==================================================
    # Reporte consolidado
    # ==================================================

    profile_rows = []

    # ==================================================
    # Columnas numéricas
    # ==================================================

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for col in numeric_columns:

        print(f"\n📈 Analizando columna numérica: {col}")

        mode = (
            df[col].mode().iloc[0]
            if not df[col].mode().empty
            else None
        )

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        outliers = df[
            (df[col] < (Q1 - 1.5 * IQR)) |
            (df[col] > (Q3 + 1.5 * IQR))
        ]

        outlier_percentage = (
            len(outliers) / len(df)
        ) * 100

        profile_rows.append({

            # ==================================================
            # Identidad
            # ==================================================

            "column": col,
            "dtype": str(df[col].dtype),

            # ==================================================
            # Calidad
            # ==================================================

            "count": df[col].count(),

            "null_count": (
                df[col].isnull().sum()
            ),

            "null_percentage": (
                df[col].isnull().mean() * 100
            ),

            "unique_values": (
                df[col].nunique()
            ),

            "zero_percentage": (
                (df[col] == 0).mean() * 100
            ),

            "negative_percentage": (
                (df[col] < 0).mean() * 100
            ),

            "outlier_percentage": (
                outlier_percentage
            ),

            # ==================================================
            # Tendencia central
            # ==================================================

            "mean": df[col].mean(),
            "median": df[col].median(),
            "mode": str(mode),

            # ==================================================
            # Dispersión
            # ==================================================

            "std_dev": df[col].std(),
            "variance": df[col].var(),

            # ==================================================
            # Distribución
            # ==================================================

            "skewness": df[col].skew(),
            "kurtosis": df[col].kurtosis(),

            # ==================================================
            # Rangos y percentiles
            # ==================================================

            "min": df[col].min(),

            "p25": df[col].quantile(0.25),
            "p50": df[col].quantile(0.50),
            "p75": df[col].quantile(0.75),

            "p90": df[col].quantile(0.90),
            "p95": df[col].quantile(0.95),
            "p99": df[col].quantile(0.99),

            "max": df[col].max()
        })

    # ==================================================
    # Columnas categóricas
    # ==================================================

    categorical_columns = df.select_dtypes(
        exclude=["number", "object"]
    ).columns

    for col in categorical_columns:

        print(f"\n📝 Analizando columna categórica: {col}")

        mode = (
            df[col].mode().iloc[0]
            if not df[col].mode().empty
            else None
        )

        profile_rows.append({

            # ==================================================
            # Identidad
            # ==================================================

            "column": col,
            "dtype": str(df[col].dtype),

            # ==================================================
            # Calidad
            # ==================================================

            "count": df[col].count(),

            "null_count": (
                df[col].isnull().sum()
            ),

            "null_percentage": (
                df[col].isnull().mean() * 100
            ),

            "unique_values": (
                df[col].nunique()
            ),

            "zero_percentage": None,
            "negative_percentage": None,
            "outlier_percentage": None,

            # ==================================================
            # Tendencia central
            # ==================================================

            "mean": None,
            "median": None,
            "mode": str(mode),

            # ==================================================
            # Dispersión
            # ==================================================

            "std_dev": None,
            "variance": None,

            # ==================================================
            # Distribución
            # ==================================================

            "skewness": None,
            "kurtosis": None,

            # ==================================================
            # Rangos
            # ==================================================

            "min": df[col].min(),

            "p25": None,
            "p50": None,
            "p75": None,

            "p90": None,
            "p95": None,
            "p99": None,

            "max": df[col].max()
        })

    # ==================================================
    # DataFrame consolidado
    # ==================================================

    profile_df = pd.DataFrame(profile_rows)

    # ==================================================
    # Orden columnas
    # ==================================================

    ordered_columns = [

        # ==================================================
        # Identidad
        # ==================================================

        "column",
        "dtype",

        # ==================================================
        # Calidad
        # ==================================================

        "count",
        "null_count",
        "null_percentage",
        "unique_values",
        "zero_percentage",
        "negative_percentage",
        "outlier_percentage",

        # ==================================================
        # Tendencia central
        # ==================================================

        "mean",
        "median",
        "mode",

        # ==================================================
        # Dispersión
        # ==================================================

        "std_dev",
        "variance",

        # ==================================================
        # Distribución
        # ==================================================

        "skewness",
        "kurtosis",

        # ==================================================
        # Rangos y percentiles
        # ==================================================

        "min",
        "p25",
        "p50",
        "p75",
        "p90",
        "p95",
        "p99",
        "max"
    ]

    profile_df = profile_df[ordered_columns]

    print("\n📋 REPORTE CONSOLIDADO")
    print(profile_df)

    # ==================================================
    # Duplicados dataset
    # ==================================================

    duplicates = df.duplicated().sum()

    duplicate_percentage = (
        duplicates / len(df)
    ) * 100

    print("\n📋 DUPLICADOS DATASET")

    print(f"❌ Registros duplicados: {duplicates}")

    print(
        f"❌ % duplicados: "
        f"{duplicate_percentage:.2f}%"
    )

    # ==================================================
    # Dataset shape
    # ==================================================

    print("\n📦 DATASET")

    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    # ==================================================
    # Métricas temporales
    # ==================================================

    if "tpep_pickup_datetime" in df.columns:

        print("\n📅 RANGO TEMPORAL")

        print(
            f"Inicio: "
            f"{df['tpep_pickup_datetime'].min()}"
        )

        print(
            f"Fin: "
            f"{df['tpep_pickup_datetime'].max()}"
        )

    # ==================================================
    # Nombre reporte
    # ==================================================

    base_name = os.path.basename(file)

    report_name = (
        base_name.replace(
            ".parquet",
            "_profile.csv"
        )
    )

    output_file = (
        f"{OUTPUT_DIR}/{report_name}"
    )

    # ==================================================
    # Guardar reporte
    # ==================================================

    profile_df.to_csv(
        output_file,
        index=False
    )

    print(f"\n💾 Reporte guardado en {output_file}")

    # ==================================================
    # Tiempo procesamiento
    # ==================================================

    end_time = time.time()

    processing_time = (
        end_time - start_time
    )

    print(
        f"⏱ Tiempo procesamiento: "
        f"{processing_time:.2f} segundos"
    )

    # ==================================================
    # Liberar memoria
    # ==================================================

    del df
    del profile_df
    del profile_rows

    gc.collect()

    print("🧹 Memoria liberada")

print("\n🎉 Profiling completo")
