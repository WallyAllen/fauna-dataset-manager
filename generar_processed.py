"""
Genera los archivos procesados en processed_datasets/ a partir de los datasets crudos.
Debe ejecutarse una vez antes de iniciar la aplicación Streamlit.
"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.eliminaciones import sanitizar_dataset
from src.dataset_config import PROCESSED_DATASETS_DIR, DATASET_PROCESSED_FILES

RAW_DATASETS = {
    "iadiza":      PROJECT_ROOT / "raw_datasets" / "iadiza"      / "occurrence.txt",
    "inaturalist": PROJECT_ROOT / "raw_datasets" / "inaturalist" / "observations.csv",
    "xenocanto":   PROJECT_ROOT / "raw_datasets" / "xeno_canto"  / "Occurrence.txt",
}


def main():
    PROCESSED_DATASETS_DIR.mkdir(exist_ok=True)

    for nombre, ruta_entrada in RAW_DATASETS.items():
        ruta_salida = PROCESSED_DATASETS_DIR / DATASET_PROCESSED_FILES[nombre]

        if not ruta_entrada.exists():
            print(f"[{nombre}] Archivo crudo no encontrado: {ruta_entrada}. Saltando.")
            continue

        print(f"\n[{nombre}] Procesando {ruta_entrada.name}...")
        sanitizar_dataset(nombre, str(ruta_entrada), str(ruta_salida))

    print("\nProceso finalizado. Archivos disponibles en processed_datasets/.")


if __name__ == "__main__":
    main()
