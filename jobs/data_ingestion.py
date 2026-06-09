import os
import requests

# ==================================================
# Dataset Víctimas de Siniestros Viales
# ==================================================

DATASET_URL = (
    "https://data.buenosaires.gob.ar/dataset/"
    "victimas-siniestros-viales/resource/"
    "79914119-0e1e-47c6-9f7b-f1f7bf542786/download"
)

OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# Nombre archivo
# ==================================================

output_file = (
    f"{OUTPUT_DIR}/victimas_siniestros_viales.xlsx"
)

# ==================================================
# Verificar existencia
# ==================================================

if os.path.exists(output_file):

    print(
        f"✔ Archivo ya existe: "
        f"{output_file}"
    )

else:

    print("⬇️ Descargando dataset")

    try:

        response = requests.get(
            DATASET_URL,
            stream=True,
            timeout=60
        )

        if response.status_code == 200:

            with open(output_file, "wb") as f:

                for chunk in response.iter_content(
                    chunk_size=8192
                ):
                    if chunk:
                        f.write(chunk)

            print(
                f"✅ Dataset descargado: "
                f"{output_file}"
            )

        else:

            print(
                f"❌ Error HTTP: "
                f"{response.status_code}"
            )

    except Exception as e:

        print(
            f"❌ Error descargando dataset: {e}"
        )

print("🎉 Descarga completada")