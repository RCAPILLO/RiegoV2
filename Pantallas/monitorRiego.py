import tkinter as tk
import queue
import tkinter.messagebox as messagebox
import mysql.connector
class VentanaMonitorRiego(tk.Frame):
    def __init__(self, parent, controller,context):
        super().__init__(parent)
        self.controller = controller
        self.context=context
        self.datos_arduino = context.datos_arduino
        self.datos_recibidos = context.datos_cola
        self.red_neuronal = context.red_neuronal
        self.after_id = None  # Para controlar el .after
        self.modo_manual_activo = False 
        self.controller.title("Monitor de Riego")
        self.controller.geometry("700x700")
        
        self.miframe = tk.Frame(self, width=600, height=450)
        self.miframe.pack()

        # Etiquetas
        tk.Label(self, text="Sistema de Riego", font=("Comic Sans MS", 24)).place(x=120, y=20)
        tk.Frame(self, bg="black", height=2, width=460).place(x=20, y=80)
        tk.Label(self, text="Monitor de Riego", font=("Comic Sans MS", 18)).place(x=80, y=100)

        tk.Label(self, text="Estado del Sistema", font=("Comic Sans MS", 16)).place(x=20, y=160)
        tk.Label(self, text="Sensor Humedad zona A", font=("Comic Sans MS", 16)).place(x=20, y=200)
        tk.Label(self, text="Sensor Humedad zona B", font=("Comic Sans MS", 16)).place(x=20, y=240)
        tk.Label(self, text="Temperatura ambiente", font=("Comic Sans MS", 16)).place(x=20, y=280)

        self.estado_label = tk.Label(self, text="Activo", font=("Comic Sans MS", 16))
        self.estado_label.place(x=440, y=160)

        self.humedad_a_label = tk.Label(self, text="...", font=("Comic Sans MS", 16))
        self.humedad_a_label.place(x=360, y=200)

        self.humedad_b_label = tk.Label(self, text="...", font=("Comic Sans MS", 16))
        self.humedad_b_label.place(x=360, y=240)

        self.temperatura_label = tk.Label(self, text="...", font=("Comic Sans MS", 16))
        self.temperatura_label.place(x=360, y=280)
        
        self.label_modo_manual = tk.Label(self, text="Modo Manual Activado", font=("Comic Sans MS", 12), fg="blue")
        self.boton_cerrar_valvula = tk.Button(self, text="Cerrar Válvula", font=("Comic Sans MS", 12), bg="gray",
                                      command=self.cerrar_valvula_manual)
        


        self.boton_modo_manual=tk.Button(self, text="Modo Manual", font=("Comic Sans MS", 16), width=10, bg="blue",
               command=self.modo_manual)
        self.boton_modo_manual.place(x=20, y=340)
        self.boton_stop=tk.Button(self.miframe, text="Stop", font=("Comic Sans MS", 16), width=10, bg="red",
               command=self.detener)
        self.boton_stop.place(x=140, y=340)
        self.boton_alarmas=tk.Button(self.miframe, text="Alarmas", font=("Comic Sans MS", 16), width=10, bg="orange",
               command=self.alarmas)
        self.boton_alarmas.place(x=300, y=340)
        self.boton_informes=tk.Button(self.miframe, text="Informes", font=("Comic Sans MS", 16), width=10, bg="green",
               command=self.abrir_informes)
        self.boton_informes.place(x=480, y=340)

        self.conexion_label =tk.Label(self.miframe, text="Verificando conexión...", font=("Comic Sans MS", 12))
        self.conexion_label.place(x=20, y=400)

        # Validar estado de conexión
        if self.datos_arduino.arduino and self.datos_arduino.arduino.is_open:
            self.conexion_label.config(text="Conectado a Arduino", fg="green")
        else:
            self.conexion_label.config(text="Error al conectar", fg="red")

        # Iniciar actualización automática
        self.actualizar_datos()

    def modo_manual(self):
        if not self.modo_manual_activo:
        # Mostrar aviso visual
            self.boton_cerrar_valvula.place(x=250, y=400)
            self.label_modo_manual.place(x=250, y=450)
            self.boton_modo_manual.config(state=tk.DISABLED)
            self.boton_alarmas.config(state=tk.DISABLED)
            self.boton_informes.config(state=tk.DISABLED)
            self.boton_stop.config(state=tk.DISABLED)
            print("Activando Modo Manual")
            """if self.red_neuronal:
                self.red_neuronal.detener_riego()

            if self.datos_arduino.arduino and self.datos_arduino.arduino.is_open:
                self.datos_arduino.enviar_datos("ON")
                self.estado_label.config(text="Manual ON", fg="blue")
                self.modo_manual_activo = True
            else:
                print("Conexión a Arduino no disponible.")
        else:
            print("Desactivando Modo Manual")
            self.cerrar_valvula_manual()"""

    def detener(self):
        print("Cancelando y cerrando todo...")
        self.controller.mostrar_pantalla("VentanaPrincipal")



    def alarmas(self):
        print("Mostrando alarmas")

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='sistema_riego'
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT humedad_promedio, duracion 
                FROM registro_riego 
                ORDER BY hora_inicio DESC 
                LIMIT 1
            """)
            resultado = cursor.fetchone()
            conn.close()

            if resultado is None:
                messagebox.showinfo("Sin registros", "No se encontraron datos en la base de datos.")
                return

            humedad_actual = float(resultado[0])
            tiempo_riego_minutos = float(resultado[1]/3600)

            mensajes = []

            if humedad_actual > 85:
                mensajes.append(f"Humedad alta detectada: {humedad_actual:.1f}%")

            if tiempo_riego_minutos > 40:
                mensajes.append(f"Riego apagado por exceder los 40 minutos ({tiempo_riego_minutos:.1f} min)")

            if mensajes:
                mensaje_final = "\n".join(mensajes)
                messagebox.showwarning("Alarma de Riego", mensaje_final)
            else:
                messagebox.showinfo("Estado del Sistema", "No se detectaron alarmas.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo acceder a la base de datos:\n{err}")


    def abrir_informes(self):
        self.controller.mostrar_pantalla("VentanaInformes")

    def actualizar_datos(self):
        try:
            datos_str = self.datos_recibidos.get_nowait()
            print(f"Datos leídos: {datos_str}")
            if datos_str and datos_str.strip():
                datos = datos_str.split(",")
                if len(datos) >= 3:
                    temperatura = float(datos[0])
                    humedadA = float(datos[1])
                    humedadB = float(datos[2])

                    self.temperatura_label.config(text=f"{temperatura} °C")
                    self.humedad_a_label.config(text=f"{humedadA} %")
                    self.humedad_b_label.config(text=f"{humedadB} %")

                    if humedadA > 35:
                        self.estado_label.config(text="Activo", fg="green")
                    else:
                        self.estado_label.config(text="Bajo", fg="red")
                else:
                    print("Formato de datos incompleto")
            else:
                print("No hay datos disponibles")
        except queue.Empty:
            print("Cola vacía, esperando datos...")
        except Exception as e:
            print(f"Error inesperado: {e}")

        self.after_id = self.after(1000, self.actualizar_datos)


    def cerrar_valvula_manual(self):
        if self.datos_arduino.arduino and self.datos_arduino.arduino.is_open:
            self.datos_arduino.enviar_datos("OFF")
            self.estado_label.config(text="Manual OFF", fg="gray")
            print("Válvula cerrada manualmente")
        
        # Ocultar elementos visuales
        self.label_modo_manual.place_forget()
        self.boton_cerrar_valvula.place_forget()
        self.boton_modo_manual.config(state=tk.NORMAL)
        self.boton_alarmas.config(state=tk.NORMAL)
        self.boton_informes.config(state=tk.NORMAL)
        self.boton_stop.config(state=tk.NORMAL)
        self.modo_manual_activo = False
