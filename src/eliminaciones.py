import csv
import os

def eliminar_por_identificador(ruta_entrada, ruta_salida, columnaID, identificador, delimiter = ','):
    """
    Esta funcion elimina un registro del dataset a partir del identificador recibido.
    """
    ruta_temporal = ruta_salida + '.temp'
    encontre= False
    try: 
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open(ruta_temporal, mode = 'w', encoding='utf-8') as archivo_escritura:
            lector=csv.DictReader(archivo_lectura, delimiter=delimiter)
            nombres_columnas= lector.fieldnames
            escritor=csv.DictWriter(archivo_escritura, nombres_columnas, delimiter=delimiter)
            escritor.writeheader()
            for fila in lector:
                if fila.get(columnaID) == str(identificador):
                    print("Registro encontrado correctamente.")
                    encontre= True
                else:
                    escritor.writerow(fila)
        if not encontre:
            print("Registro no encontrado.")
        os.replace(ruta_temporal, ruta_salida)
    except FileNotFoundError:
        print("FileNotFoundError")
        os.remove(ruta_temporal)
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise   
    
def eliminar_por_lista(ruta_entrada, ruta_salida, columnaID, identificador, delimiter = ','): #identificador en este caso es una lista
    """
    Esta funcion elimina registros del data_set a partir de la lista recibida.
    """
    ruta_temporal= ruta_salida + '.temp'
    encontre= False
    try:
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open (ruta_temporal, mode= 'w', encoding= 'utf-8') as archivo_escritura:
            lector= csv.DictReader(archivo_lectura, delimiter = delimiter)
            nombres_columnas= lector.fieldnames
            escritor= csv.DictWriter(archivo_escritura, nombres_columnas, delimiter = delimiter)
            for fila in lector:
                if fila.get(columnaID) in identificador:
                    print("Valor encontrado dentro del registro")
                    encontre= True
                else:
                    escritor.writerow(fila)
        if not encontre:
            print("Ninguno de los valores fue encontrado")
        os.replace(ruta_temporal, ruta_salida)
    except FileNotFoundError:
        print("FileNotFoundError")
        os.remove(ruta_temporal)
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise   
    
def cumple_condicion(valor_fila, condicion, valor_buscado):
    """
    Evalua la condicion matematica entre el valor de la fila y el buscado
    """
    #intento convertir ambos a numeros para compararlos matematicamente
    try:
        val_f = float(valor_fila)
        val_b = float(valor_buscado)
    except ValueError:
        #si da error los dejo como string
        val_f = str(valor_fila)
        val_b = str(valor_buscado)
        
    #evaluo que simbolo pasaron y retorno yrue o false
    if condicion == '==': return val_f == val_b
    elif condicion == '!=': return val_f != val_b
    elif condicion == '>': return val_f > val_b
    elif condicion == '<': return val_f < val_b
    elif condicion == '>=': return val_f >= val_b
    elif condicion == '<=': return val_f <= val_b
    else: return False
    
def eliminar_por_condicion(ruta_entrada, ruta_salida, columnaID, condicion, valor, delimiter=','):
    """
        esta funcion elimina un registro si cumple la condicion
    """
    ruta_temporal= ruta_salida + '.temp'
    encontre= False
    try:
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open (ruta_temporal, mode= 'w', encoding= 'utf-8') as archivo_escritura:
                lector= csv.DictReader(archivo_lectura, delimiter = delimiter)
                escritor= csv.DictWriter(archivo_escritura, nombres_columnas= lector.fieldnames , delimiter = delimiter)
                escritor.writeheader()
        for fila in lector:
                    # llamo a la funcion anterior
                    if cumple_condicion(fila.get(columnaID), condicion, valor):
                        print(f"Registro eliminado por cumplir: {columnaID} {condicion} {valor}")
                        encontre = True
                    else:
                        escritor.writerow(fila)
        if not encontre:
                print(f"Ningun registro cumplio la condicion '{condicion} {valor}'.")
        os.replace(ruta_temporal, ruta_salida)
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo de origen '{ruta_entrada}'")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)        
    except Exception as e: 
        print(f"Se produjo un error al procesar el archivo: {e}")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise    

import csv
import os
import validaciones # Asumiendo que así se llama el archivo de tu compañero B

def sanitizar_dataset(nombre_dataset, ruta_entrada, ruta_salida, delimitador='\t'):
    """
    Sanitiza un dataset completo evaluando cada registro con las reglas de validación.
    Los registros con errores son omitidos (eliminados) en el nuevo archivo limpio.
    """
    ruta_temporal = ruta_salida + '.temp'
    
    # Contadores para saber qué pasó (ideal para el ejercicio 6.F)
    registros_leidos = 0
    registros_eliminados = 0