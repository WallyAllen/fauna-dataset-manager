from pathlib import Path
import csv
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
def validar_coordenadas(path,nombreColumna,delimitador):
    cant_inv = 0
    list_inv = []
    colum_vacio = True
    print("Buscando errores en los datos de latitud...")
    if delimitador == "\\t" or delimitador == "/t" : delimitador = "\t"

    with open(path, "r") as file:
        csv_reader = csv.DictReader(file,delimiter = delimitador)

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
#def constatar_coordenadas()

#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    list = []
    cant = 0
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'bird-sounds' / 'Occurrence.txt'

    dato = input('Ingrese que columna quiere verificar:')
    delimitador = input('Ingrese el delimitador del dataset:')
    cant, lista = validar_coordenadas(file_route,dato,delimitador)
    print(f"La cantidad de registro invalidos son {cant}")
    for i in range(len(lista)):
        print(f"Los registros invalidos son {lista[i]}")


