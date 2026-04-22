from pathlib import Path
from datetime import datetime
import csv
import pycountry

# Funcion para abrir el archivo con el path enviado
def evaluar_error(valor,nombreColumna):
    error = False

    if 'latitude' in nombreColumna:
        if valor < -90 or valor > 90:
            error = True
    if 'longitude' in nombreColumna:
        if valor < -180 or valor > 180:
            error = True
    return error
# 3.A
def validar_coordenadas(nombreColumna,path,delimitador):
    cant_inv = 0
    list_inv = []
    colum_vacio = True
    print("Buscando errores en los datos de latitud...")
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"

    with open(path, "r") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")
            return cant_inv, list_inv
        if nombreColumna not in csv_reader.fieldnames:
            print(f"La columna {nombreColumna} no existe en el dataset")
            return cant_inv, list_inv

        # Recorre la columna enviada para buscar errores
        for fila in csv_reader:
        # Evaluo si existe un valor en ese registro
            valor = fila[nombreColumna]
            if valor != '':
                colum_vacia = False
                # Utilizo el try/except para valores que no son numeros
                try:
                    coord = float(valor)
                    # La funcion evaluar_error devuelve True si encuentra un error
                    if evaluar_error(coord,nombreColumna):
                        cant_inv += 1
                        list_inv.append(coord)
                except (ValueError, TypeError):
                    cant_inv += 1
                    list_inv.append(valor)

    if colum_vacia:
        print("No existen valores en la columna o la columna enviada en invalida")
    return cant_inv, list_inv

#3.B
def constatar_coordenadas(primer_colum,segunda_colum,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    colum_vacia = True
    print("Evaluando inconsistencias en las coordenadas...")
    with open(path, "r") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        if primer_colum not in csv_reader.fieldnames:
            print(f"La columna {primer_colum} no existe en el dataset")
            return
        elif segunda_colum not in csv_reader.fieldnames:
            print(f"La columna {segunda_colum} no existe en el dataset")
            return

        for fila in csv_reader:
            if  fila[primer_colum] == '' and fila[segunda_colum] == '':
                pass
                #print(f"Existe una inconsistencia en ambos registros -- linea {csv_reader.line_num} ")
            elif fila[primer_colum] == '' or fila[segunda_colum] == '':
                colum_vacia = False
                #print(f"Existe una inconsistencia en un registro -- linea {csv_reader.line_num}")
            if colum_vacia: print("Las columnas enviadas no poseen datos")
    return

#3.C
def validar_fechas(nombre_columna,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    anio_post = 0
    cant = 0
    colum_vacia = True
    print("Evaluando fechas del dataset...")

    with open(path, "r") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        if nombre_columna not in csv_reader.fieldnames:
            print(f"La columna {nombre_columna} no existe en el dataset")
            return

        for fila in csv_reader:
            try:
                #convierte el string formate ISO en un dato tipo datetime
                fecha = datetime.fromisoformat(fila[nombre_columna])
                if fecha.year > 2026: anio_post += 1
            #Si la fecha no concuerda con el formate ISO significa que es una fecha invalida
            except (ValueError,TypeError):
                cant += 1
                #print("La fecha posee un formato invalido o no se puede interpretar como una")
        print(F"La cantidad de fechas invalidas son {cant}")
    return anio_post

#3.D
def verificar_duplicados(nombre_columna,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    colum_vacia = True
    duplicados = []
    cant_dupli = 0
    set_id = set()

    print("Evaluando registros repetidos del dataset...")

    with open(path, "r") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        if nombre_columna not in csv_reader.fieldnames:
            print(f"La columna {nombre_columna} no existe en el dataset")
            return
        for fila in csv_reader:
            if fila[nombre_columna] in set_id:
                duplicados.append(fila[nombre_columna])
                cant_dupli += 1
            else:
                set_id.add(fila[nombre_columna]) 
    return cant_dupli, duplicados

#3.E
def verificar_countryCode(nombre_columna,path,delimitador):
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"
    colum_vacia = True

    print("Evaluando errores del campo 'countryCode' del dataset...")

    with open(path, "r") as file:
        try:
            csv_reader = csv.DictReader(file,delimiter = delimitador)
        except TypeError:
            print("Ingrese un delimitador valido")

        if nombre_columna not in csv_reader.fieldnames:
            print(f"La columna {nombre_columna} no existe en el dataset")
            return
        for fila in csv_reader:
            pais = pycountry.countries.get(alpha_2=fila[nombre_columna])
            if pais == none:
                print(F"El codigo {fila[nombre_columna] no es valida")
    return
#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    def datos(dato,delimitador):
        dato = input('Ingrese que columna quiere verificar:')
        delimitador = input('Ingrese el delimitador del dataset:')
        return dato,delimitador
    lista = []
    cant = 0
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'bird-sounds' / 'Occurrence.txt'
    """
    dato, delimitador = datos(dato,delimitador)
    cant, lista = validar_coordenadas(file_route,dato,delimitador)
    print(f"La cantidad de registro invalidos son {cant}")
    for i in range(len(lista)):
        print(f"Los registros invalidos son {lista[i]}")

    dato1 = input('Ingrese la primer columna:')
    dato2 = input('Ingrese la segunda columna:')
    delimitador = input('Ingrese el delimitador del dataset:')
    constatar_coordenadas(dato1, dato2,file_route,delimitador)
    

    dato,delimitador = datos(dato, delimitador)
    cant = validar_fechas(dato,file_route,delimitador)
    print(f"La cantidad de fechas posteriores a 2026 son:{cant}")
    
    dato, delimitador = datos(dato, delimitador)
    cant,lista = verificar_duplicados(dato,file_route,delimitador)
    for i in range(len(lista)):
        print(f"Los IDS duplicados son :{lista[i]}")
    print(f"La cantidad de datos duplicados son :{cant}")
    """
    dato, delimitador = datos(dato, delimitador)
    verificar_countryCode(dato,file_route,delimitador)
