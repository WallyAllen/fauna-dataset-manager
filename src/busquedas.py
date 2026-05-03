import csv
import os
from log_operaciones import log
from src import validaciones
from src.log_operaciones import log

TRADUCTOR_DATASETS = validaciones.TRADUCTOR_DATASETS

def _obtener_config_dataset(dataset):
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    return TRADUCTOR_DATASETS[dataset]

def buscar_registros(ruta_archivo, filtros, delimitador = ',', dataset=None):
    """
    Esta funcion busca registros en un archivo iterando con csv.dictreader y
    retorna una lista de diccionarios con las filas que cumplen los filtros
    """
    if dataset is not None:
        config = _obtener_config_dataset(dataset)
        if delimitador == ',':
            delimitador = config['delimitador']
        filtros = {config.get(col, col): str(val) for col, val in filtros.items()}

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

def actualizar_registros(ruta_archivo, ruta_salida, identificador, columnaID, valores_nuevos, delimitador = ',', dataset=None):
    """
    Esta funcion busca el archivo que busca el nombre de la columna en el registro dicho y setea el nuevo valor  
    """

    if dataset is not None:
        config = _obtener_config_dataset(dataset)
        if delimitador == ',':
            delimitador = config['delimitador']
        columnaID = config.get(columnaID, columnaID)
        valores_nuevos_traducidos = {config.get(col, col): val for col, val in valores_nuevos.items()}
    else:
        valores_nuevos_traducidos = valores_nuevos

    ruta_temporal = ruta_salida + ".temp" # creo una ruta temporal para poder operar       
            
    afectados = 0
    try:
        with open(ruta_archivo, mode= 'r', encoding= 'utf-8') as archivo_lectura, open(ruta_temporal, mode='w', newline='', encoding='utf-8') as archivo_escritura:
            # abro tanto el archivo que estoy leyendo como el nuevo que voy a modificar (ya que no podemos modificar los raw)
            lector = csv.DictReader(archivo_lectura, delimiter = delimitador)
            nombres_columnas = lector.fieldnames 
            escritor = csv.DictWriter(archivo_escritura, fieldnames = nombres_columnas, delimiter = delimitador)
            # creo el encabezado
            escritor.writeheader()
            # itero hasta encontrar lo que quiero modificar
            for fila in lector:
                # me fijo si es la fila correcto
                if fila.get(columnaID) == str(identificador):
                    # actualizo el valor
                    fila.update(valores_nuevos_traducidos) # al ser un diccionario, update va a modificar aquellas variables cuya clave sea la misma
                    print(f"Registro '{identificador}' actualizado con exito.")
                    afectados += 1
                # guardo la fila se haya modificado o no
                escritor.writerow(fila)

        if afectados == 0:
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
            if dataset is not None:
                log(dataset, "UPDATE", 0, status="ERROR")
        else:
            # validaciones sobre el archivo temporal (solo si hubo filas modificadas)
            no_valido = False
            if dataset is not None:
                config = _obtener_config_dataset(dataset)
                if config['latitud'] in valores_nuevos_traducidos or config['longitud'] in valores_nuevos_traducidos:
                    res = validaciones.validar_coordenadas(dataset, ruta_temporal)
                    if res.get('existe_error'):
                        no_valido = True
                if config['fecha'] in valores_nuevos_traducidos:
                    res = validaciones.validar_fechas(dataset, ruta_temporal)
                    if res.get('existe_error'):
                        no_valido = True
                if config['pais'] in valores_nuevos_traducidos:
                    res = validaciones.verificar_countryCode(dataset, ruta_temporal)
                    if res and res.get('existe_error'):
                        no_valido = True
                if config['coordenada_rango'] and config['coordenada_rango'] in valores_nuevos_traducidos:
                    res = validaciones.verificar_incertidumbre(dataset, ruta_temporal)
                    if res.get('existe_error'):
                        no_valido = True

            if not no_valido:
                os.replace(ruta_temporal, ruta_salida)
                if dataset is not None:
                    log(dataset, "UPDATE", afectados)
            else:
                print(f"Error al actualizar el registro '{identificador}'")
                if dataset is not None:
                    log(dataset, "UPDATE", 0, status="ERROR")
                if os.path.exists(ruta_temporal):
                    os.remove(ruta_temporal)

    except FileNotFoundError: # como dice, en caso de no estar/encontrar el archivo
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'.")
        if dataset is not None:
            log(dataset, "UPDATE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        if dataset is not None:
            log(dataset, "UPDATE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise
