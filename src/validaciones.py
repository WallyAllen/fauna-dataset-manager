from pathlib import Path
from datetime import datetime
import csv
import pycountry
from src.lectura import count_records

TRADUCTOR_DATASETS ={
    'iadiza': {
        'latitud' : 'decimalLatitude',
        'longitud' : 'decimalLongitude',
        'fecha' : 'eventDate',
        'id' : 'gbifID',
        'pais' : 'countryCode',
        'coordenada_rango' : '',
        'taxonomica' : ['scientificName','kingdom','phylum',
                        'class','order','family','genus',
                        'specificEpithet','taxonRank'] 
    },
    'inaturalist': {
        'latitud' : 'decimalLatitude',
        'longitud' : 'decimalLongitude',
        'fecha' : 'eventDate',
        'id' : 'id',
        'pais' : 'countryCode',
        'coordenada_rango' : 'coordinateUncertaintyInMeters',
        'taxonomica' : ['scientificName','taxonID',
                        'taxonRank','kingdom','phylum',
                        'class','order','family','genus']
    },
    'xenocanto' : {
        'latitud' : 'latitudeDecimal',
        'longitud' : 'longitudeDecimal',
        'fecha' : 'eventDate',
        'id' : 'id',
        'pais' : 'country',
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
def errores_taxonomicos(dataset,path,delimitador):
    cant_errores = 0
    print("Buscando errores en los datos taxonomicos...")
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
 
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return cant_errores
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]
    
    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")
            return cant_errores
        for fila in csv_reader:
            for i in range(len(colum_dataset["taxonomica"])):
                if fila[colum_dataset["taxonomica"][i]] == "":
                    cant_errores += 1

    return cant_errores

# 3.A
def validar_coordenadas(dataset, path, delimitador):
    """
    Ejercicio 3.A
    Detecta registros con coordenadas geográficas inválidas.

    Args:
        dataset (str): Nombre del dataset ('iadiza', 'inaturalist', 'xenocanto')
        path (str | Path): Ruta al archivo CSV
        delimitador (str): Separador de campos del archivo

    Returns:
        tuple:
            - exist_error (bool): True si hay al menos un registro inválido
            - cant_inv (int): Cantidad de REGISTROS inválidos
            - list_inv (list[str]): IDs de los registros inválidos

    Raises:
        ValueError: Si el dataset no está en TRADUCTOR_DATASETS
        ValueError: Si el delimitador no es un string de un carácter
    """
    if delimitador in ("\\t", "/t"):
        delimitador = "\t"

    if dataset not in TRADUCTOR_DATASETS:
        raise ValueError(
            f"Dataset '{dataset}' no reconocido. "
            f"Opciones válidas: {list(TRADUCTOR_DATASETS.keys())}"
        )

    colum_dataset = TRADUCTOR_DATASETS[dataset]
    cant_inv = 0
    list_inv = []
    exist_error = False

    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file, delimiter=delimitador)
        except TypeError as e:
            raise ValueError(f"Delimitador inválido: {e}")

        for fila in csv_reader:
            valor_lat = fila[colum_dataset["latitud"]]
            valor_lon = fila[colum_dataset["longitud"]]

            lat_invalida = evaluar_error(valor_lat, -90, 90)
            lon_invalida = evaluar_error(valor_lon, -180, 180)

            if lat_invalida or lon_invalida:
                cant_inv += 1
                exist_error = True
                list_inv.append(fila[colum_dataset["id"]])

    return exist_error, cant_inv, list_inv

#3.B
def constatar_coordenadas(dataset,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    colum_vacia = True
    exist_error = False
    print("Evaluando inconsistencias en las coordenadas...")
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return exist_error
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]

    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        for fila in csv_reader:
            if  fila[colum_dataset["latitud"]] == '' and fila[colum_dataset["longitud"]] == '':
                pass
                colum_vacia = False
                print(f"Existe una inconsistencia en ambos registros -- linea {csv_reader.line_num} ")
            elif fila[colum_dataset["latitud"]] == '' or fila[colum_dataset["longitud"]] == '':
                colum_vacia = False
                exist_error = True
                print(f"Existe una inconsistencia en un registro -- linea {csv_reader.line_num}")
        if colum_vacia: print("No existen inconsistencia en las columnas de 'latidud' y 'longitud' ")
    return exist_error

#3.C
def validar_fechas(dataset,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    anio_post = 0
    fecha_inv = 0
    exist_error = False
    print("Evaluando fechas del dataset...")
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return anio_post,fecha_inv,exist_error
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]

    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        for fila in csv_reader:
            try:
                #convierte el string formate ISO en un dato tipo datetime
                fecha = datetime.fromisoformat(fila[colum_dataset["fecha"]])
                if fecha.year > 2026: 
                    anio_post += 1
                    exist_error = True
            #Si la fecha no concuerda con el formate ISO significa que es una fecha invalida
            except (ValueError,TypeError):
                fecha_inv += 1
                exist_error = True
                #print("La fecha posee un formato invalido o no se puede interpretar como una")
    return anio_post,fecha_inv, exist_error

#3.D
def verificar_duplicados(dataset,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    duplicados = []
    cant_dupli = 0
    exist_error = False
    set_id = set()

    print("Evaluando registros repetidos del dataset...")
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return cant_dupli, duplicados,exist_error
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]

    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        for fila in csv_reader:
            if fila[colum_dataset["id"]] in set_id:
                duplicados.append(fila[colum_dataset["id"]])
                cant_dupli += 1
                exist_error = True
            else:
                set_id.add(fila[colum_dataset["id"]]) 
    return cant_dupli, duplicados,exist_error

