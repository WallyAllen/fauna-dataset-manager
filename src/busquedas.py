import csv
import os
from datetime import datetime
import pycountry
from src import validaciones
from src.log_operaciones import log

TRADUCTOR_DATASETS = validaciones.TRADUCTOR_DATASETS


def _obtener_config_dataset(dataset):
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    return TRADUCTOR_DATASETS[dataset]


def _traducir_clave_unica(clave, config):
    """
    Traduce una clave semántica a un único nombre de columna real.
    Si la clave semántica apunta a varias columnas (ej. 'fecha' -> ['eventDate', ...]),
    devuelve la primera (canónica). Si la clave no es semántica, se asume que ya es
    el nombre real de una columna y se devuelve tal cual.
    """
    target = config.get(clave, clave)
    if isinstance(target, list):
        return target[0] if target else clave
    return target


def _expandir_clave(clave, config):
    """
    Devuelve la lista de columnas reales asociadas a una clave semántica.
    Para claves multi-columna (ej. 'fecha') devuelve todas las opciones.
    Para claves simples devuelve una lista con una sola entrada.
    """
    target = config.get(clave, clave)
    if isinstance(target, list):
        return list(target)
    return [target]


def _valor_coincide(valor_fila, valor_buscado):
    # si la fila no tiene la columna, get devuelve None
    if valor_fila is None:
        return valor_buscado is None or valor_buscado == ""
    # si el filtro pide None, admitimos celda vacía
    if valor_buscado is None:
        return valor_fila == ""
    return str(valor_fila) == str(valor_buscado)


def _fila_pasa_filtros(fila, filtros_expandidos):
    """
    `filtros_expandidos` es una lista de tuplas (lista_columnas, valor).
    Una fila pasa si para cada filtro al menos una de las columnas de su lista
    coincide con el valor buscado.
    """
    return all(
        any(_valor_coincide(fila.get(col), val) for col in cols)
        for cols, val in filtros_expandidos
    )


def buscar_registros(ruta_archivo, filtros, delimitador=None, dataset=None):
    """
    Esta funcion busca registros en un archivo iterando con csv.dictreader y
    retorna una lista de diccionarios con las filas que cumplen los filtros.

    Las claves de `filtros` pueden ser semánticas (definidas en TRADUCTOR_DATASETS:
    'latitud', 'longitud', 'fecha', 'pais', 'id', 'coordenada_rango') o nombres
    de columna reales. Para 'fecha' (que mapea a varias columnas) la fila pasa
    si CUALQUIERA de esas columnas coincide con el valor buscado.
    """
    if dataset is not None:
        config = _obtener_config_dataset(dataset)
        if delimitador is None:
            delimitador = config['delimitador']
        # cada filtro queda como (lista_de_columnas_reales, valor_buscado)
        filtros_expandidos = [
            (_expandir_clave(col, config), val) for col, val in filtros.items()
        ]
    else:
        if delimitador is None:
            delimitador = ','
        filtros_expandidos = [([col], val) for col, val in filtros.items()]

    #inicializo la lista
    resultados = []
    #Considero que el try-except se acoplan mejor a la logica de verificar la existencia del archivo 
    try:
         #con with open puedo abrir el archivo y saber que post uso va a estar cerrado. (evito usar .close() y etc etc)
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            # DictReader asume la primera fila como claves del diccionario 
            lector = csv.DictReader(archivo, delimiter=delimitador)
            resultados = list(filter( #filter me sirve para filtar los elementos que cumplan la condicion y #list me devuelve una lista
                lambda fila: _fila_pasa_filtros(fila, filtros_expandidos), lector
            #_fila_pasa_filtros encapsula la doble iteracion (cada filtro contra sus posibles columnas)
                ))
    except FileNotFoundError: #como dice, en caso de no estar/encontrar el archivo
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'.")
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error que 
        print(f"Se produjo un error al procesar el archivo: {e}")
        raise

    return resultados


