import os
import datetime

def validar_fecha(fecha):
    try:
        fecha_ingresada = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()

        fecha_actual = datetime.date.today()
        
        if fecha_ingresada < fecha_actual:
            print("⚠️ No se puede registrar una fecha anterior a la actual.")
            return False
        
        return True
    except ValueError:
        print("⚠️ Formato de fecha inválido. Use YYYY-MM-DD (ej: 2025-11-02).")
        return False


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


