import pandas as pd
import glob
import os
import gc
import sys

# ==================================================
# Configuración
# ==================================================

INPUT_FILES = glob.glob(
    "data/processed/*.csv"
)

OUTPUT_DIR = "data/reports"

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

# ==================================================
# Umbrales de calidad
# ==================================================

MAX_NULL_PERCENTAGE = 15
MAX_DUPLICATE_PERCENTAGE = 5

# ==================================================
# Valores especiales
# ==================================================

SPECIAL_VALUES = [

    "SD",
    "S/D",
    "SIN DATO",
    "N/A",
    "NA",
    "NULL",
    "-"

]

# ==================================================
# Valores especiales permitidos por columna
# (no serán considerados nulos)
# ==================================================

IGNORE_SPECIAL_VALUES = {

    "modo_desplazamiento_victima": [
        "SD"
    ],

    "contraparte_siniestro": [
        "SD"
    ]

}

# ==================================================
# Métricas globales
# ==================================================

global_rows = 0
global_duplicates = 0
global_nulls = 0

quality_errors = []

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

        na_values=SPECIAL_VALUES,

        keep_default_na=True

    )

    file_name = os.path.basename(file)

    total_rows = len(df)

    total_columns = len(df.columns)

    global_rows += total_rows

    print(f"📊 Filas: {total_rows:,}")
    print(f"📊 Columnas: {total_columns}")

    # ==================================================
    # Buscar valores especiales
    # ==================================================

    print("\n🔍 VALORES ESPECIALES DETECTADOS")

    special_report = []

    raw_df = pd.read_csv(
        file,
        low_memory=False
    )

    for col in raw_df.columns:

        try:

            serie = (

                raw_df[col]

                .astype(str)

                .str.strip()

                .str.upper()

            )

            for value in SPECIAL_VALUES:

                count = (
                    serie == value
                ).sum()

                if count > 0:

                    special_report.append({

                        "column": col,
                        "value": value,
                        "count": count

                    })

        except Exception:

            pass

    if special_report:

        special_df = pd.DataFrame(
            special_report
        )

        print(
            special_df.sort_values(
                ["column", "value"]
            )
        )

    else:

        print(
            "✅ No se encontraron valores especiales"
        )

    # ==================================================
    # Duplicados
    # ==================================================

    duplicate_count = (
        df.duplicated().sum()
    )

    duplicate_percentage = (

        duplicate_count
        / total_rows

    ) * 100

    global_duplicates += (
        duplicate_count
    )

    print("\n📌 DUPLICADOS")

    print(
        f"Cantidad: {duplicate_count:,}"
    )

    print(
        f"Porcentaje: {duplicate_percentage:.2f}%"
    )

    if (

        duplicate_percentage
        > MAX_DUPLICATE_PERCENTAGE

    ):

        quality_errors.append(

            f"{file_name} supera "
            f"el límite de duplicados "
            f"({duplicate_percentage:.2f}%)"

        )

    # ==================================================
    # NULOS
    # ==================================================

    print("\n📌 NULOS POR COLUMNA")

    # Nulos detectados por pandas
    null_counts = (
        df.isnull().sum()
    )

    # Ajustar nulos para valores especiales permitidos
    adjusted_null_counts = (
        null_counts.copy()
    )

    for column, allowed_values in (

        IGNORE_SPECIAL_VALUES.items()

    ):

        if column not in raw_df.columns:
            continue

        serie = (

            raw_df[column]

            .astype(str)

            .str.strip()

            .str.upper()

        )

        allowed_count = (

            serie.isin(

                [
                    value.upper()
                    for value in allowed_values
                ]

            )

            .sum()

        )

        adjusted_null_counts[column] = max(

            0,

            adjusted_null_counts[column]
            - allowed_count

        )

    null_percentages = (

        adjusted_null_counts
        / total_rows

    ) * 100

    quality_report = pd.DataFrame({

        "column":
            df.columns,

        "null_count":
            adjusted_null_counts.values,

        "null_percentage":
            null_percentages.values,

        "dtype":
            df.dtypes.astype(str).values,

        "unique_values":
            df.nunique().values

    })

    print(
        quality_report
    )

    file_nulls = (
        adjusted_null_counts.sum()
    )

    global_nulls += (
        file_nulls
    )

    # ==================================================
    # Columnas con exceso de nulos
    # ==================================================

    problematic_columns = (

        quality_report[

            quality_report[
                "null_percentage"
            ]

            > MAX_NULL_PERCENTAGE

        ]

    )

    if not problematic_columns.empty:

        print(
            "\n⚠️ Columnas con exceso de nulos"
        )

        print(
            problematic_columns
        )

        for _, row in (

            problematic_columns
            .iterrows()

        ):

            quality_errors.append(

                f"{file_name} -> "
                f"{row['column']} tiene "
                f"{row['null_percentage']:.2f}% "
                f"de nulos"

            )

    # ==================================================
    # Tipos de datos
    # ==================================================

    print("\n📌 TIPOS DE DATOS")

    dtype_summary = (

        df.dtypes

        .value_counts()

        .reset_index()

    )

    dtype_summary.columns = [

        "dtype",
        "count"

    ]

    print(
        dtype_summary
    )

    # ==================================================
    # Columnas constantes
    # ==================================================

    print("\n📌 COLUMNAS CONSTANTES")

    constant_columns = []

    for col in df.columns:

        unique_values = (

            df[col]

            .nunique(
                dropna=False
            )

        )

        if unique_values <= 1:

            constant_columns.append(
                col
            )

    if constant_columns:

        print(
            constant_columns
        )

    else:

        print(
            "✅ No se encontraron columnas constantes"
        )

    # ==================================================
    # Valores negativos
    # ==================================================

    print("\n📌 VALORES NEGATIVOS")

    numeric_columns = (

        df.select_dtypes(
            include=["number"]
        )

        .columns

    )

    negative_report = []

    for col in numeric_columns:

        negative_count = (

            (df[col] < 0)

            .sum()

        )

        negative_percentage = (

            negative_count
            / total_rows

        ) * 100

        if negative_count > 0:

            negative_report.append({

                "column":
                    col,

                "negative_count":
                    negative_count,

                "negative_percentage":
                    negative_percentage

            })

    if negative_report:

        negative_df = pd.DataFrame(
            negative_report
        )

        print(
            negative_df
        )

    else:

        print(
            "✅ No se encontraron valores negativos"
        )

    # ==================================================
    # Guardar reporte
    # ==================================================

    report_output = (

        f"{OUTPUT_DIR}/"

        f"{file_name.replace('.csv', '_quality.csv')}"

    )

    quality_report.to_csv(

        report_output,

        index=False

    )

    print(
        f"\n💾 Reporte guardado: "
        f"{report_output}"
    )

    # ==================================================
    # Liberar memoria
    # ==================================================

    del df
    del raw_df
    del quality_report

    if special_report:
        del special_df

    gc.collect()

    print(
        "🧹 Memoria liberada"
    )

# ==================================================
# Resumen global
# ==================================================

print("\n================================================")
print("📋 RESUMEN GLOBAL DE CALIDAD")
print("================================================")

print(
    f"📊 Total filas analizadas: "
    f"{global_rows:,}"
)

print(
    f"📊 Total duplicados: "
    f"{global_duplicates:,}"
)

print(
    f"📊 Total nulos: "
    f"{global_nulls:,}"
)

# ==================================================
# Resultado final
# ==================================================

if quality_errors:

    print(
        "\n❌ FALLAS DE CALIDAD DETECTADAS"
    )

    for error in quality_errors:

        print(
            f"- {error}"
        )

    sys.exit(1)

else:

    print(
        "\n✅ Calidad de datos OK"
    )