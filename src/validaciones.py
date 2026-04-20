#EJERCICIO 3.A
from pathlib import Path
import csv


#Bloque para probar las funciones de validacion
if __name__ == "__main__":
    #Creo una variable con la ruta de archivo dinamica
    DIC_BASE = Path(__file__).resolve().parent.parent

    file_route = DIC_BASE / 'raw_datasets' / 'coleccion-ornitologica' / 'occurrence.txt'
    print(f"Buscando en {file_route}")
    with open(file_route, "r") as file:
        csv_file = csv.DictReader(file,delimiter='\t')
        type(csv_file)
        i = 0
        for fila in csv_file:
            i += 1
            if i < 2:
                print(f"La localidad es {fila['locality']}")
                print(f"La latitud es {fila['decimalLatitude']}")
            else:
                break

