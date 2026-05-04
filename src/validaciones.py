from pathlib import Path
from datetime import datetime
import csv
import pycountry
from src.lectura import count_records

TRADUCTOR_DATASETS ={
    'iadiza': {
        'delimitador' : '\t',
        'latitud' : 'decimalLatitude',
        'longitud' : 'decimalLongitude',
        'fecha' : ['eventDate', 'dateIdentified', 'modified', 'georeferencedDate'],
        'id' : 'gbifID',
        'pais' : 'countryCode',
        'tipo_pais' : 'alpha_2',
        'coordenada_rango' : '',
        'taxonomica' : ['scientificName','kingdom','phylum',
                        'class','order','family','genus',
                        'specificEpithet','taxonRank']
    },
    'inaturalist': {
        'delimitador' : ',',
        'latitud' : 'decimalLatitude',
        'longitud' : 'decimalLongitude',
        'fecha' : ['eventDate', 'dateIdentified', 'modified'],
        'id' : 'id',
        'pais' : 'countryCode',
        'tipo_pais' : 'alpha_2',
        'coordenada_rango' : 'coordinateUncertaintyInMeters',
        'taxonomica' : ['scientificName','taxonID',
                        'taxonRank','kingdom','phylum',
                        'class','order','family','genus']
    },
    'xenocanto' : {
        'delimitador' : ',',
        'latitud' : 'latitudeDecimal',
        'longitud' : 'longitudeDecimal',
        'fecha' : ['eventDate'],
        'id' : 'id',
        'pais' : 'country',
        'tipo_pais' : 'nombre',
        'coordenada_rango' : '',
        'taxonomica' : ['scientificName', 'specificEpithet', 'infraspecificEpithet',
                        'taxonRank','kingdom','phylum', 'higherClassification',
                        'class','order','family','genus','nomenclaturaCode',
                        'vernacularName','identificationRemarks']

    }

}

LATITUD_NORTE = 13
LATITUD_SUR = -56.5
LONGITUD_ESTE = -34.5
LONGITUD_OESTE = -92

# Evaluar error de medicion de coordenada 
def evaluar_error(valor, parametro_neg, parametro_pos):
    """
    Retorna True si el valor es inválido para el rango dado.
    Campos vacíos no se consideran error.
    """
    if valor == '' or valor is None:
        return False
    
    try:
        coord = float(valor)
        return coord < parametro_neg or coord > parametro_pos
    except (ValueError, TypeError):
        return True

# Evaluar errores taxonomicos
def errores_taxonomicos(dataset,path):
    cant_errores = 0
    print("Buscando errores en los datos taxonomicos...")
 
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    colum_dataset = TRADUCTOR_DATASETS[dataset]
    
    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])
        for fila in csv_reader:
            for campo in colum_dataset["taxonomica"]:
                if fila[campo] == "":
                    cant_errores += 1
                    break

    return cant_errores

# 3.A
def validar_coordenadas(dataset, path,lat = False, lon = False):
    """
    Ejercicio 3.A
    Detecta registros con coordenadas geográficas inválidas.

    Args:
        dataset (str): Nombre del dataset ('iadiza', 'inaturalist', 'xenocanto')
        path (str | Path): Ruta al archivo CSV
        delimitador (str): Separador de campos del archivo

    Returns:
        dict:
            - exist_error (bool): True si hay al menos un registro inválido
            - cant_inv (int): Cantidad de REGISTROS inválidos
            - list_inv (list[str]): IDs de los registros inválidos

    Raises:
        ValueError: Si el dataset no está en TRADUCTOR_DATASETS
        ValueError: Si el delimitador no es un string de un carácter
    """

    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )

    colum_dataset = TRADUCTOR_DATASETS[dataset]
    cant_inv = 0
    list_inv = []
    exist_error = False
    result = {}

    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter=colum_dataset['delimitador'])

        for fila in csv_reader:
            valor_lat = fila[colum_dataset["latitud"]]
            valor_lon = fila[colum_dataset["longitud"]]
            if not lat and not lon:
                lat_invalida = evaluar_error(valor_lat, -90, 90)
                lon_invalida = evaluar_error(valor_lon, -180, 180)
            if lat:
                lat_invalida = evaluar_error(valor_lat, -90, 90)
                lon_invalida = False
            elif lon:
                lon_invalida = evaluar_error(valor_lon, -180, 180)
                lat_invalida = False

            if lat_invalida or lon_invalida:
                cant_inv += 1
                exist_error = True
                list_inv.append(fila[colum_dataset["id"]])
    result ={
        'cantidad_invalidos' : cant_inv,
        'lista_invalidos' : list_inv,
        'existe_error' : exist_error
    }
    return result

