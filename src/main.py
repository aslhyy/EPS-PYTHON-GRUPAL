import curses

from modules.models import Atencion, GestorAtenciones
from modules.storage import guardar_en_csv, leer_atenciones
from modules.utils import validar_fecha, limpiar_pantalla

def mostrar_menu(stdscr, opciones):
    """
    Muestra el menú principal del sistema.
    """
    curses.curs_set(0)  # Oculta el cursor
    seleccion = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== SISTEMA DE REGISTRO DE ATENCIÓN EPS ===\n", curses.A_BOLD)

        for i, opcion in enumerate(opciones):
            if i == seleccion:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {opcion}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {opcion}\n")

        tecla = stdscr.getch()

        if tecla == curses.KEY_UP and seleccion > 0:
            seleccion -= 1
        elif tecla == curses.KEY_DOWN and seleccion < len(opciones) - 1:
            seleccion += 1
        elif tecla == ord("\n"):
            return seleccion  # Devuelve el índice seleccionado

def registrar_atencion(gestor):
    """
    Permite ingresar los datos de una nueva atención.
    Valida la fecha y maneja excepciones por entradas vacías.
    """
    try:
        print("\n--- Registrar Nueva Atención ---")
        nombre = input("Nombre del beneficiario: ").strip()
        servicio = input("Servicio solicitado: ").strip()
        responsable = input("Responsable: ").strip()
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        resultado = input("Resultado de la atención: ").strip()

        # Validación básica
        if not all([nombre, servicio, responsable, fecha, resultado]):
            print("Todos los campos son obligatorios.")
            return

        # Validar formato de fecha
        if not validar_fecha(fecha):
            return

        # === NUEVO BLOQUE: Selección del estado del paciente ===
        opciones_estado = ["Mala", "Regular", "Aceptable", "Buena", "Excelente"]
        print("\n--- Seleccione el estado del paciente ---")
        for i, estado in enumerate(opciones_estado, 1):
            print(f"{i}. {estado}")

        while True:
            try:
                seleccion = int(input("Ingrese el número correspondiente al estado: "))
                if 1 <= seleccion <= len(opciones_estado):
                    estado_paciente = opciones_estado[seleccion - 1]
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
            except ValueError:
                print("Ingrese un número válido.")

        # Crear objeto y agregar al gestor
        nueva_atencion = Atencion(nombre, servicio, responsable, fecha, resultado, estado_paciente)
        gestor.agregar_atencion(nueva_atencion)
        print(f"Atención registrada exitosamente con estado: {estado_paciente}.")

    except Exception as e:
        print(f"Error al registrar la atención: {e}")


def mostrar_atenciones(gestor):
    """
    Muestra todas las atenciones registradas en memoria.
    """
    atenciones = gestor.listar_atenciones()
    if not atenciones:
        print("\nNo hay atenciones registradas aún.")
        return

    print("\n--- LISTADO DE ATENCIONES ---")
    for i, atencion in enumerate(atenciones, start=1):
        print(f"{i}. {atencion.nombre} | {atencion.servicio} | "
              f"{atencion.responsable} | {atencion.fecha} | {atencion.resultado} | {atencion.estado}")

def generar_reporte_csv(gestor):
    """
    Genera el archivo CSV con todas las atenciones registradas.
    """
    try:
        guardar_en_csv(gestor.listar_atenciones())
        print("Reporte CSV generado exitosamente en data/atenciones.csv")
    except Exception as e:
        print(f"Error al generar el reporte: {e}")

def main(stdscr):
    """
    Menú principal con flechas y enter.
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    opciones = ["Registrar atención", "Ver atenciones", "Generar reporte CSV", "Salir"]
    gestor = GestorAtenciones()

    datos = leer_atenciones()
    for d in datos:
        gestor.agregar_atencion(Atencion(**d))

    while True:
        seleccion = mostrar_menu(stdscr, opciones)

        if seleccion == 0:
            curses.endwin()
            registrar_atencion(gestor)
            input("\nPresione Enter para continuar...")
        elif seleccion == 1:
            curses.endwin()
            print("\n--- LISTADO DE ATENCIONES ---")
            for i, a in enumerate(gestor.listar_atenciones(), start=1):
                print(f"{i}. {a.nombre} | {a.servicio} | {a.responsable} | {a.fecha} | {a.resultado} | {a.estado}")
            input("\nPresione Enter para continuar...")
        elif seleccion == 2:
            curses.endwin()
            guardar_en_csv(gestor.listar_atenciones())
            print("Reporte CSV generado exitosamente.")
            input("\nPresione Enter para continuar...")
        elif seleccion == 3:
            curses.endwin()
            print("\nGracias por usar el sistema. ¡Hasta luego!")
            break
        curses.doupdate()

# Punto de entrada
if __name__ == "__main__":
    import curses
    curses.wrapper(main)