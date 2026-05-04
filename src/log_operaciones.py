import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "operations.log"

def current_date():
    """
    Ejercicio 7.A
    Retorna la fecha y hora actual en un formato "YYYY-MM-DD HH:MM:SS",
    usando la zona horaria UTC-3 (Argentina).

    Returns:
        str: Fecha y hora formateadas.
    """
    tz_ar = dt.timezone(dt.timedelta(hours=-3))
    now = dt.datetime.now(tz_ar)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log(dataset, op_type, affected, status=None):
    """
    Ejercicio 7.B
    Registra en `logs/operations.log` una línea con la fecha/hora actual y 
    datos de la operación realizada sobre un dataset.

    Sigue el formato:
    "<fecha_hora> | <dataset> | <tipo_operacion> | <affected> registros[ | ERROR] (si aplica)"

    Args:
        dataset (str): Nombre del dataset sobre el que se ejecutó la operación.
        op_type (str): Tipo de operación registrada. (ej: "INSERT", "DELETE", "UPDATE").
        affected (int): Cantidad de registros afectados por la operación.
        status (opcional): Indicador de estado. Si no es `None`, se agrega la etiqueta
            "ERROR" al final del registro. Por default, es `None`.
    
    Crea la carpeta y el archivo si no existen, agrega la línea sin
    sobreescribir el contenido previo.
    """

    error_tag = " | ERROR" if status is not None else ""
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(f"{current_date()} | {dataset} | {op_type} | {affected} registros{error_tag}\n")
    except PermissionError:
        print("ERROR: No hay permisos de escritura para el usuario.")
    except OSError as e:
        print(f"ERROR: Error de archivo/sistema. Detalle: {e}")