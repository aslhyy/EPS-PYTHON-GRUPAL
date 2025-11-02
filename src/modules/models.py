from datetime import datetime


# Clase que representa una atencion medica en el sistema
class Atencion:
    def __init__(self, nombre, servicio, responsable, fecha, resultado, estado):
        # Revisamos que todos los campos estén completos
        if not all([nombre, servicio, responsable, fecha, resultado, estado]):
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
        self.estado = estado

    def to_dict(self):
        # Conviertimos los datos a diccionario
        return {
            "nombre": self.nombre,
            "servicio": self.servicio,
            "responsable": self.responsable,
            "fecha": self.fecha,
            "resultado": self.resultado,
            "estado": self.estado
        }

    def __str__(self):
        return f"{self.fecha} - {self.nombre} ({self.servicio}) → {self.resultado} [Estado: {self.estado}]"


# Clase encargada de guardar y manejar todas las atenciones
class GestorAtenciones:
    def __init__(self):
        # guardaremos todas las atenciones en una lista
        self.atenciones = []

    def agregar_atencion(self, atencion):
        # Agrega una nueva atencion a la lista
        if not isinstance(atencion, Atencion):
            raise TypeError("Solo puedes agregar objetos del tipo 'Atencion'.")
        self.atenciones.append(atencion)

    def listar_atenciones(self):
        # Muestra todas las atenciones registradas pos en la lista
        return self.atenciones

    def generar_resumen(self):
        # Genera un resumen con la cantidad de atenciones por servicio
        if not self.atenciones:
            raise ValueError("No hay atenciones registradas para generar resumen.")
        
        resumen = {}
        for atencion in self.atenciones:
            servicio = atencion.servicio
            resumen[servicio] = resumen.get(servicio, 0) + 1
        return resumen