import datetime as dt

def current_date():
    """
    Ejercicio 7.A
    This function returns the current date time in a YYYY-MM-DD HH:MM:SS format, fixed to UTC-3 (Argentina Standard Timezone).
    """
    tz_ar = dt.timezone(dt.timedelta(hours=-3))
    now = dt.datetime.now(tz_ar)
    return now.strftime("%Y-%m-%d %H:%M:%S")

print(f"La hora actual es {current_date()}")