from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
from datetime import datetime

def mostrarGrafico(frame):
    # Limpiar el frame antes de dibujar
    for widget in frame.winfo_children():
        widget.destroy()

    # Conexión a la base de datos MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_riego"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT hora_inicio, consumo_agua, humedad_promedio FROM registro_riego ORDER BY hora_inicio")
    datos = cursor.fetchall()
    conn.close()

    if not datos:
        return

    tiempos = [row[0] for row in datos]
    consumos = [float(row[1]) for row in datos]
    humedades = [float(row[2]) for row in datos]

    # Crear figura
    fig = Figure(figsize=(6, 5), dpi=100)
    ax1 = fig.add_subplot(211)
    ax1.plot(tiempos, consumos, marker='o', color='blue')
    ax1.set_title("Consumo de Agua vs Tiempo")
    ax1.set_ylabel("Litros")

    ax2 = fig.add_subplot(212)
    ax2.plot(tiempos, humedades, marker='x', color='green')
    ax2.set_title("Humedad Promedio vs Tiempo")
    ax2.set_xlabel("Fecha y hora")
    ax2.set_ylabel("% Humedad")
    for label in ax1.get_xticklabels():
        label.set_rotation(30)
        label.set_ha('right')

    for label in ax2.get_xticklabels():
        label.set_rotation(30)
        label.set_ha('right')

    fig.tight_layout()  # Ajusta automáticamente los márgenes


    # Mostrar en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
