from tkinter import  Tk, Frame, Button,Label,PhotoImage
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from Comunicacion.comunicacion import Comunicacion
import collections

class Grafica(Frame):
    def __init__(self,master,*args):
        super().__init__(master,*args)
        self.datos_arduino =Comunicacion()
        self.datos_recibidos = self.datos_arduino.datos_recibidos  # Usar la misma variable
        self.actualizar_puertos()
        self.muestra=100
        self.datos=0.0
        self.fig,ax =plt.subplots(facecolor="#000000",dpi=100,figsize=(4,2))

        plt.title("Grafica de prueba ",color="green",size=12,family="Arial")
        ax.tick_params(direction='out',length=6,width=2,color="white",grid_color="r",grid_alpha=0.5)
        self.line,=ax.plot([],[],color='red',marker='o',linewidth=2,markersize=2,markeredgecolor='r')
        self.line2,=ax.plot([],[],color='blue',marker='o',linewidth=2,markersize=2,markeredgecolor='b')
        self.line3,=ax.plot([],[],color='green',marker='o',linewidth=2,markersize=2,markeredgecolor='g')

        ax.set_xlim([0, self.muestra])
        ax.set_ylim([0, 100])  # Ajusta este límite según los valores esperados
        ax.set_yticks(range(0, 101, 10)) 
        ax.tick_params(axis='y', colors='white') 

        ax.set_facecolor('#6E6D7000')
        ax.spines['bottom'].set_color('blue')
        ax.spines['left'].set_color('blue')
        ax.spines['top'].set_color('blue')
        ax.spines['right'].set_color('blue')
        self.datos_señal_uno=collections.deque([0]*self.muestra,maxlen=self.muestra)
        self.datos_señal_dos=collections.deque([0]*self.muestra,maxlen=self.muestra)
        self.datos_señal_tres=collections.deque([0]*self.muestra,maxlen=self.muestra)
        self.widgets()
    
    def animate(self, i):
        dato = self.datos_recibidos.get().split(",")  # Separa los valores

        if len(dato) < 3:  # Asegura que haya al menos 3 valores antes de continuar
            print("Error: Datos incompletos recibidos:", dato)
            return

        try:
            dato1 = float(dato[0])  # Temperatura
            dato2 = float(dato[1])  # Humedad Ambiente
            dato3 = float(dato[2])  # Humedad Suelo
            print('La lectura')
            print(f"Temperatura: {dato1} C, Humedad: {dato2} %, Humedad Suelo: {dato3} %")
       
            self.datos_señal_uno.append(dato1)
            self.datos_señal_dos.append(dato2)
            self.datos_señal_tres.append(dato3)

            self.line.set_data(range(self.muestra),self.datos_señal_uno)
            self.line2.set_data(range(self.muestra),self.datos_señal_dos)
            self.line3.set_data(range(self.muestra),self.datos_señal_tres)
            
            # 🔹 Ajustar límites de la gráfica automáticamente
            ax = self.fig.axes[0]
            ax.relim()  # Recalcular límites
            ax.autoscale_view()  # Ajustar vista automáticamente

            # 🔹 Redibujar la figura
            self.fig.canvas.draw_idle()

        except ValueError:
            print("Error: No se pudieron convertir los datos a número:", dato)

    def iniciar(self):
        self.ani=animacion.FuncAnimation(self.fig,self.animate,interval=100,blit=False,save_count=100)
        self.bt_graficar.config(state="disabled")
        self.bt_pausar.config(state="normal")
        self.canvas.draw()
    def pausar(self):
        self.ani.event_source.stop()
        self.bt_reanudar.config(state="normal")
    def reanudar(self):
        self.ani.event_source.start()
        self.bt_reanudar.config(state="disabled")
    def widgets(self):
        frame=Frame(self.master,bg="gray50",bd=2)
        frame.grid(column=0,columnspan=2,row=0,sticky='nsew')
        frame_uno=Frame(self.master,bg='black')
        frame_uno.grid(column=2,row=0,sticky='nsew')
        frame_cuatro=Frame(self.master,bg='black')
        frame_cuatro.grid(column=0,row=1,sticky='nsew')
        frame_dos=Frame(self.master,bg='black')
        frame_dos.grid(column=1,row=1,sticky='nsew')
        frame_tres=Frame(self.master,bg='black')
        frame_tres.grid(column=2,row=1,sticky='nsew')
        
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(1,weight=1)
        self.master.columnconfigure(2,weight=1)
        self.master.rowconfigure(0,weight=5)
        self.master.rowconfigure(1,weight=1)
        self.master.rowconfigure(2, weight=1)

        self.canvas=FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(padx=0,pady=0,expand=True,fill='both')

        self.bt_graficar=Button(frame_cuatro,text="Iniciar",font=('Arial',12,'bold'),width=12,bg='purple4',fg='white',command=self.iniciar)
        self.bt_graficar.pack(pady=5,expand=1)
        self.bt_pausar=Button(frame_cuatro,state='disabled',text="Pausar",font=('Arial',12,'bold'),width=12,bg='purple4',fg='white',command=self.pausar)
        self.bt_pausar.pack(pady=5,expand=1)
        self.bt_reanudar=Button(frame_cuatro,state='disabled',text="Reanudar",font=('Arial',12,'bold'),width=12,bg='purple4',fg='white',command=self.reanudar)
        self.bt_reanudar.pack(pady=5,expand=1)
        
        self.logo = PhotoImage(file=".\Imagenes\Agro1.png").subsample(3, 3) 

        Label(frame_dos,text="Lectura de sensores en linea",font=("Comic san MS",12,'bold'),bg='black',fg='white').pack(padx=5,pady=5,expand=1)
        Label(frame_dos,text="Temperatura ambiente:  Rojo",font=("Comic san MS",10,'bold'),bg='black',fg='white',anchor="w", justify="left").pack(padx=5,pady=5,expand=1)
        Label(frame_dos,text="Humedad relativa del ambiente: Azul",font=("Comic san MS",10,'bold'),bg='black',fg='white',anchor="w", justify="left").pack(padx=5,pady=5,expand=1)
        Label(frame_dos,text="Humedad del suelo: Verde",font=("Comic san MS",10,'bold'),bg='black',fg='white',anchor="w", justify="left").pack(padx=5,pady=5,expand=1)
        #style=ttk.Style() 
        #style.configure("Horizontal.TScale",background='black')
        #self.slider_uno=ttk.Scale(frame_dos,command=self.datos_slider_uno,state='disabled',to=255,from_=0,orient='horizontal',length=280,style='TScale')
        #self.slider_uno.pack(pady=5,expand=1)
        #self.slider_dos=ttk.Scale(frame_dos,command=self.datos_slider_dos,state='disabled',to=255,from_=0,orient='horizontal',length=280,style='TScale')
        #self.slider_dos.pack(pady=5,expand=1)

        port=self.datos_arduino.puertos
        baud=self.datos_arduino.braudates

        Label(frame_uno,text="Puertos COM",bg='black',fg='white',font=('Arial',12,'bold')).pack(padx=5,expand=1)
        self.combobox_port=ttk.Combobox(frame_uno,values=port,justify='center',width=12,font='Arial')
        self.combobox_port.pack(pady=0,expand=1)
        self.combobox_port.current(0)

        Label(frame_uno,text="Baudrates",bg='black',fg='white',font=('Arial',12,'bold')).pack(padx=5,expand=1)
        self.combobox_baud=ttk.Combobox(frame_uno,values=baud,justify='center',width=12,font='Arial')
        self.combobox_baud.pack(pady=5,expand=1)
        self.combobox_baud.current(3)

        self.bt_conectar=Button(frame_uno,text='Conectar',font=('Arial',12,'bold'),width=12,bg='green',command=self.conectar_serial)
        self.bt_conectar.pack(pady=5,expand=1)

        self.bt_actualizar_puertos=Button(frame_uno,text='Actualizar',font=('Arial',12,'bold'),width=12,bg='green',command=self.actualizar_puertos)
        self.bt_actualizar_puertos.pack(pady=5,expand=1)

        self.bt_desconectar_puertos=Button(frame_uno,text='Desconectar',font=('Arial',12,'bold'),width=12,bg='red',command=self.desconectar_serial)
        self.bt_desconectar_puertos.pack(pady=5,expand=1)
        
        self.bt_cerrar_ventana=Button(frame_uno,text='Cerrar',font=('Arial',12,'bold'),width=12,bg='red',command=self.cerrar_ventana)
        self.bt_cerrar_ventana.pack(pady=5,expand=1)

        Label(frame_tres,image=self.logo,bg='black').pack(pady=5,expand=1)

    def actualizar_puertos(self):
        self.datos_arduino.puertos_disponibles()
    def conectar_serial(self):
        self.bt_conectar.config(state='disabled')
        self.bt_desconectar_puertos.config(state='normal')
        #self.slider_uno.config(state='normal')
        #self.slider_dos.config(state='normal')
        self.bt_reanudar.config(state='disabled')
        self.bt_cerrar_ventana.config(state='disabled')

        self.datos_arduino.arduino.port=self.combobox_port.get()
        self.datos_arduino.arduino.baudrate=self.combobox_baud.get()
        self.datos_arduino.conexion_serial()
    def desconectar_serial(self):
        self.bt_conectar.config(state='normal')
        self.bt_desconectar_puertos.config(state='disabled')
        #self.slider_uno.config(state='disabled')
        #self.slider_dos.config(state='disabled')
        self.bt_reanudar.config(state='disabled')
        self.bt_cerrar_ventana.config(state='normal')
        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        self.datos_arduino.desconectar()
    #def datos_slider_uno(self,*args):
    #    dato='1,'+str(int(self.slider_uno.get()))
    #    self.datos_arduino.enviar_datos(dato)
    #def datos_slider_dos(self,*args):
    #    dato='2,'+str(int(self.slider_dos.get()))
    #    self.datos_arduino.enviar_datos(dato)
    
    def cerrar_ventana(self):
        try:
            self.datos_arduino.desconectar()  # Desconecta la comunicación serial si es necesario
            if hasattr(self, 'ani'):
                self.ani.event_source.stop()  # Detener la animación si está corriendo
                from .informes import mostrar_pantalla_informes
                self.master.destroy()  # Cierra la ventana actual
                mostrar_pantalla_informes()
        except Exception as e:
            print(f"Error al cerrar la ventana: {e}")

def mostrar_ventana_informes_linea():
    # Verifica si ya existe un ciclo de mainloop ejecutándose antes de crear una nueva ventana
    try:
        root = Tk()
        root.geometry('742x535')
        root.config(bg='gray30',bd=4)
        root.wm_title('Grafica en Linea')
        root.minsize(width=700,height=400)
        app = Grafica(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al crear la ventana: {e}")
