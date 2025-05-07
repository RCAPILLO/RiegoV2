from tkinter import *
from .mostrarGrafico import mostrarGrafico  # Importa la función para mostrar gráficos
from .grafica import mostrar_ventana_informes_linea

class VentanaInformes:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Riego informes")
        self.master.geometry("600x500")

        # Crear el marco
        self.miframe = Frame(self.master, width=600, height=500)
        self.miframe.pack()

        # Etiqueta de título
        Label(self.miframe, text="Sistema de Riego", font=("Comic Sans MS", 24)).place(x=20, y=20)
        Frame(self.miframe, bg="black", height=2, width=460).place(x=20, y=80)  # Línea decorativa

        # Botón para ver el informe
        verInforme=Button(self.miframe, text="Ver Informe", width=12, height=1, font=("Comic Sans MS", 14), bg="blue", fg="white",
               command=self.mostrar_grafico)
        verInforme.place(x=100,y=150)
        volver=Button(self.miframe, text="Volver", width=12, height=1, font=("Comic Sans MS", 14), bg="green", fg="white",
               command=self.volver_a_monitor)
        volver.place(x=100,y=200)
        VerEnLinea=Button(self.miframe, text="Informe Linea", width=12, height=1, font=("Comic Sans MS", 14), bg="red", fg="white",
               command=self.mostrar_enlinea)
        VerEnLinea.place(x=100,y=250)

    # Método para mostrar el gráfico
    def mostrar_grafico(self):
        mostrarGrafico()  # Llama a la función `mostrarGrafico`
    def volver_a_monitor(self):
        from .monitorRiego import mostrar_pantalla_monitor_riego
        self.master.destroy()  # Cierra la ventana actual
        mostrar_pantalla_monitor_riego()
    def mostrar_enlinea(self):
        self.master.destroy()  # Cierra la ventana actual
        mostrar_ventana_informes_linea()
        

def mostrar_pantalla_informes():
    root = Tk()
    app = VentanaInformes(root)
    root.mainloop()