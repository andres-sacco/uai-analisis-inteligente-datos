import pandas as pd
import glob
import os
import gc

INPUT_FILES = glob.glob("data/processed/*.parquet")

OUTPUT_DIR = "data/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

aggregated_results = []

for file in INPUT_FILES:

    print(f"📂 Agregando {file}")

    # =========================
    # Leer parquet procesado
    # =========================
    df = pd.read_parquet(file)

    # =========================
    # Agregaciones
    # =========================
    result = (
        df.groupby("hour")
          .agg(
              total_trips=("hour", "count"),
              avg_distance=("trip_distance", "mean"),
              avg_tip=("tip_amount", "mean")
          )
          .reset_index()
    )

    aggregated_results.append(result)

    # =========================
    # Liberar memoria
    # =========================
    del df

    gc.collect()

    print("🧹 Memoria liberada")

# =========================
# Combinar agregaciones
# =========================
final_result = pd.concat(
    aggregated_results,
    ignore_index=True
)

# =========================
# Reagrupar
# (porque cada mes tiene su propia agregación)
# =========================
final_result = (
    final_result.groupby("hour")
    .agg(
        total_trips=("total_trips", "sum"),
        avg_distance=("avg_distance", "mean"),
        avg_tip=("avg_tip", "mean")
    )
    .reset_index()
)

# =========================
# Guardar
# =========================
output_file = (
    f"{OUTPUT_DIR}/aggregated_full_year.parquet"
)

final_result.to_parquet(output_file, index=False)

print(f"✅ Resultado guardado: {output_file}")