from pathlib import Path
import csv
# Funcion para verificar que el iterador enviado es correcto
def validar_archivo(csv,nombreColumna):
    # Compruebo que el tipo de dato es un iterador
    if not hasattr(csv, "__iter__"):
        print("El tipo de dato no es un iterador")
        return True
    # Compruebo que exista la columna enviada
    if nombreColumna not in csv.fieldnames:
        print("La columna es incorrecta o no existe en el dataset")
        return True
return False
# 3.A
def validar_coordenadas(csv,nombreColumna):
    cant_inv = 0
    list_inv = []
    colum_vacio = True
    print("Buscando errores en los datos de latitud...")
    if validar_archivo(csv,nombreColumna): return cant_inv, list_inv
    # Recorre la columna enviada para buscar errores
    for fila in csv:
    # Evaluo si existe un valor en ese registro
        valor = fila[nombreColumna]
        if valor != '':
            colum_vacia = False
            coord = float(valor)
            if 'latitude' in nombreColumna:
                if coord < -90 or coord > 90:
                    cant_inv += 1
                    list_inv.append(coord)
            if 'longitude' in nombreColumna:
                if coord < -180 or coord > 180:
                    cant_inv += 1
                    list_inv.append(coord)

    if colum_vacia:
        print("No existen valores en la columna o la columna enviada en invalida")
    return cant_inv, list_inv

#3.B
def constatar_coordenadas()

#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    list = []
    cant = 0
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'bird-sounds' / 'Occurrence.txt'

    with open(file_route, "r") as file:
        csv_file = csv.DictReader(file,delimiter=',')
        print(csv_file.fieldnames)
        dato = input('Ingrese que columna quiere verificar:')
        cant, lista = validar_coordenadas(csv_file,dato)
        print(f"La cantidad de registro invalidos son {cant}")
        for i in range(len(lista)):
            print(f"Los registros invalidos son {lista[i]})


