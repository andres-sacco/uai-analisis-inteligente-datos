import pandas as pd
import glob
import os
import gc
import sys

# ==================================================
# Configuración
# ==================================================

INPUT_FILES = glob.glob(
    "data/raw/*.xlsx"
)

OUTPUT_DIR = "data/processed"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==================================================
# Verificar archivos
# ==================================================

if not INPUT_FILES:

    print(
        "❌ No se encontraron archivos XLSX"
    )

    print(
        "📂 Path buscado: data/raw/*.xlsx"
    )

    sys.exit(1)

print(
    f"✅ Archivos encontrados: "
    f"{len(INPUT_FILES)}"
)

# ==================================================
# Métricas globales
# ==================================================

total_original = 0
total_final = 0
total_duplicates = 0
total_removed_geo = 0

# ==================================================
# Procesar archivos
# ==================================================

for file in INPUT_FILES:

    print(f"\n📂 Procesando {file}")

    try:

        df = pd.read_excel(
            file,
            sheet_name="HECHOS"
        )

    except Exception as e:

        print(
            f"❌ Error leyendo sheet HECHOS: {e}"
        )

        continue

    original_count = len(df)

    total_original += original_count

    print(
        f"📊 Registros originales: "
        f"{original_count:,}"
    )

    # ==================================================
    # Eliminar filas vacías
    # ==================================================

    before_null_rows = len(df)

    df = df.dropna(
        how="all"
    )

    removed_null_rows = (
        before_null_rows - len(df)
    )

    print(
        f"🧹 Filas vacías eliminadas: "
        f"{removed_null_rows:,}"
    )

    # ==================================================
    # Eliminar registros sin ID
    # ==================================================

    if "id_siniestro" in df.columns:

        before_id = len(df)

        df = df.dropna(
            subset=["id_siniestro"]
        )

        removed_id = (
            before_id - len(df)
        )

        print(
            f"🧹 Registros sin ID: "
            f"{removed_id:,}"
        )


    # ==================================================
    # Conversión de fechas
    # ==================================================

    if "fecha_siniestro" in df.columns:

        df["fecha_siniestro"] = (
            pd.to_datetime(
                df["fecha_siniestro"],
                errors="coerce"
            )
        )

    # ==================================================
    # Conversión numérica
    # ==================================================

    numeric_columns = [

        "numero_total_de_victimas",
        "numero_victimas_leve_siniestro",
        "numero_victimas_grave_siniestro",
        "numero_victimas_mortal_siniestro",
        "anio_siniestro",
        "mes_siniestro",
        "dia_siniestro",
        "comuna_siniestro",
        "longitud_siniestro",
        "latitud_siniestro"

    ]

    for col in numeric_columns:

        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # ==================================================
    # Imputación de víctimas faltantes
    # ==================================================

    victim_columns = [

        "numero_total_de_victimas",
        "numero_victimas_leve_siniestro",
        "numero_victimas_grave_siniestro",
        "numero_victimas_mortal_siniestro"

    ]

    for col in victim_columns:

        if col in df.columns:
            df[col] = (

                df[col]

                .replace(
                    [
                        "SD",
                        "sd",
                        "S/D",
                        "s/d",
                        "SIN DATO",
                        "Sin dato",
                        ""
                    ],
                    0
                )

            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            df[col] = (
                df[col]
                .fillna(0)
                .astype(int)
            )

    # ==================================================
    # Hora del siniestro
    # Algunos registros vienen con formato HH:MM
    # ==================================================

    if "rango_horario" in df.columns:
        df["hora_siniestro"] = pd.to_numeric(
            df["rango_horario"]
            .astype(str)
            .str.extract(r"(\d+)")[0],
            errors="coerce"
        ).fillna(0).astype(int)

    # ==================================================
    # Otras columnas numéricas
    # ==================================================

    other_numeric_columns = [

        "comuna_siniestro",
        "latitud_siniestro",
        "longitud_siniestro"

    ]

    for col in other_numeric_columns:

        if col in df.columns:
            df[col] = (
                df[col]
                .fillna(0)
            )
    # ==================================================
    # Eliminar duplicados
    # ==================================================

    if "id_siniestro" in df.columns:

        before_duplicates = len(df)

        df = df.drop_duplicates(
            subset=["id_siniestro"]
        )

        duplicates_removed = (
            before_duplicates - len(df)
        )

    else:

        before_duplicates = len(df)

        df = df.drop_duplicates()

        duplicates_removed = (
            before_duplicates - len(df)
        )

    total_duplicates += (
        duplicates_removed
    )

    print(
        f"❌ Duplicados eliminados: "
        f"{duplicates_removed:,}"
    )

    # ==================================================
    # Coordenadas inválidas
    # ==================================================

    if (
        "latitud_siniestro" in df.columns
        and
        "longitud_siniestro" in df.columns
    ):

        before_geo = len(df)

        df = df[
            (
                df["latitud_siniestro"]
                .between(-90, 90)
            )
            &
            (
                df["longitud_siniestro"]
                .between(-180, 180)
            )
        ]

        removed_geo = (
            before_geo - len(df)
        )

        total_removed_geo += (
            removed_geo
        )

        print(
            f"🧹 Coordenadas inválidas eliminadas: "
            f"{removed_geo:,}"
        )

    # ==================================================
    # Normalizar campos categóricos
    # ==================================================

    text_columns = [

        "rango_horario",
        "direccion_normalizada_siniestro",
        "tipo_de_via_siniestro",
        "participantes_siniestro",
        "modo_desplazamiento_victima",
        "contraparte_siniestro",
        "gravedad_siniestro"

    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna("DESCONOCIDO")
                .astype(str)
                .str.upper()
                .str.strip()
            )

    # ==================================================
    # Imputación general de texto
    # ==================================================

    object_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for col in object_columns:

        df[col] = (
            df[col]
            .fillna("DESCONOCIDO")
            .astype(str)
            .str.strip()
        )

    # ==================================================
    # Variables temporales
    # ==================================================

    if "fecha_siniestro" in df.columns:

        df["dia_semana"] = (
            df["fecha_siniestro"]
            .dt.dayofweek
        )

        df["mes"] = (
            df["fecha_siniestro"]
            .dt.month
        )

        df["anio"] = (
            df["fecha_siniestro"]
            .dt.year
        )

        df["trimestre"] = (
            df["fecha_siniestro"]
            .dt.quarter
        )

        df["fin_de_semana"] = (
            df["dia_semana"]
            .isin([5, 6])
            .astype(int)
        )

    # ==================================================
    # Eliminar columnas completamente vacías
    # ==================================================

    df = df.dropna(
        axis=1,
        how="all"
    )

    # ==================================================
    # Resultado final
    # ==================================================

    final_count = len(df)

    total_final += final_count

    print(
        f"✅ Registros finales: "
        f"{final_count:,}"
    )

    # ==================================================
    # Guardar CSV limpio
    # ==================================================

    file_name = os.path.basename(
        file
    )

    output_name = (
        file_name.replace(
            ".xlsx",
            "_hechos_clean.csv"
        )
    )

    output_path = (
        f"{OUTPUT_DIR}/{output_name}"
    )

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

    print(
        f"💾 Guardado: "
        f"{output_path}"
    )

    # ==================================================
    # Liberar memoria
    # ==================================================

    del df

    gc.collect()

    print(
        "🧹 Memoria liberada"
    )

# ==================================================
# Resumen global
# ==================================================

print("\n==============================")
print("📈 RESUMEN DE LIMPIEZA")
print("==============================")

print(
    f"📊 Registros originales: "
    f"{total_original:,}"
)

print(
    f"❌ Duplicados eliminados: "
    f"{total_duplicates:,}"
)

print(
    f"❌ Coordenadas inválidas: "
    f"{total_removed_geo:,}"
)

print(
    f"✅ Registros finales: "
    f"{total_final:,}"
)

removed_total = (
    total_original - total_final
)

print(
    f"🧹 Total eliminados: "
    f"{removed_total:,}"
)

if total_original > 0:

    clean_percentage = (
        total_final
        / total_original
    ) * 100

    print(
        f"✨ % conservación: "
        f"{clean_percentage:.2f}%"
    )