import csv
import os
def eliminar_por_identificador(ruta_entrada, ruta_salida, columnaID, identificador, delimiter = ','):
    """
    Esta funcion elimina un registro del processed_dataset a partir del identificador recibido.
    """
    ruta_temporal = ruta_salida + '.temp'
    encontre= False
    try: 
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open(ruta_temporal, mode = 'w', encoding='utf-8') as archivo_escritura:
            lector=csv.DictReader(archivo_lectura, delimiter=delimiter)
            nombres_columnas= lector.fieldnames
            escritor=csv.DictWritter(archivo_escritura, nombres_columnas, delimiter=delimiter)
            escritor.writeheader()
            for fila in lector:
                if fila(columnaID) == str(identificador):
                    print("Archivo encontrado correctamente.")
                    encontre= True
                else:
                    
                    escritor.writerow(fila)
            if not encontre:
                print("Archivo no encontrado.")
            os.replace(ruta_temporal, ruta_salida)
    except FileNotFoundError:
        print()
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise   