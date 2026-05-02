import csv
import random
import os
import contextlib
from validaciones import (
    TRADUCTOR_DATASETS,
    validar_coordenadas,
    constatar_coordenadas,
    validar_fechas,
    verificar_countryCode,
    verificar_incertidumbre,
    errores_taxonomicos,
    evaluar_cotas_america
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
    Se utiliza el código de validaciones.py, debido a que lee archivos enteros, creamos un archivo temporal,
    luego escribimos el registro el archivo temporal y se lo pasamos a las funciones originales.
    Retorna True si el registro es válido, False en caso contrario.
    """
    if dataset_name not in TRADUCTOR_DATASETS:
        print(f"Dataset '{dataset_name}' no reconocido.")
        return False
        
    temp_file = f"temp_validation_{random.randint(1000, 9999)}.csv"
    delim = TRADUCTOR_DATASETS[dataset_name]['delimitador']
    
    try:
        # Escribimos el registro como un CSV de una fila
        with open(temp_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=record.keys(), delimiter=delim)
            writer.writeheader()
            writer.writerow(record)
            
        # 1. Validar coordenadas
        exist_error, _, _ = validar_coordenadas(dataset_name, temp_file)
        if exist_error:
            return False
            
        # 2. Inconsistencia de coordenadas
        exist_error, _, _ = constatar_coordenadas(dataset_name, temp_file)
        if exist_error:
            return False

        # 3. Está dentro de América del Sur?
        exist_error, _, _ = evaluar_cotas_america(dataset_name, temp_file)
        if exist_error:
            return False

        # 4. Validar fechas
        _, _, exist_error = validar_fechas(dataset_name, temp_file)
        if exist_error:
            return False

        # 5. Validar countryCode
        exist_error = verificar_countryCode(dataset_name, temp_file)
        if exist_error:
            return False

        # 6. Validar incertidumbre
        if TRADUCTOR_DATASETS[dataset_name]['coordenada_rango'] != '':
            exist_error = verificar_incertidumbre(dataset_name, temp_file)
            if exist_error:
                return False

        # 7. Validar datos taxonómicos
        cant_errores = errores_taxonomicos(dataset_name, temp_file)
        if cant_errores > 0:
            return False

    finally:
        # Eliminamos el archivo temporal
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return True


