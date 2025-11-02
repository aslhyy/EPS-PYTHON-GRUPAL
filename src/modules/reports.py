# modules/reportes.py
import os
import sys
import csv
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


def _guardar_csv(ruta, encabezados, datos):
    """Guarda un archivo CSV simple sin usar pandas."""
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(encabezados)
        for fila in datos:
            writer.writerow(fila)


# --- Función principal para generar gráficas y CSV ---
def generar_graficas(lista_atenciones, salida_dir=None, abrir=False):
    """
    Genera gráficos de barras y pastel sin depender de pandas.
    Además exporta las estadísticas a CSV (por servicio, estado, mes y dashboard),
    guardándolos en carpetas separadas (img/ y csv/).
    """
    if not lista_atenciones:
        raise ValueError("No hay atenciones para graficar.")

    # Carpeta base donde se guardan los reportes
    if salida_dir is None:
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "reports")
    else:
        base = salida_dir

    # Subcarpetas separadas
    dir_img = os.path.join(base, "img")
    dir_csv = os.path.join(base, "csv")

    _asegurar_dir(dir_img)
    _asegurar_dir(dir_csv)

    # --- Convertir lista de objetos a lista de diccionarios ---
    filas = []
    for a in lista_atenciones:
        if hasattr(a, "to_dict"):
            filas.append(a.to_dict())
        else:
            filas.append(dict(a))

    rutas = {}

    # -----------------------------
    # 1️⃣  Gráfico y CSV por servicio
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

        ruta_serv_img = os.path.join(dir_img, "atenciones_por_servicio.png")
        plt.savefig(ruta_serv_img)
        plt.close()
        rutas["servicio_img"] = ruta_serv_img

        # CSV correspondiente
        ruta_serv_csv = os.path.join(dir_csv, "atenciones_por_servicio.csv")
        _guardar_csv(ruta_serv_csv, ["Servicio", "Cantidad"], conteo_servicio.items())
        rutas["servicio_csv"] = ruta_serv_csv

    # -----------------------------
    # 2️⃣  Gráfico y CSV por estado
    # -----------------------------
    estados = [fila.get("estado", "Desconocido") for fila in filas]
    conteo_estado = Counter(estados)

    if conteo_estado:
        plt.figure(figsize=(6, 6))
        plt.pie(conteo_estado.values(), labels=conteo_estado.keys(), autopct="%1.1f%%", startangle=90)
        plt.title("Distribución por estado del paciente")
        plt.tight_layout()

        ruta_estado_img = os.path.join(dir_img, "estado_de_los_pacientes.png")
        plt.savefig(ruta_estado_img)
        plt.close()
        rutas["estado_img"] = ruta_estado_img

        # CSV correspondiente
        ruta_estado_csv = os.path.join(dir_csv, "estado_de_los_pacientes.csv")
        _guardar_csv(ruta_estado_csv, ["Estado", "Cantidad"], conteo_estado.items())
        rutas["estado_csv"] = ruta_estado_csv

    # -----------------------------
    # 3️⃣  Gráfico y CSV por mes
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

        ruta_mes_img = os.path.join(dir_img, "atenciones_por_mes.png")
        plt.savefig(ruta_mes_img)
        plt.close()
        rutas["mes_img"] = ruta_mes_img

        # CSV correspondiente
        ruta_mes_csv = os.path.join(dir_csv, "atenciones_por_mes.csv")
        _guardar_csv(ruta_mes_csv, ["Mes", "Cantidad"], conteo_mes.items())
        rutas["mes_csv"] = ruta_mes_csv

    # -----------------------------
    # 4️⃣  Dashboard textual en CSV
    # -----------------------------
    dashboard = generar_dashboard_textual(lista_atenciones)

    ruta_dash_csv = os.path.join(dir_csv, "dashboard_resumen.csv")
    with open(ruta_dash_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Categoría", "Valor"])
        writer.writerow(["Total atenciones", dashboard["total_atenciones"]])
        writer.writerow([])

        writer.writerow(["--- Por servicio ---", ""])
        for s, c in dashboard["por_servicio"].items():
            writer.writerow([s, c])

        writer.writerow([])
        writer.writerow(["--- Por estado ---", ""])
        for e, c in dashboard["por_estado"].items():
            writer.writerow([e, c])

        writer.writerow([])
        writer.writerow(["--- Por responsable ---", ""])
        for r, c in dashboard["por_responsable"].items():
            writer.writerow([r, c])

    rutas["dashboard_csv"] = ruta_dash_csv

    # Abrir imágenes si se desea
    if abrir:
        for p in rutas.values():
            if p.endswith(".png"):
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
