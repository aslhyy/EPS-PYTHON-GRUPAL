from datetime import datetime


# Clase que representa una atencion medica en el sistema
class Atencion:
    def __init__(self, nombre, servicio, responsable, fecha, resultado):
        # Revisamos que todos los campos estén completos
        if not all([nombre, servicio, responsable, fecha, resultado]):
            raise ValueError("Por favor completa todos los campos.")

        # Revisamos que la fecha tenga el formato correcto
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD.")

        # Guardamos los datos
        self.nombre = nombre
        self.servicio = servicio
        self.responsable = responsable
        self.fecha = fecha
        self.resultado = resultado

    def to_dict(self):
        # Conviertimos los datos a diccionario
        return {
            "nombre": self.nombre,
            "servicio": self.servicio,
            "responsable": self.responsable,
            "fecha": self.fecha,
            "resultado": self.resultado,
        }

    def __str__(self):
        return f"{self.fecha} - {self.nombre} ({self.servicio}) → {self.resultado}"
