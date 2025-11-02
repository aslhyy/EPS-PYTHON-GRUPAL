# modules/reportes.py
import os
import sys
from datetime import datetime, date
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# --- Utilidades internas ---
def _asegurar_dir(path):
    os.makedirs(path, exist_ok=True)

def abrir_imagen(path):
    """Abre la imagen con el visor predeterminado según el sistema operativo."""
    try:
        if os.name == "nt":  # Windows
            os.startfile(path)
        else:
            if sys.platform.startswith("darwin"):  # macOS
                os.system(f'open "{path}"')
            else:  # Linux y otros
                os.system(f'xdg-open "{path}"')
    except Exception:
        pass


# --- Función principal para generar gráficas ---
def generar_graficas(lista_atenciones, salida_dir=None, abrir=False):
    """
    Genera gráficos de barras y pastel sin depender de pandas.
    Recibe una lista de objetos Atencion o diccionarios equivalentes.
    Guarda las imágenes en tests/reports/.
    """
    if not lista_atenciones:
        raise ValueError("No hay atenciones para graficar.")

    if salida_dir is None:
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "reports")
    else:
        base = salida_dir
    _asegurar_dir(base)

    # --- Convertir lista de objetos a lista de diccionarios ---
    filas = []
    for a in lista_atenciones:
        if hasattr(a, "to_dict"):
            filas.append(a.to_dict())
        else:
            filas.append(dict(a))

    rutas = {}

    # -----------------------------
    # 1️⃣  Gráfico de barras por servicio
    # -----------------------------
    servicios = [fila["servicio"] for fila in filas if "servicio" in fila]
    conteo_servicio = Counter(servicios)

    if conteo_servicio:
        plt.figure(figsize=(8, 5))
        plt.bar(conteo_servicio.keys(), conteo_servicio.values())
        plt.title("Atenciones por servicio")
        plt.xlabel("Servicio")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        ruta_serv = os.path.join(base, "atenciones_por_servicio.png")
        plt.savefig(ruta_serv)
        plt.close()
        rutas["servicio"] = ruta_serv

    # -----------------------------
    # 2️⃣  Gráfico pastel por estado
    # -----------------------------
    estados = [fila.get("estado", "Desconocido") for fila in filas]
    conteo_estado = Counter(estados)

    if conteo_estado:
        plt.figure(figsize=(6, 6))
        plt.pie(conteo_estado.values(), labels=conteo_estado.keys(), autopct="%1.1f%%", startangle=90)
        plt.title("Distribución por estado del paciente")
        plt.tight_layout()

        ruta_estado = os.path.join(base, "estado_de_los_pacientes.png")
        plt.savefig(ruta_estado)
        plt.close()
        rutas["estado"] = ruta_estado

    # -----------------------------
    # 3️⃣  Gráfico de barras por mes
    # -----------------------------
    fechas = [fila.get("fecha") for fila in filas if fila.get("fecha")]
    conteo_mes = defaultdict(int)

    for f in fechas:
        try:
            fecha_dt = datetime.strptime(f, "%Y-%m-%d")
            clave_mes = fecha_dt.strftime("%Y-%m")
            conteo_mes[clave_mes] += 1
        except Exception:
            continue

    if conteo_mes:
        meses = sorted(conteo_mes.keys())
        valores = [conteo_mes[m] for m in meses]
        plt.figure(figsize=(8, 5))
        plt.bar(meses, valores)
        plt.title("Atenciones por mes")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        ruta_mes = os.path.join(base, "atenciones_por_mes.png")
        plt.savefig(ruta_mes)
        plt.close()
        rutas["mes"] = ruta_mes

    # Abrir las imágenes automáticamente si se desea
    if abrir:
        for p in rutas.values():
            abrir_imagen(p)

    return rutas


# --- Dashboard textual ---
def generar_dashboard_textual(lista_atenciones):
    """
    Genera un resumen textual con totales, atenciones hoy, y conteos por servicio/estado.
    Retorna un diccionario con los resultados.
    """
    if not lista_atenciones:
        return {"mensaje": "No hay atenciones registradas."}

    filas = []
    for a in lista_atenciones:
        if hasattr(a, "to_dict"):
            filas.append(a.to_dict())
        else:
            filas.append(dict(a))

    total = len(filas)
    hoy = date.today().isoformat()

    atenciones_hoy = sum(1 for f in filas if f.get("fecha") == hoy)
    servicios = [f.get("servicio") for f in filas if f.get("servicio")]
    estados = [f.get("estado") for f in filas if f.get("estado")]
    responsables = [f.get("responsable") for f in filas if f.get("responsable")]

    resumen = {
        "total_atenciones": total,
        "atenciones_hoy": atenciones_hoy,
        "por_servicio": dict(Counter(servicios)),
        "por_estado": dict(Counter(estados)),
        "por_responsable": dict(Counter(responsables)),
    }

    return resumen
