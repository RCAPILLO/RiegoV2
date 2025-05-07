from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para mostrar el gráfico de historial de riego
def mostrarGrafico():
    # Crear nueva ventana para el gráfico
    grafico_ventana=Toplevel()
    grafico_ventana.title("Historial de Riego")
    grafico_ventana.geometry("700x500")
    
    # Datos simulados (puedes reemplazar con datos reales de la base de datos)
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    riego = [30, 45, 25, 50, 40, 35, 20]  # Valores en litros o minutos de riego
    
    # Crear figura de Matplotlib
    fig = Figure(figsize=(7, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(dias, riego, marker='o', color='b', label="Historial de Riego")
    plot.set_title("Historial de Riego Semanal")
    plot.set_xlabel("Días de la semana")
    plot.set_ylabel("Cantidad de Riego (litros)")
    plot.grid()
    plot.legend()
    
    # Insertar gráfico en la ventana
    canvas = FigureCanvasTkAgg(fig, master=grafico_ventana)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()