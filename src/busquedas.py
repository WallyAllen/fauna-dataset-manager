import csv

def buscar_registros(ruta_archivo, filtros, delimitador = ',' ):
    """
    Esta funcion busca registros en un archivo iterando con csv.dictreader y
    retorna una lista de diccionarios con las filas que cumplen los filtros
    """
    resultados = [] #inicializo la lista
     
    try: #Considero que el try-except se acoplan mejor a la logica de verificar la existencia del archivo
            # con with open puedo abrir el archivo y saber que post uso va a estar cerrado. (evito usar .close() y etc etc)
        with open(ruta_archivo, mode= 'r', encoding= 'utf-8') as archivo:
            # DictReader asume la primera fila como claves del diccionario 
            lector = csv.DictReader(archivo, delimiter = delimitador)
            resultados = list(filter( #filter me sirve para filtar los elementos que cumplan la condicion y #list me devuelve una lista
                lambda fila: all(fila.get(col) == str(val) for col, val in filtros.items()), lector #utilizo lambda para 
            #no hacer una funcion entera. simplifique la logica de for e if con el metodo all() que verifica que los elementos de la lista 
            #sean == true en relacion a los parametros dados
                ))
    except FileNotFoundError: #como dice, en caso de no estar/encontrar el archivo
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'.")
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error que 
        print(f"Se produjo un error al procesar el archivo: {e}")
        raise
            
    return resultados 

def actualizar_registros(ruta_archivo, ruta_salida, identificador, columnaID, valores_nuevos, delimitador = ','):
    """
    Esta funcion busca el archivo que busca el nombre de la columna en el registro dicho y setea el nuevo valor  
    """
    try:
        with open(ruta_archivo, mode= 'r', encoding= 'utf-8') as archivo_lectura, open(ruta_salida, mode='w') as archivo_escritura:
            #abro tanto el archivo que estoy leyendo como el nuevo que voy a modificar (ya que no podemos modificar los raw)
            lector= csv.DictReader(archivo_lectura, delimiter = delimitador)
            nombres_columnas = lector.fieldnames 
            escritor = csv.DictWriter(archivo_escritura, fieldnames = nombres_columnas, delimiter = delimitador)
            #obtengo los nombres de las filas            
            #creo el encabezado
            escritor.writeheader()
            #itero hasta encontrar lo que quiero modificar
            for fila in lector:
                #me fijo si es la fila correcto
                if fila.get(columnaID) == str(identificador):
                    #actualizo el valor
                    fila.update(valores_nuevos) #al ser un diccionario, update va a modificar aquellas variables cuya clave sea la misma
                escritor.writerow(fila)    
    except FileNotFoundError: #como dice, en caso de no estar/encontrar el archivo
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'.")
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error que 
        print(f"Se produjo un error al procesar el archivo: {e}")
        raise                                  
                       
