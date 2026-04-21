from pathlib import Path
import csv
# EJERCICIO 3.A
def validar_coordenadas(csv,nombreColumna):
    cant_inv = 0
    list_inv = []
    colum_vacia = True
    # Compruebo que el tipo de dato es un iterador
    if hasattr(csv, "__iter__"):
        print("Buscando errores en los datos de latitud...")
        # Recorre la columna enviada para buscar errores
        for fila in csv:
            # Evaluo si existe un valor en ese registro
            valor = fila[nombreColumna]
            if valor != '' and 'latitude' in nombreColumna:
                colum_vacia = False
                latitud = float(valor)
                if latitud < -90 or latitud > 90:
                    cant_inv += 1
                    list_inv.append(latitud)
            else: print('El nombre de la columna es incorrecto o no existe en el dataset')
        
        if colum_vacia:
            print("No existen valores en la columna 'decimalLatitude'")
    else:
        print("El tipo de dato no es un iterador")
        

#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'bird-sounds' / 'Occurrence.txt'

    with open(file_route, "r") as file:
        csv_file = csv.DictReader(file,delimiter=',')
        print(csv_file.fieldnames)
        dato = input('Ingrese que columna quiere verificar:')
        validar_coordenadas(csv_file,dato)


        # Comprobacion para saber si se cargo bien el archivo
        """
        i = 0
        for fila in csv_file:
            i += 1
            if i < 2:
                print(f"La localidad es {fila['locality']}")
                print(f"La latitud es {fila['decimalLatitude']}")
            else:
                break
        """


