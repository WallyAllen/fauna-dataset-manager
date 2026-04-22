import csv

def buscar_registros(ruta_archivo, filtros):
    """
    Esta funcion busca registros en un archivo iterando con csv.dictreader y
    retorna una lista de diccionarios con las filas que cumplen los filtros
    """
    resultados = [] #inicializo la lista
     
try: #Considero que el try-except se acoplan mejor a la logica de verificar la existencia del archivo
        # con with open puedo abrir el archivo y saber que post uso va a estar cerrado. (evito usar .close() y etc etc)
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            # DictReader asume la primera fila como claves del diccionario 
            lector = csv.DictReader(archivo, delimiter='\t')
            for fila in lector:
                coincidencia = True
                # Itero sobre los diccionarios 
                for columna, valor_buscado in filtros.items():
                    # Valido que la columna exista y su valor sea igual al buscado
                    # Convierto valor_buscado a string para facilitar la comparacion
                    if fila.get(columna) != str(valor_buscado):
                        coincidencia = False
                        break # Rompe el bucle interno si una condición ya no se cumple
                if coincidencia:
                    resultados.append(fila)
                    
