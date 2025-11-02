import csv
import os

# Ruta del archivo CSV
RUTA_ARCHIVO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "atenciones.csv")

def guardar_en_csv(lista_atenciones):
    """
    Guarda la lista de atenciones en el archivo CSV.
    Si el archivo no existe, lo crea con encabezados.
    """
    try:
        # Asegurarse de que el directorio data exista
        os.makedirs(os.path.dirname(RUTA_ARCHIVO), exist_ok=True)

        # Definir encabezados
        campos = ["nombre", "servicio", "responsable", "fecha", "resultado", "estado"]

        # Abrir el archivo en modo escritura
        with open(RUTA_ARCHIVO, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()

            for atencion in lista_atenciones:
                # Convertir cada objeto a diccionario
                if hasattr(atencion, "to_dict"):
                    escritor.writerow(atencion.to_dict())
                else:
                    escritor.writerow(atencion)

        print(f"\n✅ Reporte guardado correctamente en '{RUTA_ARCHIVO}'")

    except Exception as e:
        print(f"❌ Error al guardar el archivo CSV: {e}")


def leer_atenciones():
    """
    Lee las atenciones desde el archivo CSV, si existe.
    Retorna una lista de diccionarios con los datos.
    """
    if not os.path.exists(RUTA_ARCHIVO):
        return []

    try:
        with open(RUTA_ARCHIVO, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return [fila for fila in lector]
    except Exception as e:
        print(f"❌ Error al leer el archivo CSV: {e}")
        return []
