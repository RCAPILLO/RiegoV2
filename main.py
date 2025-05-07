import tkinter as tk
from AppContext import AppContext
from Pantallas.inicio import VentanaInicio
from Pantallas.principal import VentanaPrincipal
from Pantallas.programarRiego import VentanaProgramarRiego
from Pantallas.monitorRiego import VentanaMonitorRiego

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Riego Inteligente")
        self.geometry("800x600")
        self.iconbitmap("Imagenes/LogoRiegoV1.ico")
        self.resizable(0, 0)

        contenedor = tk.Frame(self)
        contenedor.pack(fill="both", expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)
        self.context = AppContext()

        self.pantallas = {}

        # Solo se crea la pantalla de inicio por ahora
        pantalla_inicio = VentanaInicio(contenedor, self)
        self.pantallas["VentanaInicio"] = pantalla_inicio
        pantalla_inicio.grid(row=0, column=0, sticky="nsew")

        self.contenedor = contenedor  # Guarda contenedor para futuras pantallas

        self.mostrar_pantalla("VentanaInicio")

    def cargar_pantalla_si_no_existe(self, nombre):
        if nombre not in self.pantallas:
            if nombre == "VentanaPrincipal":
                pantalla = VentanaPrincipal(self.contenedor, self,self.context)
            elif nombre == "VentanaProgramarRiego":
                pantalla = VentanaProgramarRiego(self.contenedor, self)
            elif nombre == "VentanaMonitorRiego":
                pantalla = VentanaMonitorRiego(self.contenedor, self, self.context)
            else:
                return
            self.pantallas[nombre] = pantalla
            pantalla.grid(row=0, column=0, sticky="nsew")


    def mostrar_pantalla(self, nombre_pantalla):
        self.cargar_pantalla_si_no_existe(nombre_pantalla)
        pantalla = self.pantallas[nombre_pantalla]
        pantalla.tkraise()


def main():
    app = Aplicacion()
    app.mainloop()

if __name__ == "__main__":
    main()