#3.B
def constatar_coordenadas(dataset,path):
    exist_error = False
    cant_inconsistentes = 0
    list_ids = []
    print("Evaluando inconsistencias en las coordenadas...")
    if dataset not in TRADUCTOR_DATASETS:
            raise ValueError(
                f"Dataset '{dataset}' no reconocido. "
                f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
            )
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]

    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])
        for fila in csv_reader:
            lat = fila[colum_dataset["latitud"]]
            lon = fila[colum_dataset["longitud"]]
            if (lat == '') != (lon == ''):  # XOR: inconsistencia solo si UNA está vacía
                cant_inconsistentes +=1
                exist_error = True
                list_ids.append(fila[colum_dataset["id"]])
    result = {
        'cantidad_inconsistencias' : cant_inconsistentes,
        'lista_ids' : list_ids,
        'existe_error' : exist_error
    }
    return result

#3.C
def validar_fechas(dataset,path):
    anio_post = 0
    fecha_inv = 0
    exist_error = False
    print("Evaluando fechas del dataset...")
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    colum_dataset = TRADUCTOR_DATASETS[dataset]

    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])

        for fila in csv_reader:
            for columna_fecha in colum_dataset["fecha"]:
                if columna_fecha not in fila:
                    continue
                valor = fila[columna_fecha]
                if not valor:
                    continue
                try:
                    # 'Z' (UTC) solo es soportado por fromisoformat desde Python 3.11
                    fecha = datetime.fromisoformat(valor.replace('Z', '+00:00'))
                    if fecha.year > 2026:
                        anio_post += 1
                        exist_error = True
                #Si la fecha no concuerda con el formate ISO significa que es una fecha invalida
                except (ValueError,TypeError):
                    fecha_inv += 1
                    exist_error = True
    result = {
        'anios_posteriores' : anio_post,
        'fechas_invalidas' : fecha_inv,
        'existe_error' : exist_error
    }
    return result

#3.D
def verificar_duplicados(dataset,path):
    duplicados = []
    cant_dupli = 0
    exist_error = False
    set_id = set()

    print("Evaluando registros repetidos del dataset...")
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    colum_dataset = TRADUCTOR_DATASETS[dataset]

    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])

        for fila in csv_reader:
            if fila[colum_dataset["id"]] in set_id:
                duplicados.append(fila[colum_dataset["id"]])
                cant_dupli += 1
                exist_error = True
            else:
                set_id.add(fila[colum_dataset["id"]])
    result = {
        'cantidad_duplicados' : cant_dupli,
        'id_duplicados' : duplicados,
        'existe_error' : exist_error
    }
    return result

#3.E
def verificar_countryCode(dataset,path):
    exist_error = False
    list_ids = []
    print("Evaluando errores en el campo 'countryCode' del dataset...")
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    colum_dataset = TRADUCTOR_DATASETS[dataset]
    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])

        for fila in csv_reader:
            valor = fila[colum_dataset["pais"]]
            if not valor:
                continue
            if colum_dataset['tipo_pais'] == 'alpha_2':
                pais = pycountry.countries.get(alpha_2=valor)
            else:
                pais = pycountry.countries.get(name=valor)
            if pais is None:
                print(f"El pais '{valor}' no es valido")
                exist_error = True
                list_ids.append(fila[colum_dataset["id"]])
    result = {
        'lista_ids' : list_ids,
        'existe_error' : exist_error
    }
    return result

