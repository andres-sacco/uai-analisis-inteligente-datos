import os
import requests

YEAR = os.getenv("YEAR", "2025")

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for month in range(1, 13):

    month_str = str(month).zfill(2)

    file_name = f"yellow_tripdata_{YEAR}-{month_str}.parquet"

    url = f"{BASE_URL}/{file_name}"

    output_path = f"{OUTPUT_DIR}/{file_name}"

    # Evitar descargar de nuevo
    if os.path.exists(output_path):
        print(f"✔ Ya existe: {file_name}")
        continue

    print(f"⬇️ Descargando {file_name}")

    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Descargado: {file_name}")

        else:
            print(f"❌ Error {response.status_code}: {file_name}")

    except Exception as e:
        print(f"❌ Error descargando {file_name}: {e}")

print("🎉 Descarga anual completada")