#3.E
def verificar_countryCode(dataset,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    exist_error = False
    print("Evaluando errores en el campo 'countryCode' del dataset...")
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]
    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        for fila in csv_reader:
            pais = pycountry.countries.get(alpha_2=fila[colum_dataset["pais"]])
            if pais == None:
                print(f"El codigo {fila[colum_dataset["pais"]]} no es valido")
                exist_error = True
    return exist_error

#3.F
def verificar_incertidumbre(dataset,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    fuera_rango = 0
    no_dato = 0
    exist_error = false
    print("Evaluando errores en el campo 'coordinateUncertainyInMeters' del dataset...")
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return exist_error
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]
    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        for fila in csv_reader:
            try:
                rango = float(fila[colum_dataset["coordenada_rango"]])
                if rango < 0: 
                    fuera_rango += 1
                    exist_error = True
                elif rango > 100:
                    fuera_rango += 1
                    exist_error = true
            except ValueError:
                no_dato += 1
                exist_error = True
        print(f"La cantidad de datos no validos son: {fuera_rango}")
        print(f"La cantidad de datos no numericos son: {no_dato}")
    return exist_error

#3.G
def resumen_calidad(dataset,path,delimitador):
    cant_regist = count_records(path)
    cant_inv = validar_coordenadas(dataset,path,delimitador)
    cant_fechas = validar_fechas(dataset,path,delimitador)
    cant_dupli = verificar_duplicados(dataset,path,delimitador)
    cant_taxo = errores_taxonomicos(dataset,path,delimitador)
    resumen = {
            'registro' : cant_regist,
            'error_coordenadas' : cant_inv,
            'error_fechas' : cant_fechas,
            'duplicados' : cant_dupli,
            'error_taxonomico' : cant_taxo
    }

    # TITULO
    print("\n" + "*" * 50)
    print(f"RESUMEN DE CALIDAD DEL DATASET {dataset}")
    print("*" * 50)
    total_fechas = resumen['error_fechas'][1] + resumen['error_fechas'][2]
    # INFORMACION DE ERRORES
    print(f"Cantidad total de registros analizados: {cant_regist}")
    print("-" * 50)
    print(f"Cantidad de errores en las coordenadas 'latitud' y 'longitud': {resumen['error_coordenadas'][1]}")
    print(f"Cantidad de errores en las fechas: {total_fechas}")
    print(f"Cantidad de datos duplicados: {resumen['duplicados'][1]}")
    print(f"Cantidad de registros con informacion taxonomica incompleta: {resumen['error_taxonomico']}")

    
    return resumen

#3.H
def evaluar_cotas_america(dataset,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    lat_inv = 0
    lon_inv = 0
    exist_error = False
    print("Evaluando cotas de coordenadas (America del sur) del dataset...")
    if dataset not in TRADUCTOR_DATASETS.keys():
            print(f"El dataset {dataset} no existe")
            return exist_error
    else: colum_dataset = TRADUCTOR_DATASETS[dataset]
    with open(path, "r", encoding="utf-8") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        for fila in csv_reader:
            valor_lat = fila[colum_dataset["latitud"]]
            valor_lon = fila[colum_dataset["longitud"]]
            if evaluar_error(valor_lat,LATITUD_SUR,LATITUD_NORTE):
                lat_inv += 1
                exist_error = True
            if evaluar_error(valor_lon,LONGITUD_OESTE,LONGITUD_ESTE):
                lon_inv += 1
                exist_error = True
    return exist_error, lat_inv, lon_inv

#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    def datos(dato,delimitador):
        dato = input('Ingrese que dataset quiere verificar (iadiza - inaturalist - xenocanto):')
        delimitador = input('Ingrese el delimitador del dataset:')
        return dato,delimitador

    lista = []
    dato = ''
    delimitador = ''
    cant = 0
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'inaturalist-filtered' / 'observations.csv'
    dato, delimitador = datos(dato,delimitador)
    """
    cant, lista = validar_coordenadas(dato,file_route,delimitador)
    print(f"La cantidad de registro invalidos son {cant}")
    for i in range(len(lista)):
        print(f"Los registros invalidos son {lista[i]}")

    
    constatar_coordenadas(dato,file_route,delimitador)

    cant = validar_fechas(dato,file_route,delimitador)
    print(f"La cantidad de fechas posteriores a 2026 son:{cant}")

    cant,lista = verificar_duplicados(dato,file_route,delimitador)
    for i in range(len(lista)):
        print(f"Los IDS duplicados son :{lista[i]}")
    print(f"La cantidad de datos duplicados son :{cant}")

    verificar_countryCode(dato,file_route,delimitador)

    verificar_incertidumbre(dato,file_route,delimitador)
    
    dict_resumen = resumen_calidad(dato,file_route,delimitador)
    """
    latitud, longitud = evaluar_cotas_america(dato,file_route,delimitador)
    print(f"Cotas seteadas para la latitud -- NORTE:{LATITUD_NORTE} | SUR:{LATITUD_SUR}")
    print(f"Cantidad de datos invalidos:{latitud}")
    print("")
    print(f"Cotas seteadas para la longitud -- ESTE:{LONGITUD_ESTE} | OESTE:{LONGITUD_OESTE}")
    print(f"Cantidad de datos invalidos:{longitud}")

