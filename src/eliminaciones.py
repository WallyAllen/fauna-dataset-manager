import csv
import os
import validaciones
from src.log_operaciones import log

def _obtener_config_dataset(dataset):
    if dataset not in validaciones.TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. Opciones válidas: {list(validaciones.TRADUCTOR_DATASETS.keys())}"
        )
    return validaciones.TRADUCTOR_DATASETS[dataset]

def eliminar_por_identificador(dataset, ruta_entrada, ruta_salida, columnaID, identificador, delimiter = ','):
    """
    Esta función elimina un registro del dataset a partir del identificador recibido.
    """
    ruta_temporal = ruta_salida + '.temp'
    eliminados = 0
    try: 
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open(ruta_temporal, mode = 'w', newline='', encoding='utf-8') as archivo_escritura:
            lector = csv.DictReader(archivo_lectura, delimiter=delimiter)
            nombres_columnas = lector.fieldnames
            escritor = csv.DictWriter(archivo_escritura, fieldnames=nombres_columnas, delimiter=delimiter)
            escritor.writeheader()
            for fila in lector:
                if fila.get(columnaID) == str(identificador):
                    print("Registro encontrado correctamente.")
                    eliminados += 1
                else:
                    escritor.writerow(fila)
        if eliminados == 0:
            print("Registro no encontrado.")
            log(dataset, "DELETE", 0, status="ERROR")
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
        else:
            os.replace(ruta_temporal, ruta_salida)
            log(dataset, "DELETE", eliminados)
    except FileNotFoundError:
        print("FileNotFoundError")
        log(dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        log(dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise   
    
def eliminar_por_lista(dataset, ruta_entrada, ruta_salida, columnaID, identificador, delimiter = ','): # identificador en este caso es una lista
    """
    Esta funcion elimina registros del data_set a partir de la lista recibida.
    """
    ruta_temporal= ruta_salida + '.temp'
    eliminados = 0
    try:
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open (ruta_temporal, mode= 'w', newline='', encoding= 'utf-8') as archivo_escritura:
            lector = csv.DictReader(archivo_lectura, delimiter = delimiter)
            nombres_columnas = lector.fieldnames
            escritor = csv.DictWriter(archivo_escritura, fieldnames=nombres_columnas, delimiter = delimiter)
            escritor.writeheader()
            for fila in lector:
                if fila.get(columnaID) in identificador:
                    print("Valor encontrado dentro del registro")
                    eliminados += 1
                else:
                    escritor.writerow(fila)
        if eliminados == 0:
            print("Ninguno de los valores fue encontrado")
            log(dataset, "DELETE", 0, status="ERROR")
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
        else:
            os.replace(ruta_temporal, ruta_salida)
            log(dataset, "DELETE", eliminados)
    except FileNotFoundError:
        print("FileNotFoundError")
        log(dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        log(dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise   
    
def cumple_condicion(valor_fila, condicion, valor_buscado):
    """
    Evalua la condicion matematica entre el valor de la fila y el buscado
    """
    # intento convertir ambos a numeros para compararlos matematicamente
    try:
        val_f = float(valor_fila)
        val_b = float(valor_buscado)
    except ValueError:
        # si da error los dejo como string
        val_f = str(valor_fila)
        val_b = str(valor_buscado)
        
    # evaluo que simbolo pasaron y retorno true o false
    if condicion == '==': return val_f == val_b
    elif condicion == '!=': return val_f != val_b
    elif condicion == '>': return val_f > val_b
    elif condicion == '<': return val_f < val_b
    elif condicion == '>=': return val_f >= val_b
    elif condicion == '<=': return val_f <= val_b
    else: return False
    
def eliminar_por_condicion(dataset, ruta_entrada, ruta_salida, columnaID, condicion, valor, delimiter=','):
    """
        Esta funcion elimina un registro si cumple la condición.
    """
    ruta_temporal = ruta_salida + '.temp'
    eliminados = 0
    try:
        with open(ruta_entrada, mode= 'r', encoding= 'utf-8') as archivo_lectura, open (ruta_temporal, mode= 'w', newline='', encoding= 'utf-8') as archivo_escritura:
                lector= csv.DictReader(archivo_lectura, delimiter = delimiter)
                escritor= csv.DictWriter(archivo_escritura, fieldnames= lector.fieldnames , delimiter = delimiter)
                escritor.writeheader()
                for fila in lector:
                    # llamo a la funcion anterior
                    if cumple_condicion(fila.get(columnaID), condicion, valor):
                        print(f"Registro eliminado por cumplir: {columnaID} {condicion} {valor}")
                        eliminados += 1
                    else:
                        escritor.writerow(fila)
        if eliminados == 0:
            print(f"Ningun registro cumplio la condicion '{condicion} {valor}'.")
            log(dataset, "DELETE", 0, status="ERROR")
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
        else:
            os.replace(ruta_temporal, ruta_salida)
            log(dataset, "DELETE", eliminados)
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo de origen '{ruta_entrada}'")
        log(dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)        
    except Exception as e: 
        print(f"Se produjo un error al procesar el archivo: {e}")
        log(dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise    

def sanitizar_dataset(nombre_dataset, ruta_entrada, ruta_salida, delimitador='\t'):
    """
    Sanitiza un dataset completo evaluando cada registro con las funciones de validacion
    Los registros con errores son omitidos en el nuevo archivo limpio.
    """
    config = _obtener_config_dataset(nombre_dataset)
    
    # inicializo contadores
    registros_leidos = 0
    registros_eliminados = 0
    # diccionario para agrupar motivos 
    motivos_eliminacion = {}

    ids_a_eliminar = {} # {id: motivo}
    
    def registrar_errores(resultado, motivo):
        if resultado and resultado.get('existe_error'):
            lista_ids = resultado.get('lista_invalidos') or resultado.get('lista_ids') or resultado.get('id_duplicados') or []
            for rid in lista_ids:
                if rid not in ids_a_eliminar:
                    ids_a_eliminar[rid] = motivo

    registrar_errores(validaciones.validar_coordenadas(nombre_dataset, ruta_entrada), "Error en Coordenadas")
    registrar_errores(validaciones.validar_fechas(nombre_dataset, ruta_entrada), "Error en Fechas")
    registrar_errores(validaciones.verificar_countryCode(nombre_dataset, ruta_entrada), "Error en Código de País")
    registrar_errores(validaciones.verificar_incertidumbre(nombre_dataset, ruta_entrada), "Error en Incertidumbre")

    ruta_temporal = ruta_salida + '.temp'
    col_id = config['id']

    try:
        # Abrimos origen y destino temporal
        with open(ruta_entrada, mode='r', encoding='utf-8') as archivo_lectura, open(ruta_temporal, mode='w', newline='', encoding='utf-8') as archivo_escritura:
            lector = csv.DictReader(archivo_lectura, delimiter=delimitador)
            nombres_columnas = lector.fieldnames        
            escritor = csv.DictWriter(archivo_escritura, fieldnames=nombres_columnas, delimiter=delimitador)
            escritor.writeheader()
            for fila in lector:
                registros_leidos += 1
                rid = fila.get(col_id)
                # aplico validaciones y agrego and para reducir procesamiento
                if rid in ids_a_eliminar:
                    # si contiene errores lo omito y aumento registros_eliminados
                    registros_eliminados += 1
                    motivo_falla = ids_a_eliminar[rid]
                    if motivo_falla in motivos_eliminacion:
                        motivos_eliminacion[motivo_falla] += 1
                    else:
                        motivos_eliminacion[motivo_falla] = 1
                else:
                    # si el registro esta ok, lo escribo en el .temp
                    escritor.writerow(fila)
                    
        #post sanitizar, reemplazo la ruta de salida por el .temp
        os.replace(ruta_temporal, ruta_salida)
        if registros_leidos > 0:
            porcentaje = (registros_eliminados / registros_leidos) * 100
        else:
            porcentaje = 0.0
        #un poquito de magia estetica para la consola
        print("====================================================")
        print(f"Sanitización de '{nombre_dataset}' finalizada")
        print(f"Registros analizados: {registros_leidos}")
        print(f"Registros eliminados (con errores): {registros_eliminados}")
        print(f"Registros limpios guardados: {registros_leidos - registros_eliminados}")
        print(f"Registros eliminados: {registros_eliminados} ({porcentaje:.2f}% del total)")
        if registros_eliminados > 0:
            log(nombre_dataset, "DELETE", registros_eliminados)
            print("\nMotivos de eliminación detallados:")
            for motivo, cantidad in motivos_eliminacion.items():
                porcentaje_motivo = (cantidad / registros_eliminados) * 100
                print(f" - {motivo}: {cantidad} registros ({porcentaje_motivo:.1f}%)")
        print("====================================================")
    except FileNotFoundError:
        print(f"Error: No se encontro el dataset original en '{ruta_entrada}'")
        log(nombre_dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
            
    except Exception as e: 
        print(f"Se produjo un error al sanitizar: {e}")
        log(nombre_dataset, "DELETE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise
