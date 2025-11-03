# 🏥 SISTEMA DE REGISTRO DE ATENCIÓN EPS

**Categoría:** Procesos Misional <br>
**Versión de Python utilizada:** Python 3.13.9

---

## 1. Problema o necesidad identificada

En las Entidades Prestadoras de Salud (EPS), el registro manual de atenciones médicas genera errores de transcripción, pérdida de información y demoras en la generación de reportes.
Este problema afecta directamente la trazabilidad de los servicios prestados y la eficiencia operativa del personal administrativo.

Por tanto, surge la necesidad de implementar un **sistema automatizado que permita registrar, listar y analizar las atenciones de los pacientes** de forma rápida, estructurada y segura, garantizando la persistencia de los datos y la trazabilidad de las gestiones realizadas.

---

## 2. Solución propuesta

El proyecto **“Sistema de Registro de Atención EPS”** consiste en una aplicación de consola desarrollada en **Python**, que permite:

* Registrar atenciones de pacientes (nombre, servicio, responsable, fecha, resultado de la atención y estado del paciente).
* Almacenar la información en archivos **CSV** de manera persistente.
* Generar reportes estadísticos y gráficos (por servicio, fecha(mes) o cantidad de atenciones).
* Facilitar la consulta, validación y exportación de datos desde una interfaz textual clara.

### 🧱 Arquitectura general

El sistema se organiza bajo una estructura modular:

```
EPS/
│
├── src/
│   ├── main.py                # Menú principal y flujo del programa
│   ├── modules/
│   │   ├── models.py          # Clases Atencion y GestorAtenciones
│   │   ├── storage.py         # Lectura y escritura de archivos CSV
│   │   ├── reports.py         # Generación de reportes y gráficas
│   │   ├── utils.py           # Validaciones, limpieza de pantalla, fechas
│   └── data/
│       └── atenciones.csv     # Archivo base con registros
│
├── tests/                     # Pruebas y archivos de ejemplo
├── requirements.txt
└── README.md
```

---

## 3. Manual de usuario

### ✅ Requisitos previos

* Tener instalado **Python 3.13.9** o superior.
* (Opcional) Crear y activar un entorno virtual:

  ```bash
  python -m venv .venv
  source .venv/Scripts/activate   
  ```

### ⚙️ Instalación

**1.** Clonar el repositorio desde GitHub:

   ```bash
   git clone https://github.com/<usuario>/EPS.git
   cd EPS
   ```

**2.** Instalar dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

### ▶️ Ejecución

Para iniciar el sistema:

```bash
python src/main.py
```

El menú principal mostrará las opciones para registrar atención, ver atenciones y generar reportes de atenciones.

### 💬 Ejemplo de uso

* Registrar una atención ingresando los datos solicitados en consola.
* Generar un reporte de servicios para obtener un resumen gráfico de atenciones por tipo.

### 📤 Salidas esperadas

* Archivo `atenciones.csv` actualizado con nuevos registros.
* Archivo `atenciones_por_servicio.csv` con resumen estadístico.
* Gráfica PNG generada en la carpeta `/reports` con la distribución visual de servicios.

---

## 4. Evidencias del funcionamiento

* Ejecución en consola de `main.py` mostrando menú principal y registro de datos.

  <img width="1592" height="308" alt="image" src="https://github.com/user-attachments/assets/e52b65db-9ec9-47b8-96a9-ed55daaa3159" />

* Visualización de `atenciones.csv` con estructura validada y registros correctamente formateados.

  <img width="1223" height="405" alt="image" src="https://github.com/user-attachments/assets/04e4a978-f95f-41e7-8811-5002e3371bd2" />

* Ejemplo de gráfico generado por `matplotlib` mostrando comparativa de servicios.

  <img width="290" height="240" alt="image" src="https://github.com/user-attachments/assets/c178300b-1a5c-487f-a7e8-073594548920" />
  <img width="290" height="240" alt="image" src="https://github.com/user-attachments/assets/35263bc8-6283-4d92-9c08-ddefb0b771ed" />
  <img width="290" height="240" alt="image" src="https://github.com/user-attachments/assets/e880e7a8-86a5-46ed-a2e5-a6ae64316c75" />


### 📂 Descripción del archivo CSV

**Nombre:** `atenciones.csv`
<br>
**Columnas:** `nombre`, `servicio`, `responsable`, `fecha`, `resultado`, `estado`.
Cada registro corresponde a una atención individual almacenada mediante el módulo `storage.py`.

---

## 5. Temas de Python aplicados

El proyecto integra diversos conceptos vistos en clase, entre ellos:

* **Estructuras de datos:** listas, diccionarios y tuplas.
* **Programación orientada a objetos (POO):** clases, métodos y encapsulamiento.
* **Manejo de archivos:** lectura y escritura con `csv`.
* **Excepciones y validaciones:** control de errores de entrada y fechas.
* **Funciones modulares:** reutilización de código por módulos.
* **Bibliotecas externas:** uso de `matplotlib` para generar reportes gráficos.
* **Trabajo colaborativo con Git y GitHub.**

---

## 6. Trabajo colaborativo

### 🔗 Repositorio y commits

Enlace al repositorio:
https://github.com/aslhyy/EPS-PYTHON-GRUPAL/commits/main/ 

### 👩‍💻 Aportes de los integrantes

| Integrante                      | Aporte principal                                                                                                                       |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Aslhy Casteblanco**           | Integró las validaciones y el flujo principal del programa (`main.py`, `utils.py`), resolución de conflictos y mantenimiento de ramas. <br><br> Generación del archivo README.md y creación de ambiente virtual para `curses`. |
| **Juan Riveros** | Depuración de errores, validación de datos, actualización de funciones de almacenamiento y finalización del producto (`storage.py`). <br><br> Creación de reportes estadísticos con `matplotlib`, manejo de CSV resumen y apoyo en pruebas finales (`reports.py`).        |
| **Hugo Mancera**                   | Implementación de clases `Atencion` y `GestorAtenciones`, estructura base del sistema y manejo de errores en clases (`models.py`).     |        

---

## 7. Límites y mejoras futuras

* Migrar de consola a interfaz gráfica con **Tkinter** o **Flask**.
* Incorporar autenticación de usuarios y control de roles.
* Implementar almacenamiento en **SQLite o PostgreSQL**.
* Añadir pruebas unitarias automatizadas con **pytest**.

---

## 🧩 Conclusión

El **Sistema de Registro de Atención EPS** representa una solución misional efectiva para optimizar el registro y seguimiento de servicios médicos dentro de una entidad de salud.
Permite la trazabilidad de los datos, mejora la eficiencia operativa y aplica de manera práctica los principios de la programación estructurada y orientada a objetos en Python.
