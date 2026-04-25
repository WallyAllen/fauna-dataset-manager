import csv
import os
def eliminar_por_identificador(ruta_entrada, ruta_salida, identificador, delimiter = ','):
    """
    Esta funcion elimina un registro del processed_dataset a partir del identificador recibido.
    """
    try: 
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open(ruta_salida, mode = 'r', encoding='utf-8') as archivo_escritura:
            lector=csv.DictReader(archivo_lectura, delimiter=delimiter)
            escritor=csv.DictWritter(archivo_escritura, delimiter=delimiter)
    
    except FileNotFoundError:
        print()