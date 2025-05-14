
import tkinter as tk
from .mostrarGrafico import mostrarGrafico  # Importa la función para mostrar gráficos
from .grafica import mostrar_ventana_informes_linea

class VentanaInformes(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.parent = parent
        self.controller=controller
        self.controller.title("Sistema de Riego informes")
        self.controller.geometry("700x700")
        self.miframe = tk.Frame(self, width=600, height=600)
        self.miframe.pack()

        self.frame_grafico = tk.Frame(self.miframe, bg="white", width=460, height=300)
        self.frame_grafico.place(x=10, y=110)


        # Etiqueta de título
        tk.Label(self.miframe, text="Sistema de Riego", font=("Comic Sans MS", 24)).place(x=20, y=10)
        tk.Frame(self.miframe, bg="black", height=2, width=460).place(x=20, y=55)  # Línea decorativa

        # Botón para ver el informe
        verInforme=tk.Button(self.miframe, text="Ver Informe", width=12, height=1, font=("Comic Sans MS", 14), bg="blue", fg="white",
               command=self.mostrar_grafico)
        verInforme.place(x=20,y=60)
        VerEnLinea=tk.Button(self.miframe, text="Informe Linea", width=12, height=1, font=("Comic Sans MS", 14), bg="red", fg="white",
               command=self.mostrar_enlinea)
        VerEnLinea.place(x=200,y=60)
        volver=tk.Button(self.miframe, text="Volver", width=12, height=1, font=("Comic Sans MS", 14), bg="green", fg="white",
               command=self.volver_a_monitor)
        volver.place(x=360,y=60)

    # Método para mostrar el gráfico
    def mostrar_grafico(self):
        from .mostrarGrafico import mostrarGrafico
        mostrarGrafico(self.frame_grafico)
        
    def volver_a_monitor(self):
        self.controller.mostrar_pantalla("VentanaMonitorRiego")
    def mostrar_enlinea(self):
        self.controller.mostrar_pantalla("VentanaMonitorRiego")
