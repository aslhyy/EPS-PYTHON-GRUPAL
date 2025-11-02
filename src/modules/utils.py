# modules/utils.py
import os, datetime

def validar_fecha(fecha):
    try:
        datetime.datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
