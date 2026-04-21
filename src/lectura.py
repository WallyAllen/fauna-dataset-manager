import csv
from pathlib import Path


def print_first_rows(filepath, n=10, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.A
    Imprime las primeras n filas del dataset.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if i >= n:
                break
            print(f"--- Registro {i + 1} ---")
            for clave, valor in row.items():
                print(f"  {clave}: {valor}")

def get_columns(filepath, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.B
    Retorna la lista de columnas del dataset.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return reader.fieldnames
    
def get_column_indices(filepath, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.C
    Retorna un diccionario {nombre_columna: índice} de cada columna.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return {nombre: indice for indice, nombre in enumerate(reader.fieldnames)}    
    
def count_records(filepath, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.D
    Retorna la cantidad total de registros del dataset.
    """
    count = 0
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            count += 1
    return count    

def get_columns_with_nulls(filepath, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.E
    Retorna una lista con las columnas que tienen al menos un valor vacío.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        tiene_nulo = {col: False for col in reader.fieldnames}
        for row in reader:
            for col in reader.fieldnames:
                if row[col] == '':
                    tiene_nulo[col] = True
    return [col for col, tiene in tiene_nulo.items() if tiene]


def get_null_percentage(filepath, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.F
    Retorna un diccionario {columna: porcentaje_de_nulos} para cada columna.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        nulos = {col: 0 for col in reader.fieldnames}
        total = 0
        for row in reader:
            total += 1
            for col in reader.fieldnames:
                if row[col] == '':
                    nulos[col] += 1
    return {col: round((nulos[col] / total) * 100, 2) for col in nulos}

def get_distinct_count(filepath, column, encoding='utf-8', delimiter='\t'):
    """
    Ejercicio 2.G
    Retorna la cantidad de valores distintos en una columna.
    Si la columna no existe informa el error.
    """
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        if column not in reader.fieldnames:
            print(f"La columna '{column}' no existe en el dataset.")
            return None
        valores = set()
        for row in reader:
            if row[column] != '':
                valores.add(row[column])
    return len(valores)