#3.F
def verificar_incertidumbre(dataset,path):
    fuera_rango = 0
    no_dato = 0
    exist_error = False
    list_ids = []
    print("Evaluando errores en el campo 'coordinateUncertaintyInMeters' del dataset...")
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    colum_dataset = TRADUCTOR_DATASETS[dataset]

    if not colum_dataset['coordenada_rango']:
        return {
            'dato_invalido': 0,
            'no_dato': 0,
            'lista_ids': [],
            'existe_error': False
        }

    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])

        for fila in csv_reader:
            valor = fila[colum_dataset["coordenada_rango"]]
            if not valor:
                continue
            try:
                rango = float(valor)
                if rango < 0 or rango > 100:
                    fuera_rango += 1
                    exist_error = True
                    list_ids.append(fila[colum_dataset["id"]])
            except ValueError:
                no_dato += 1
                exist_error = True
                list_ids.append(fila[colum_dataset["id"]])
    result = {
        'dato_invalido' : fuera_rango,
        'no_dato' : no_dato,
        'lista_ids' : list_ids,
        'existe_error' : exist_error
    }
    return result

#3.G
def resumen_calidad(dataset,path):
    cant_regist = count_records(path)
    result_coor = validar_coordenadas(dataset,path)
    result_consist = constatar_coordenadas(dataset,path)
    result_fechas = validar_fechas(dataset,path)
    result_dupli = verificar_duplicados(dataset,path)
    result_taxo = errores_taxonomicos(dataset,path)
    total_fechas = result_fechas['anios_posteriores'] + result_fechas['fechas_invalidas']
    resumen = {
            'registro' : cant_regist,
            'error_coordenadas' : result_coor['cantidad_invalidos'],
            'inconsistencias_coordenadas' : result_consist['cantidad_inconsistencias'],
            'error_fechas' : total_fechas,
            'duplicados' : result_dupli['cantidad_duplicados'],
            'error_taxonomico' : result_taxo
    }

    # TITULO
    print("\n" + "*" * 50)
    print(f"RESUMEN DE CALIDAD DEL DATASET {dataset}")
    print("*" * 50)
       # INFORMACION DE ERRORES
    print(f"Cantidad total de registros analizados: {cant_regist}")
    print("-" * 50)
    print(f"Cantidad de errores en las coordenadas 'latitud' y 'longitud': {resumen['error_coordenadas']}")
    print(f"Cantidad de inconsistencias en coordenadas (lat sin lon o viceversa): {resumen['inconsistencias_coordenadas']}")
    print(f"Cantidad de errores en las fechas: {total_fechas}")
    print(f"Cantidad de datos duplicados: {resumen['duplicados']}")
    print(f"Cantidad de registros con informacion taxonomica incompleta: {result_taxo}")

    
    return resumen

#3.H
def evaluar_cotas_america(dataset,path,lat = False, lon = False):
    lat_inv = 0
    lon_inv = 0
    list_ids = []
    exist_error = False
    print("Evaluando cotas de coordenadas (America del sur) del dataset...")
    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )
    colum_dataset = TRADUCTOR_DATASETS[dataset]
    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file,delimiter = colum_dataset['delimitador'])

        for fila in csv_reader:
            valor_lat = fila[colum_dataset["latitud"]]
            valor_lon = fila[colum_dataset["longitud"]]
            id_fila = fila[colum_dataset["id"]]
            lat_invalida = evaluar_error(valor_lat, LATITUD_SUR, LATITUD_NORTE) and not lon
            lon_invalida = evaluar_error(valor_lon, LONGITUD_OESTE, LONGITUD_ESTE) and not lat
            if lat_invalida:
                lat_inv += 1
                exist_error = True
            if lon_invalida:
                lon_inv += 1
                exist_error = True
            if lat_invalida or lon_invalida:
                if id_fila not in list_ids:
                    list_ids.append(id_fila)
    if lat:
        return {
            'latitudes_invalidas' : lat_inv,
            'lista_ids' : list_ids,
            'existe_error' : exist_error
        }
    elif lon:
        return {
            'longitudes_invalidas' : lon_inv,
            'lista_ids' : list_ids,
            'existe_error' : exist_error
        }
    else:
        return {
            'latitudes_invalidas' : lat_inv,
            'longitudes_invalidas' : lon_inv,
            'lista_ids' : list_ids,
            'existe_error' : exist_error
        }

