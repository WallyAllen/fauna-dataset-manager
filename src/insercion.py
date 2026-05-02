import csv
import random
import os
from src.validaciones import (
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
        res_coord = validar_coordenadas(dataset_name, temp_file)
        if res_coord.get('existe_error', False):
            return False
            
        # 2. Inconsistencia de coordenadas
        res_inc = constatar_coordenadas(dataset_name, temp_file)
        if res_inc.get('existe_error', False):
            return False

        # 3. Está dentro de América del Sur?
        res_cotas = evaluar_cotas_america(dataset_name, temp_file)
        if res_cotas.get('existe_error', False):
            return False

        # 4. Validar fechas
        res_fechas = validar_fechas(dataset_name, temp_file)
        if res_fechas.get('existe_error', False):
            return False

        # 5. Validar countryCode
        res_cc = verificar_countryCode(dataset_name, temp_file)
        if res_cc.get('existe_error', False):
            return False

        # 6. Validar incertidumbre
        if TRADUCTOR_DATASETS[dataset_name]['coordenada_rango'] != '':
            res_incert = verificar_incertidumbre(dataset_name, temp_file)
            if res_incert.get('existe_error', False):
                return False

        # 7. Validar datos taxonómicos
        cant_errores = errores_taxonomicos(dataset_name, temp_file)
        if isinstance(cant_errores, dict) and cant_errores.get('existe_error', False):
            return False
        elif isinstance(cant_errores, int) and cant_errores > 0:
            return False

    finally:
        # Eliminamos el archivo temporal
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return True

def get_next_base_id(dataset_name, filepath):
    """
    Lee el archivo del dataset para encontrar el ID máximo actual y retorna el siguiente
    número autoincremental.
    """
    id_col = TRADUCTOR_DATASETS[dataset_name]['id']
    delim = TRADUCTOR_DATASETS[dataset_name]['delimitador']
    max_id = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delim)
        for row in reader:
            val = row.get(id_col, '')
            if not val:
                continue
                
            # Extraer solo el número de ID
            if dataset_name == 'xenocanto':
                val = val.replace('@XC', '')
                
            try:
                num = int(val)
                if num > max_id:
                    max_id = num
            except ValueError:
                pass
                
    # Si el archivo estuviese vacío, asignamos un número base inicial
    if max_id == 0:
        return 1000000
        
    return max_id + 1

def format_record_for_insertion(record, dataset_name, filepath):
    """
    Recibe un registro validado y le añade los IDs (autoincremental) según el dataset correspondiente.
    Retorna el diccionario listo para ser añadido al CSV.
    """
    if dataset_name not in TRADUCTOR_DATASETS:
        return record
        
    # Obtenemos el ID siguiente de forma autoincremental leyendo el archivo
    base_id = get_next_base_id(dataset_name, filepath)
    
    if dataset_name == 'inaturalist':
        record['id'] = str(base_id)
        if 'occurrenceID' in record:
            record['occurrenceID'] = f"https://www.inaturalist.org/observations/{base_id}"
        if 'catalogNumber' in record:
            record['catalogNumber'] = str(base_id)
            
    elif dataset_name == 'xenocanto':
        num_str = str(base_id)
        record['id'] = f"{num_str}@XC"
        if 'occurrenceID' in record:
            record['occurrenceID'] = f"https://data.biodiversitydata.nl/xeno-canto/observation/XC{num_str}"
        if 'catalogNumber' in record:
            record['catalogNumber'] = f"XC{num_str}"
            
    elif dataset_name == 'iadiza':
        catalog_num = str(base_id)[-6:].zfill(6)
        record['gbifID'] = str(base_id)
        if 'occurrenceID' in record:
            record['occurrenceID'] = f"IADIZA:COI:{catalog_num}"
        if 'catalogNumber' in record:
            record['catalogNumber'] = catalog_num
    return record

def insert_record(dataset_name, in_filepath, out_filepath):
    """
    Lee el dataset original para obtener su estructura.
    Agrega un nuevo registro solicitando por teclado los datos esenciales.
    Valida y formatea el registro.
    Escribe un nuevo archivo conservando la estructura e incluyendo el nuevo registro.
    """
    if dataset_name not in TRADUCTOR_DATASETS:
        print(f"Dataset '{dataset_name}' no reconocido.")
        return False
        
    id_col = TRADUCTOR_DATASETS[dataset_name]['id']
    delim = TRADUCTOR_DATASETS[dataset_name]['delimitador']
    
    # 1. Crear estructura vacía basada en el dataset original
    record = create_record_structure(in_filepath, id_column=id_col, delimiter=delim)
    
    # 2. Pedir datos por teclado
    print("--- Ingrese los datos del nuevo registro ---")
    traductor = TRADUCTOR_DATASETS[dataset_name]
    columnas_esenciales = []
    
    for key, value in traductor.items():
        if key in ['delimitador', 'id']:
            continue
        if isinstance(value, list):
            columnas_esenciales.extend(value)
        elif value != '':
            columnas_esenciales.append(value)
            
    for col in columnas_esenciales:
        if col in record:
            record[col] = input(f"Ingrese valor para {col}: ")
            
    # Validar el registro ingresado
    print("Validando registro")
    if not validate_record(record, dataset_name):
        print("El registro ingresado no cumple con las validaciones.")
        return False
        
    # Añadir los IDs correspondientes
    record = format_record_for_insertion(record, dataset_name, in_filepath)
    
    # Lectura del original y escritura del nuevo archivo
    os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
    
    # Obtiene las columnas originales para el DictWriter
    with open(in_filepath, 'r', encoding='utf-8') as fin:
        reader = csv.DictReader(fin, delimiter=delim)
        fieldnames = reader.fieldnames
        
    print("Creando nuevo archivo")
    with open(in_filepath, 'r', encoding='utf-8') as fin, open(out_filepath, 'w', encoding='utf-8') as fout:
        for line in fin:
            fout.write(line)
            
    print("Anexando el nuevo registro al final")
    with open(out_filepath, 'a', encoding='utf-8', newline='') as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter=delim)
        writer.writerow(record)
        
    print(f"Archivo generado en: {out_filepath}")
    return True
