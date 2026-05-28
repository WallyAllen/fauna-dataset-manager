"""
Metadatos del dataset (delimitador, columnas) compartidos en toda la app.   
Guardados en un módulo aparte para evitar circular imports.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATASETS_DIR = PROJECT_ROOT / "processed_datasets"

# PENDIENTE DE REVISAR!!!!!!!!!! ALERTA DE ROCCO. SI ESTÁS LEYENDO ESTO CERCA DE LA PRESENTACIÓN ES PORQUE ESTAMOS AL HORNO
DATASET_PROCESSED_FILES = {
    "iadiza": "iadiza_insertado.txt",
    "inaturalist": "inaturalist_insertado.csv",
    "xenocanto": "xenocanto_insertado.txt",
}

TRADUCTOR_DATASETS = {
    'iadiza': {
        'delimitador': '\t',
        'latitud': 'decimalLatitude',
        'longitud': 'decimalLongitude',
        'fecha': ['eventDate', 'dateIdentified', 'modified', 'georeferencedDate'],
        'id': 'gbifID',
        'pais': 'countryCode',
        'tipo_pais': 'alpha_2',
        'coordenada_rango': '',
        'taxonomica': [
            'scientificName', 'kingdom', 'phylum',
            'class', 'order', 'family', 'genus',
            'specificEpithet', 'taxonRank',
        ],
    },
    'inaturalist': {
        'delimitador': ',',
        'latitud': 'decimalLatitude',
        'longitud': 'decimalLongitude',
        'fecha': ['eventDate', 'dateIdentified', 'modified'],
        'id': 'id',
        'pais': 'countryCode',
        'tipo_pais': 'alpha_2',
        'coordenada_rango': 'coordinateUncertaintyInMeters',
        'taxonomica': [
            'scientificName', 'taxonID',
            'taxonRank', 'kingdom', 'phylum',
            'class', 'order', 'family', 'genus',
        ],
    },
    'xenocanto': {
        'delimitador': ',',
        'latitud': 'latitudeDecimal',
        'longitud': 'longitudeDecimal',
        'fecha': ['eventDate'],
        'id': 'id',
        'pais': 'country',
        'tipo_pais': 'nombre',
        'coordenada_rango': '',
        'taxonomica': [
            'scientificName', 'specificEpithet', 'infraspecificEpithet',
            'taxonRank', 'kingdom', 'higherClassification',
            'family', 'genus', 'nomenclaturalCode',
            'vernacularName', 'identificationRemarks',
        ],
    },
}


def get_dataset_filepath(dataset_name):
    """
    Devuelve la ruta al archivo procesado del dataset en processed_datasets/.
    """
    if dataset_name not in DATASET_PROCESSED_FILES:
        raise ValueError(
            f"Dataset '{dataset_name}' no reconocido. "
            f"Opciones válidas: {list(DATASET_PROCESSED_FILES.keys())}"
        )
    return PROCESSED_DATASETS_DIR / DATASET_PROCESSED_FILES[dataset_name]

def get_dataset_config(dataset_name):
    """
    Valida el nombre del dataset y retorna su configuración.
    """
    if dataset_name not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset_name}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    return TRADUCTOR_DATASETS[dataset_name]