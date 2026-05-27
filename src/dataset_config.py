"""
Dataset metadata (delimiter, column mappings) shared across the app.
Kept in a standalone module to avoid circular imports between lectura, validaciones, and ui_state.
"""

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
