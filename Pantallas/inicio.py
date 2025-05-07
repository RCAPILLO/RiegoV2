import tkinter as tk
import mysql.connector
from tkinter import messagebox

class VentanaInicio(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Sistema de riego V.1")
        self.controller.geometry("500x500")
        self.controller.iconbitmap("Imagenes/LogoRiegoV1.ico")
        self.controller.resizable(0, 0)


        # Configuración del marco
        self.miframe = tk.Frame(self, width=500, height=400)
        self.miframe.pack()

        # Etiquetas de título 
        tk.Label(self, text="Sistema de Riego", font=("Comic Sans MS", 24), justify="center").place(x=120, y=20)
        # Línea horizontal decorativa
        tk.Frame(self.miframe, bg="black", height=2, width=460).place(x=20, y=80)
        # Etiquetas de casillas para iniciar sesion
        tk.Label(self.miframe, text="Usuario", font=("Comic Sans MS", 16)).place(x=20, y=120)
        tk.Label(self.miframe, text="Password", font=("Comic Sans MS", 16)).place(x=20, y=180)

        # Campos de entrada
        self.usuario = tk.Entry(self.miframe, font=("Arial", 14))
        self.usuario.place(x=140, y=120, width=200)
        self.pasword = tk.Entry(self.miframe, font=("Arial", 14), show="*")
        self.pasword.place(x=140, y=180, width=200)

        # Mensaje de error inicializado como un Label vacío
        self.mensaje_error = tk.Label(self.miframe, text="", font=("Arial", 12), fg="red")
        self.mensaje_error.place(x=140, y=220)  # Posiciona el mensaje de error en la pantalla

        # Botón de inicio
        iniciar = tk.Button(self.miframe, text="Iniciar Sesión",width=12,height=1, font=("Arial", 14), bg="lightblue", command=self.validar_usuario, cursor="hand2")
        iniciar.place(x=180, y=250)

        # Mensaje "Olvidé mi contraseña" (con evento de clic)
        mensaje_olvide = tk.Label(self.miframe, text="Olvidé mi contraseña", font=("Arial", 12), fg="blue", cursor="hand2")
        mensaje_olvide.place(x=170, y=300)
        # Asigna un evento de clic
        mensaje_olvide.bind("<Button-1>", self.recuperar_contraseña)

        # Botón de Cancelar
        cancelar =tk. Button(self.miframe, text="Cancelar", width=12, height=1, font=("Arial", 14), bg="lightblue", command=self.cancelar, cursor="hand2")
        cancelar.place(x=180, y=350)

    # Conexión a la base de datos MySQL
    def conectar_bd(self):
        return mysql.connector.connect(
            host="localhost",       # Servidor local
            user="root",            # Usuario de MySQL 
            password="",            # Contraseña de MySQL 
            database="riego"        # Nombre de la base de datos
        )

    # Función para validar usuario y contraseña desde la base de datos
    def validar_usuario(self):
        usuario_input = self.usuario.get()
        pasword_input = self.pasword.get()

        try:
            conn = self.conectar_bd()
            cursor = conn.cursor()

            # Consulta para verificar usuario y contraseña
            cursor.execute("SELECT * FROM usuario WHERE usuario = %s AND password = %s", 
                           (usuario_input, pasword_input))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                # Si las credenciales son correctas, abrir nueva ventana
                messagebox.showinfo("Inicio de Sesión", "Bienvenido al sistema de riego v1")
                #self.master.destroy()  # Cerrar la ventana actual
                self.controller.mostrar_pantalla("VentanaPrincipal")  # Llamar a la pantalla principal
            else:
                self.mensaje_error["text"] = "Usuario o contraseña incorrectos"
        except mysql.connector.Error as err:
            self.mensaje_error["text"] = f"Error de conexión: {err}"

    # Función para manejar el evento de "Olvidé mi contraseña"
    def recuperar_contraseña(self, event):
        # Mostrar un mensaje en consola por ahora (puedes agregar más lógica aquí)
        print("Redirigir a la página de recuperación de contraseña")

    def cancelar(self):
        print("Cancelando y cerrando todo...")

        
        # Cancelar actualizaciones por `after` si existen
        if hasattr(self, 'after_id'):
            self.master.after_cancel(self.after_id)

        # Cerrar aplicación completa
        self.controller.destroy()

    
    def ir_a_principal(self):
        self.controller.mostrar_pantalla("VentanaPrincipal")