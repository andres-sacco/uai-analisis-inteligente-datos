import os
import requests

YEAR = os.getenv("YEAR", "2025")

# Opcional
MONTH = os.getenv("MONTH")

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# Determinar meses a descargar
# ==================================================

if MONTH:

    months = [int(MONTH)]

    print(
        f"📅 Descargando únicamente "
        f"{YEAR}-{MONTH}"
    )

else:

    months = range(1, 13)

    print(
        f"📅 Descargando todos los meses "
        f"del año {YEAR}"
    )

# ==================================================
# Descargar archivos
# ==================================================

for month in months:

    month_str = str(month).zfill(2)

    file_name = (
        f"yellow_tripdata_{YEAR}-{month_str}.parquet"
    )

    url = f"{BASE_URL}/{file_name}"

    output_path = (
        f"{OUTPUT_DIR}/{file_name}"
    )

    # ==================================================
    # Evitar descarga duplicada
    # ==================================================

    if os.path.exists(output_path):

        print(f"✔ Ya existe: {file_name}")

        continue

    print(f"⬇️ Descargando {file_name}")

    try:

        response = requests.get(
            url,
            stream=True
        )

        if response.status_code == 200:

            with open(output_path, "wb") as f:

                for chunk in response.iter_content(
                    chunk_size=8192
                ):

                    f.write(chunk)

            print(f"✅ Descargado: {file_name}")

        else:

            print(
                f"❌ Error "
                f"{response.status_code}: "
                f"{file_name}"
            )

    except Exception as e:

        print(
            f"❌ Error descargando "
            f"{file_name}: {e}"
        )

print("🎉 Descarga completada")