#3.I 
def validar_longitud(dataset, path):
    result_cotas = evaluar_cotas_america(dataset,path,lon=True)
    result_coor = validar_coordenadas(dataset,path,lon=True)
    resultado_lon = {
        'resultado_cotas' : result_cotas,
        'resultado_coordenadas' : result_coor
    }
    return resultado_lon

def validar_latitud(dataset,path):
    result_cotas = evaluar_cotas_america(dataset,path,lat=True)
    result_coor = validar_coordenadas(dataset,path,lat=True)
    resultado_lat = {
        'resultado_cotas' : result_cotas,
        'resultado_coordenadas' : result_coor
    }
    return resultado_lat

#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    def datos(dato):
        dato = input('Ingrese que dataset quiere verificar (iadiza - inaturalist - xenocanto):')
        return dato

    lista = []
    dato = ''
    cant = 0
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'inaturalist' / 'observations.csv'
    dato = datos(dato)
    """
    resultado = validar_coordenadas(dato,file_route)
    print(f"La cantidad de registro invalidos son {resultado["cantidad_invalidos"]}")
    for i in resultado["lista_invalidos"]:
        print(f"Los registros invalidos son {i}")

    resultado = constatar_coordenadas(dato,file_route)
    print(f"La cantidad de inconsistencias son: {resultado["cantidad_inconsistencias"]}")
    for i in resultado["lista_ids"]:
        print(f"Los ids incosistentes son:{i}")

    resultado = validar_fechas(dato,file_route)
    print(f"La cantidad de fechas posteriores a 2026 son:{resultado["anios_posteriores"]}")

    resultado = verificar_duplicados(dato,file_route)
    for i in resultado["id_duplicados"]:
        print(f"Los IDS duplicados son :{i}")
    print(f"La cantidad de datos duplicados son :{resultado["cantidad_duplicados"]}")

    resultado = verificar_countryCode(dato,file_route)
    for i in resultado["lista_ids"]:
        print(f"Los IDS invalidos son:{i}")

    resultado = verificar_incertidumbre(dato,file_route)
    for i in resultado["lista_ids"]:
        print(f"Los IDS invalidos son:{i}")

    dict_resumen = resumen_calidad(dato,file_route)

    resultado = evaluar_cotas_america(dato,file_route)
    print(f"Cotas seteadas para la latitud -- NORTE:{LATITUD_NORTE} | SUR:{LATITUD_SUR}")
    print(f"Cantidad de datos invalidos:{resultado["latidudes_invalidas"]}")
    print("")
    print(f"Cotas seteadas para la longitud -- ESTE:{LONGITUD_ESTE} | OESTE:{LONGITUD_OESTE}")
    print(f"Cantidad de datos invalidos:{resultado["longitudes_invalidas"]}")
    """
    resultado_latitud = validar_latitud(dato,file_route)
    if resultado_latitud['resultado_cotas']['existe_error']:
        print("Funco latitud cotas")
    if resultado_latitud['resultado_coordenadas']['existe_error']:
        print("Funco latitud coordenadas")
    resultado_longitud = validar_longitud(dato,file_route)
    if resultado_longitud['resultado_cotas']['existe_error']:
        print("Funco longitud cotas")
    if resultado_longitud['resultado_coordenadas']['existe_error']:
        print("Funco longitud coordenadas")
