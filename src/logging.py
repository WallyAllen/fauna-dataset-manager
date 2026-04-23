import datetime as dt
from pathlib import Path

def current_date():
    """
    Ejercicio 7.A
    This function returns the current date time in a YYYY-MM-DD HH:MM:SS format, fixed to UTC-3 (Argentina Standard Timezone).
    """
    tz_ar = dt.timezone(dt.timedelta(hours=-3))
    now = dt.datetime.now(tz_ar)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log(dataset, op_type, affected, status=None):
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_FILE = BASE_DIR / "logs" / "operations.log"
    error_tag = " | ERROR" if status is None else ""
    try:
        with open(LOG_FILE, "a") as file:
            file.write(f"{current_date()} | {dataset} | {op_type} | {affected} registros{error_tag}\n")
    except FileNotFoundError:
        print("ERROR: No existe la carpeta logs en el directorio.")
    except PermissionError:
        print("ERROR: No hay permisos de escritura para el usuario.")
    except OSError:
        print("ERROR: Errores varios en la operación del archivo, más información en ")