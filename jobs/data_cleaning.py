import pandas as pd
import glob
import os
import gc

INPUT_FILES = glob.glob("data/raw/*.parquet")

OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# Métricas globales
# ==================================================

total_original = 0
total_final = 0

total_removed_duration = 0
total_removed_invalid = 0
total_removed_extreme = 0
total_duplicates = 0

# ==================================================
# Procesar archivos
# ==================================================

for file in INPUT_FILES:

    print(f"\n📂 Procesando {file}")

    df = pd.read_parquet(file)

    original_count = len(df)

    total_original += original_count

    print(f"📊 Registros originales: {original_count:,}")

    # ==================================================
    # Fechas
    # ==================================================

    df['tpep_pickup_datetime'] = pd.to_datetime(
        df['tpep_pickup_datetime']
    )

    df['tpep_dropoff_datetime'] = pd.to_datetime(
        df['tpep_dropoff_datetime']
    )

    # ==================================================
    # Duración viaje
    # ==================================================

    df['trip_duration'] = (
        df['tpep_dropoff_datetime']
        - df['tpep_pickup_datetime']
    ).dt.total_seconds() / 60

    # ==================================================
    # Duraciones inválidas
    # ==================================================

    invalid_duration = df[
        df['trip_duration'] <= 1
    ]

    removed_duration = len(invalid_duration)

    total_removed_duration += removed_duration

    df = df[
        df['trip_duration'] > 1
    ]

    print(
        f"❌ Duraciones inválidas eliminadas: "
        f"{removed_duration:,}"
    )

    # ==================================================
    # Filtrado de valores inválidos
    # ==================================================

    filas_antes = len(df)

    print(
        f"\n📊 Filas antes filtrado: "
        f"{filas_antes:,}"
    )

    # ==================================================
    # Valores inválidos
    # ==================================================

    df = df[

        (df['trip_distance'] > 0) &

        (df['fare_amount'] >= 0) &

        (df['tip_amount'] >= 0) &

        (df['total_amount'] >= 0)

    ].copy()

    filas_post_invalidos = len(df)

    eliminadas_invalidos = (
        filas_antes - filas_post_invalidos
    )

    total_removed_invalid += (
        eliminadas_invalidos
    )

    print(
        f"🧹 Eliminados por valores inválidos: "
        f"{eliminadas_invalidos:,} "
        f"({(eliminadas_invalidos / filas_antes) * 100:.2f}%)"
    )

    # ==================================================
    # Valores físicamente imposibles
    # ==================================================

    df = df[

        (df['trip_distance'] <= 100) &

        (df['fare_amount'] <= 500) &

        (df['tip_amount'] <= 200)

    ].copy()

    filas_post_extremos = len(df)

    eliminadas_extremos = (
        filas_post_invalidos
        - filas_post_extremos
    )

    total_removed_extreme += (
        eliminadas_extremos
    )

    print(
        f"🧹 Eliminados por valores extremos imposibles: "
        f"{eliminadas_extremos:,} "
        f"({(eliminadas_extremos / filas_antes) * 100:.4f}%)"
    )

    # ==================================================
    # Totales limpieza
    # ==================================================

    print(
        f"\n📊 Filas después limpieza: "
        f"{filas_post_extremos:,}"
    )

    print(
        f"🧹 Total eliminadas: "
        f"{filas_antes - filas_post_extremos:,} "
        f"({((filas_antes - filas_post_extremos) / filas_antes) * 100:.2f}%)"
    )

    # ==================================================
    # Duplicados
    # ==================================================

    before_duplicates = len(df)

    df = df.drop_duplicates()

    duplicates_removed = (
        before_duplicates - len(df)
    )

    total_duplicates += duplicates_removed

    print(
        f"\n❌ Duplicados eliminados: "
        f"{duplicates_removed:,}"
    )

    # ==================================================
    # Imputación de valores faltantes
    # ==================================================

    print("\n🧹 Imputando valores faltantes")

    # passenger_count

    if 'passenger_count' in df.columns:

        df['passenger_count'] = (
            df['passenger_count']
            .fillna(1)
        )

    # RatecodeID

    if 'RatecodeID' in df.columns:

        df['RatecodeID'] = (
            df['RatecodeID']
            .fillna(1)
        )

    # store_and_fwd_flag

    if 'store_and_fwd_flag' in df.columns:

        df['store_and_fwd_flag'] = (
            df['store_and_fwd_flag']
            .fillna('N')
        )

    # congestion_surcharge

    if 'congestion_surcharge' in df.columns:

        df['congestion_surcharge'] = (
            df['congestion_surcharge']
            .fillna(0)
        )

    # Airport_fee

    if 'Airport_fee' in df.columns:

        df['Airport_fee'] = (
            df['Airport_fee']
            .fillna(0)
        )

    # tip_amount

    if 'tip_amount' in df.columns:

        df['tip_amount'] = (
            df['tip_amount']
            .fillna(0)
        )

    # ==================================================
    # Verificación post imputación
    # ==================================================

    columnas_imputadas = [

        'passenger_count',
        'RatecodeID',
        'store_and_fwd_flag',
        'congestion_surcharge',
        'Airport_fee',
        'tip_amount'
    ]

    columnas_existentes = [

        col for col in columnas_imputadas
        if col in df.columns
    ]

    print("\n✅ Verificación post-imputación")

    print(
        df[columnas_existentes]
        .isnull()
        .sum()
    )

    # ==================================================
    # Feature Engineering
    # ==================================================

    print("\n⚙️ Generando features")

    df['hour'] = (
        df['tpep_pickup_datetime']
        .dt.hour
    )

    df['day_of_week'] = (
        df['tpep_pickup_datetime']
        .dt.dayofweek
    )

    # ==================================================
    # Resultado final
    # ==================================================

    final_count = len(df)

    total_final += final_count

    print(f"\n✅ Registros finales: {final_count:,}")

    # ==================================================
    # Guardar archivo limpio
    # ==================================================

    file_name = os.path.basename(file)

    output_path = (
        f"{OUTPUT_DIR}/clean_{file_name}"
    )

    df.to_parquet(
        output_path,
        index=False
    )

    print(f"💾 Guardado: {output_path}")

    # ==================================================
    # Liberar memoria
    # ==================================================

    del df

    gc.collect()

    print("🧹 Memoria liberada")

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
    f"❌ Eliminados duración inválida: "
    f"{total_removed_duration:,}"
)

print(
    f"❌ Eliminados valores inválidos: "
    f"{total_removed_invalid:,}"
)

print(
    f"❌ Eliminados valores extremos: "
    f"{total_removed_extreme:,}"
)

print(
    f"❌ Duplicados eliminados: "
    f"{total_duplicates:,}"
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

clean_percentage = (
    (total_final / total_original) * 100
)

print(
    f"✨ % conservación: "
    f"{clean_percentage:.2f}%"
)