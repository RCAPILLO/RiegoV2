import tkinter as tk
import threading
from Ia.redNeuronal import RedNeuronal
from Utilitarios.riego import Riego

class VentanaPrincipal(tk.Frame):
    def __init__(self, parent, controller, context):
        super().__init__(parent)
        self.controller = controller
        self.context=context
        self.controller.title("Sistema de Riego v.1")
        self.controller.geometry("700x700")

        # Obtener contexto compartido
        context = self.controller.context
        self.datos_cola = context.datos_cola
        self.datos_arduino = context.datos_arduino

        self.riego = context.riego
        self.red_neuronal = context.red_neuronal  # Puede ser None al inicio
        self.datos_recibidos = self.datos_arduino.datos_recibidos

        # Estado del sistema
        self.EstadoDelSistema = tk.StringVar()
        self.EstadoDelSistema.set("Estado del Sistema")

        tk.Label(self, text="Sistema de Riego", font=("Comic Sans MS", 24)).place(x=120, y=20)
        tk.Frame(self, bg="black", height=2, width=460).place(x=20, y=80)

        tk.Label(self, text="Estado del sistema", font=("Comic san MS", 18)).place(x=20, y=100)
        self.EstadoSistema = tk.Label(self, text="Inactivo", font=("Comic san MS", 18))
        self.EstadoSistema.place(x=320, y=100)

        tk.Label(self, text="Temperatura", font=("Comic san MS", 18)).place(x=20, y=140)
        self.Temperatura = tk.Label(self, text="...", font=("Comic san MS", 18))
        self.Temperatura.place(x=320, y=140)

        tk.Label(self, text="Humedad del Campo", font=("Comic san MS", 18)).place(x=20, y=180)
        self.HumedadCampo = tk.Label(self, text="...", font=("Comic san MS", 18))
        self.HumedadCampo.place(x=320, y=180)

        self.start = tk.Button(self, text="Iniciar Riego", width=12, height=1, font=("Comic san MS", 18),
                               command=self.iniciar_riego)
        self.start.place(x=40, y=280)

        self.salirprograma = tk.Button(self, text="Salir", width=12, height=1, font=("Comic san MS", 18),
                                       command=self.salir)
        self.salirprograma.place(x=290, y=280)

        self.conexion_label = tk.Label(self, text="Verificando conexión...", font=("Comic Sans MS", 12))
        self.conexion_label.place(x=20, y=400)

        self.verificar_conexion()
        self.actualizar_datos()

    def verificar_conexion(self):
        if self.datos_arduino.arduino and self.datos_arduino.arduino.is_open:
            self.conexion_label.config(text="Conectado a Arduino", fg="green")
        else:
            self.conexion_label.config(text="Error al conectar", fg="red")

    def iniciar_riego(self):
        if not self.datos_arduino.arduino or not self.datos_arduino.arduino.is_open:
            print("Reconectando Arduino...")
            self.datos_arduino.conexion_serial()

        # Asegurar que se ha creado la red neuronal (si aún no existe)
        if self.context.red_neuronal is None:
            self.context.iniciar_red_neuronal()

        red = self.context.red_neuronal
        if red:
            hilo_red = threading.Thread(target=red.iniciar_riego, daemon=True)
            hilo_red.start()
            print("IA activada: Controlando el riego...")
            self.controller.mostrar_pantalla("VentanaProgramarRiego")
        else:
            print("No se pudo iniciar la IA: Red neuronal no disponible.")


    def salir(self):
        try:
            self.detener_actualizacion()
            print("Cancelando y cerrando todo...")

            # Detener IA y comunicación si están activas
            if self.context.red_neuronal:
                self.context.red_neuronal.detener_riego()
            if self.context.datos_arduino:
                self.context.datos_arduino.enviar_datos("OFF")
                self.context.datos_arduino.detener_hilo()
                self.context.datos_arduino.desconectar()

            # Detener hilos si existen
            if hasattr(self, 'hilo_redneurona') and self.hilo_redneurona.is_alive():
                self.hilo_redneurona.join(timeout=2)
            if hasattr(self, 'hilo_comunicacion') and self.hilo_comunicacion.is_alive():
                self.hilo_comunicacion.join(timeout=2)

            # Llama al método seguro de cierre en la aplicación
            self.controller.cierre_seguro()

        except Exception as e:
            print(f"Error al salir: {e}")

    def actualizar_datos(self):
        try:
            datos_str = self.datos_recibidos.get()
            print(f"Datos leídos: {datos_str}")
            if datos_str and datos_str.strip():
                datos = datos_str.split(",")
                if len(datos) >= 3:
                    temperatura = float(datos[0])
                    humedadA = float(datos[1])
                    humedadB = float(datos[2])
                    self.Temperatura.config(text=f"{temperatura} °C")
                    self.HumedadCampo.config(text=f"{humedadB} %")
        except Exception as e:
            print(f"Error en actualización: {e}")
        if self.master.winfo_exists():
            self.after_id = self.master.after(1000, self.actualizar_datos)

    def detener_actualizacion(self):
        if hasattr(self, "after_id"):
            self.master.after_cancel(self.after_id)
