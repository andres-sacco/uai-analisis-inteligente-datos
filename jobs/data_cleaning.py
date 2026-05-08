import pandas as pd
import glob
import os
import gc

INPUT_FILES = glob.glob("data/raw/*.parquet")

OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

total_original = 0
total_final = 0
total_removed_duration = 0
total_removed_distance = 0
total_duplicates = 0

for file in INPUT_FILES:

    print(f"\n📂 Procesando {file}")

    df = pd.read_parquet(file)

    original_count = len(df)

    total_original += original_count

    print(f"📊 Registros originales: {original_count}")

    # =========================
    # Fechas
    # =========================
    df['tpep_pickup_datetime'] = pd.to_datetime(
        df['tpep_pickup_datetime']
    )

    df['tpep_dropoff_datetime'] = pd.to_datetime(
        df['tpep_dropoff_datetime']
    )

    # =========================
    # Duración
    # =========================
    df['trip_duration'] = (
        df['tpep_dropoff_datetime']
        - df['tpep_pickup_datetime']
    ).dt.total_seconds() / 60

    # =========================
    # Invalid duration
    # =========================
    invalid_duration = df[
        df['trip_duration'] <= 1
    ]

    removed_duration = len(invalid_duration)

    total_removed_duration += removed_duration

    df = df[df['trip_duration'] > 1]

    # =========================
    # Invalid distance
    # =========================
    invalid_distance = df[
        df['trip_distance'] <= 0
    ]

    removed_distance = len(invalid_distance)

    total_removed_distance += removed_distance

    df = df[df['trip_distance'] > 0]

    # =========================
    # Duplicados
    # =========================
    before_duplicates = len(df)

    df = df.drop_duplicates()

    duplicates_removed = (
        before_duplicates - len(df)
    )

    total_duplicates += duplicates_removed

    # =========================
    # Nulos
    # =========================
    df['passenger_count'] = (
        df['passenger_count'].fillna(1)
    )

    df['tip_amount'] = (
        df['tip_amount'].fillna(0)
    )

    # =========================
    # Features
    # =========================
    df['hour'] = (
        df['tpep_pickup_datetime'].dt.hour
    )

    df['day_of_week'] = (
        df['tpep_pickup_datetime'].dt.dayofweek
    )

    # =========================
    # Resultado final
    # =========================
    final_count = len(df)

    total_final += final_count

    print(f"✅ Registros finales: {final_count}")

    # =========================
    # Guardar
    # =========================
    file_name = os.path.basename(file)

    output_path = (
        f"{OUTPUT_DIR}/clean_{file_name}"
    )

    df.to_parquet(output_path, index=False)

    print(f"💾 Guardado: {output_path}")

    # =========================
    # Liberar memoria
    # =========================
    del df

    gc.collect()

# =========================
# Resumen global
# =========================
print("\n==============================")
print("📈 RESUMEN DE LIMPIEZA")
print("==============================")

print(f"📊 Registros originales: {total_original}")
print(f"❌ Eliminados duración: {total_removed_duration}")
print(f"❌ Eliminados distancia: {total_removed_distance}")
print(f"❌ Duplicados eliminados: {total_duplicates}")
print(f"✅ Registros finales: {total_final}")

removed_total = total_original - total_final

print(f"🧹 Total eliminados: {removed_total}")

clean_percentage = (
    (total_final / total_original) * 100
)

print(f"✨ % conservación: {clean_percentage:.2f}%")