import serial, serial.tools.list_ports
from threading import Thread,Event
from tkinter import StringVar
import queue
import threading

class Comunicacion(threading.Thread):
    def __init__(self,datos_cola,*args):
        super().__init__(*args)
        self.datos_cola = datos_cola  # la cola de datos
        self.datos_recibidos=StringVar()
        self.arduino=serial.Serial()
        self.arduino.timeout=2
        self.braudates=['1200','2400','4800','9600','19200','38400','115200']
        self.puertos=[]
        self.señal=Event()
        self.hilo=None

    def puertos_disponibles(self):
        self.puertos=[port.device for port in serial.tools.list_ports.comports()]
        return self.puertos  # ← ¡Devuelve la lista!
    
    
    def conexion_serial(self, puerto=None, baudrate=9600):
       # Si self.arduino es None, crearlo de nuevo
        if self.arduino is None:
            self.arduino = serial.Serial()
       
        """Establece conexión con Arduino en un puerto y baudrate especificado"""
        if not puerto:
            puertos_disponibles = self.puertos_disponibles()
            if puertos_disponibles:
                puerto = puertos_disponibles[0]  # Tomamos el primer puerto disponible
            else:
                print("No hay puertos disponibles")
                return

        try:
            self.arduino.port = puerto
            self.arduino.baudrate = baudrate
            self.arduino.timeout=2
            self.arduino.dtr = False  # Deshabilita DTR
            self.arduino.rts = False  # Deshabilita RTS
            self.arduino.open()

            if self.arduino.is_open:
                self.iniciar_hilo()
                print(f'Conectado a {puerto} con baudrate {baudrate}')
        except serial.SerialException as e:
            print(f"Error al conectar con {puerto}: {e}")
            self.arduino = None

        
    def enviar_datos(self, data):
        if (self.arduino.is_open):
            self.datos=str(data)+"\n"
            self.arduino.write(self.datos.encode())
        else:
            print('Error an enviar datos')

    def leer_datos(self):
        try:
            while(self.señal.isSet()and self.arduino.is_open ):
                data=self.arduino.readline().decode('utf-8').strip()
                if not data:  # Evita procesar líneas vacías
                    continue  
                print("Datos recibidos:", data)  # Verifica qué llega exactamente
                self.datos_recibidos.set(data)  # Guarda los datos en String Var
                self.datos_cola.put(data)  #¡Ahora también los enviamos a la cola!
                print("Datos enviados a la cola:", data)  # Depuración
                print(f'Datos guardados',self.datos_recibidos)
        except (UnicodeDecodeError, TypeError) as e:
            print(f"Error al leer datos: {e}")  
            # Manejar errores específicos
        except Exception as e:
            print(f"Error inesperado: {e}")  
            # Capturar cualquier otro error

    def iniciar_hilo(self):
        self.hilo=Thread(target=self.leer_datos)
        self.hilo.setDaemon(1)
        self.señal.set()
        self.hilo.start()

    def detener_hilo(self):
        if(self.hilo is not None):
            self.señal.clear()
            self.hilo.join()
            self.hilo=None

    def desconectar(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            self.detener_hilo()
            print("Conexión cerrada con Arduino")
        else:
            print("No hay conexión activa con Arduino")
        self.arduino = None  # Asegurar que la variable se restablece correctamente
        
        
    


