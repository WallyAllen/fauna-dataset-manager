import csv

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
