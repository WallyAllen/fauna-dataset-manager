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
    """Retorna la lista de columnas del dataset."""
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return reader.fieldnames
    
def get_column_indices(filepath, encoding='utf-8', delimiter='\t'):
    """Retorna un diccionario {nombre_columna: índice} de cada columna."""
    with open(filepath, encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return {nombre: indice for indice, nombre in enumerate(reader.fieldnames)}    
    
    