def _validar_valores_nuevos(valores_nuevos_traducidos, config):
    """
    Valida que los nuevos valores a insertar sean correctos según las reglas
    del dataset. Solo revisa los campos presentes en `valores_nuevos_traducidos`,
    no el resto del archivo.

    Retorna (es_valido: bool, motivo: str | None).
    """
    # Coordenadas
    if config['latitud'] in valores_nuevos_traducidos:
        valor = valores_nuevos_traducidos[config['latitud']]
        if validaciones.evaluar_error(valor, -90, 90):
            return False, f"Latitud inválida: {valor!r}"
    if config['longitud'] in valores_nuevos_traducidos:
        valor = valores_nuevos_traducidos[config['longitud']]
        if validaciones.evaluar_error(valor, -180, 180):
            return False, f"Longitud inválida: {valor!r}"

    # Fechas (config['fecha'] siempre es lista de columnas)
    columnas_fecha = config['fecha'] if isinstance(config['fecha'], list) else [config['fecha']]
    for col in columnas_fecha:
        if col in valores_nuevos_traducidos:
            valor = valores_nuevos_traducidos[col]
            if not valor:
                continue
            try:
                fecha = datetime.fromisoformat(str(valor).replace('Z', '+00:00'))
                if fecha.year > datetime.now().year:
                    return False, f"Fecha posterior al año actual en '{col}': {valor!r}"
            except (ValueError, TypeError):
                return False, f"Fecha con formato inválido en '{col}': {valor!r}"

    # País
    if config['pais'] in valores_nuevos_traducidos:
        valor = valores_nuevos_traducidos[config['pais']]
        if valor:
            if config['tipo_pais'] == 'alpha_2':
                pais = pycountry.countries.get(alpha_2=valor)
            else:
                # nombres comunes vs oficiales: probar varias estrategias
                pais = (
                    pycountry.countries.get(name=valor)
                    or pycountry.countries.get(common_name=valor)
                    or pycountry.countries.get(official_name=valor)
                )
            if pais is None:
                return False, f"País no reconocido: {valor!r}"

    # Incertidumbre de coordenada (solo si el dataset declara la columna)
    if config.get('coordenada_rango'):
        col = config['coordenada_rango']
        if col in valores_nuevos_traducidos:
            valor = valores_nuevos_traducidos[col]
            if valor:
                try:
                    rango = float(valor)
                    if rango < 0 or rango > 100:
                        return False, f"coordinateUncertaintyInMeters fuera del rango 0-100: {valor!r}"
                except (ValueError, TypeError):
                    return False, f"coordinateUncertaintyInMeters no es numérico: {valor!r}"

    return True, None


def actualizar_registros(ruta_archivo, ruta_salida, identificador, columnaID,
                         valores_nuevos, delimitador=None, dataset=None):
    """
    Esta funcion busca el archivo que busca el nombre de la columna en el registro dicho y setea el nuevo valor.

    Si `dataset` está dado, las claves de `valores_nuevos` y `columnaID` pueden ser
    semánticas y se traducen al nombre real de columna. Antes de escribir, los
    valores nuevos se validan según las reglas del dataset (rangos, fechas ISO,
    país, incertidumbre). Si la validación falla NO se modifica el archivo destino.

    Retorna la cantidad de filas modificadas (0 si no hubo match o la validación falló).
    """
    config = None

    if dataset is not None:
        config = _obtener_config_dataset(dataset)
        if delimitador is None:
            delimitador = config['delimitador']
        columnaID = _traducir_clave_unica(columnaID, config)
        valores_nuevos_traducidos = {
            _traducir_clave_unica(col, config): val for col, val in valores_nuevos.items()
        }
    else:
        if delimitador is None:
            delimitador = ','
        valores_nuevos_traducidos = dict(valores_nuevos)

    # Validamos ANTES de tocar archivos: no copiamos en vano si el dato es invalido
    if config is not None:
        es_valido, motivo = _validar_valores_nuevos(valores_nuevos_traducidos, config)
        if not es_valido:
            print(f"Error al actualizar el registro '{identificador}': {motivo}")
            log(dataset, "UPDATE", 0, status="ERROR")
            return 0

    ruta_temporal = str(ruta_salida) + ".temp" # creo una ruta temporal para poder operar       

    afectados = 0
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo_lectura, \
             open(ruta_temporal, mode='w', newline='', encoding='utf-8') as archivo_escritura:
            # abro tanto el archivo que estoy leyendo como el nuevo que voy a modificar (ya que no podemos modificar los raw)
            lector = csv.DictReader(archivo_lectura, delimiter=delimitador)
            nombres_columnas = lector.fieldnames
            escritor = csv.DictWriter(archivo_escritura, fieldnames=nombres_columnas, delimiter=delimitador)
            # creo el encabezado
            escritor.writeheader()
            # itero hasta encontrar lo que quiero modificar
            for fila in lector:
                # me fijo si es la fila correcta
                if fila.get(columnaID) == str(identificador):
                    # actualizo el valor (los datos ya fueron validados arriba)
                    fila.update(valores_nuevos_traducidos) # al ser un diccionario, update va a modificar aquellas variables cuya clave sea la misma
                    afectados += 1
                # guardo la fila se haya modificado o no
                escritor.writerow(fila)

        if afectados == 0:
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
            print(f"No se encontró ningún registro con {columnaID}={identificador}.")
            if dataset is not None:
                log(dataset, "UPDATE", 0, status="ERROR")
        else:
            # solo confirmamos el cambio reemplazando el archivo destino al final
            os.replace(ruta_temporal, ruta_salida)
            if afectados == 1:
                print(f"Registro '{identificador}' actualizado con exito.")
            else:
                print(f"Atención: {afectados} filas con {columnaID}={identificador} fueron actualizadas.")
            if dataset is not None:
                log(dataset, "UPDATE", afectados)

    except FileNotFoundError: # como dice, en caso de no estar/encontrar el archivo
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'.")
        if dataset is not None:
            log(dataset, "UPDATE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        afectados = 0
    except Exception as e: # "Exception as e" tiene como funcion notificar el tipo de error 
        print(f"Se produjo un error al procesar el archivo: {e}")
        if dataset is not None:
            log(dataset, "UPDATE", 0, status="ERROR")
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise

    return afectados
