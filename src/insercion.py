import csv
from datetime import datetime
import pycountry
from validaciones import (
    TRADUCTOR_DATASETS,
    evaluar_error,
    LATITUD_NORTE,
    LATITUD_SUR,
    LONGITUD_ESTE,
    LONGITUD_OESTE
)

def create_record_structure(filepath, id_column='id', encoding='utf-8', delimiter='\t'):
    """
    Lee el encabezado del dataset y retorna un diccionario con sus columnas 
    (con valores vacíos por defecto) para representar la estructura de un nuevo registro.
    Se excluye la columna de identificación (ID) pasada por parámetro.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        columns = reader.fieldnames
        
    if not columns:
        return {}
        
    # Definimos la estructura como un diccionario excluyendo el ID
    record_structure = {col: '' for col in columns if col != id_column}
    
    return record_structure

def generate_empty_record(columns, id_column='id'):
    """
    Recibe una lista de columnas y genera un registro vacío representado 
    como un diccionario. Inicializa todos los valores con una cadena vacía.
    Se excluye la columna correspondiente al ID.
    """
    empty_record = {col: '' for col in columns if col != id_column}
    
    return empty_record

def validate_record(record, dataset_name):
    """
    Valida un registro antes de insertarlo.
    Reutiliza funciones y constantes de validaciones.py.
    No considera la validación del ID.
    Retorna True si el registro es válido, False en caso contrario.
    """
    if dataset_name not in TRADUCTOR_DATASETS:
        print(f"Dataset '{dataset_name}' no reconocido.")
        return False
        
    cols = TRADUCTOR_DATASETS[dataset_name]
    
    # 1. Validar coordenadas
    lat = record.get(cols['latitud'], '')
    lon = record.get(cols['longitud'], '')
    
    if evaluar_error(lat, -90, 90) or evaluar_error(lon, -180, 180):
        print("Error: Coordenadas geográficas inválidas.")
        return False
        
    # 2. Inconsistencia de coordenadas
    if (lat == '') != (lon == ''):
        print("Error: Inconsistencia en coordenadas (falta latitud o longitud).")
        return False

    # 3. Está dentro de América del Sur?
    if evaluar_error(lat, LATITUD_SUR, LATITUD_NORTE) or evaluar_error(lon, LONGITUD_OESTE, LONGITUD_ESTE):
        print("Error: Coordenadas fuera de los límites de América del Sur.")
        return False

    # 4. Validar fechas
    fecha_str = record.get(cols['fecha'], '')
    if fecha_str != '':
        try:
            fecha = datetime.fromisoformat(fecha_str)
            if fecha.year > 2026:
                print("Error: La fecha es posterior a 2026.")
                return False
        except (ValueError, TypeError):
            print("Error: La fecha no tiene un formato ISO válido.")
            return False

    # 5. Validar countryCode
    pais_str = record.get(cols['pais'], '')
    if pais_str != '':
        pais = pycountry.countries.get(alpha_2=pais_str)
        if pais is None:
            print(f"Error: El código de país '{pais_str}' no es válido.")
            return False

    # 6. Validar incertidumbre (si el dataset la usa)
    col_rango = cols.get('coordenada_rango')
    if col_rango and col_rango in record:
        rango_str = record[col_rango]
        if rango_str != '':
            try:
                rango = float(rango_str)
                if rango < 0 or rango > 100:
                    print("Error: Incertidumbre fuera de rango (0-100).")
                    return False
            except ValueError:
                print("Error: Incertidumbre no es un valor numérico.")
                return False

    # 7. Validar datos taxonómicos
    for col_tax in cols.get('taxonomica', []):
        if record.get(col_tax, '') == '':
            print(f"Error: Campo taxonómico '{col_tax}' está vacío.")
            return False

    return True
