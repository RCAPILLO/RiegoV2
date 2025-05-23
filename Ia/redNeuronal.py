import queue
import threading
import time
from datetime import datetime

class RedNeuronal(threading.Thread):
    def __init__(self, comunicacion, riego, datos_cola):
        super().__init__()  # Inicializa el Thread
        self.comunicacion = comunicacion  # Objeto de la clase Comunicacion
        self.riego = riego  # Objeto de la clase Riego
        self.datos_cola = datos_cola  # Cola para recibir datos entre hilos
        self.hilo_riego = None  # Hilo para ejecutar el riego
        
        self.ejecutando = threading.Event()  # Control del hilo
        self.activo = threading.Event()      # Control del modo automático (activo/inactivo)
        self.activo.set()                    # Por defecto, está activo
        # Pesos de la red neuronal (ajustar según entrenamiento)
        self.w_humedad = 0.68
        self.w_temperatura = 0.5
        self.bias = -0.6

    def evaluar_riego(self, humedad_suelo, temp_amb):
        """ Evalúa si se debe activar el riego usando la red neuronal """
        salida_nn = (humedad_suelo * self.w_humedad) + (temp_amb * self.w_temperatura) + self.bias
        return salida_nn > 0  # Si la salida es mayor a 0, activar riego

    def iniciar_riego(self):
        if self.datos_cola.empty():
            print("La cola de datos está vacía. Verifica la conexión con Arduino.")

        """ Inicia el riego en un hilo separado y lo monitorea """
        if self.hilo_riego is None or not self.hilo_riego.is_alive():
            self.ejecutando.set()
            self.hilo_riego = threading.Thread(target=self.regar)
            self.hilo_riego.start()

    def detener_riego(self):
        """ Detiene el riego """
        self.ejecutando.clear()
        self.comunicacion.enviar_datos("OFF")  # Enviar comando a Arduino
        print("Riego detenido")
    def detener(self):
        """ Detiene el control automático y cualquier riego en curso """
        self.activo.clear()
        self.detener_riego()
        print("Red neuronal detenida (modo manual activado)")

    def reanudar(self):
        """ Reanuda el control automático de riego """
        self.activo.set()
        print("Red neuronal activada (modo automático)")
    
    def regar(self):
        """ Mantiene el riego activado hasta que la humedad alcance el umbral o pase el tiempo límite """
        try:
            datos_sensores = self.datos_cola.get(timeout=5)
            temp_amb,humedad_amb, humedad_inicio = map(float, datos_sensores.split(","))
        except queue.Empty:
            print("No se recibieron datos para iniciar el riego. Abortando.")
            return
    
        inicio = datetime.now()
        self.comunicacion.enviar_datos("ON")
        print("Riego activado")

        humedad_fin = humedad_inicio  # valor por defecto

        while self.ejecutando.is_set():
            try:
                # Leer los datos de la cola
                datos_sensores = self.datos_cola.get(timeout=1)  # Espera hasta 1 segundo para recibir datos
                temp_amb,humedad_amb,humedad_suelo= map(float, datos_sensores.split(","))
                humedad_fin = humedad_suelo  # se actualiza en cada iteración
                estado_riego=self.evaluar_riego(humedad_suelo,temp_amb)#Revisar que valor devuelve la red neuronal
                print(f"Estado NN: {estado_riego}, Humedad: {humedad_suelo}")
                
                # Condiciones de parada: humedad >= 55% o tiempo > 40 minutos o NN indica apagar
                tiempo_transcurrido = (datetime.now() - inicio).seconds
                if humedad_suelo >= 55 or tiempo_transcurrido >= 2400 or not estado_riego:
                    self.detener_riego()
                    break
                
                time.sleep(10)  # Revisar cada 10 segundos

            except queue.Empty:
                print("Soy la rede Nuronal, Esperando datos de sensores...")

        # Guardar datos en MySQL
        fin = datetime.now()
        duracion = (fin - inicio).seconds
        consumo=float((duracion/3600)*(3*2.2*249))
        self.riego.guardar_en_riego(inicio, fin, humedad_inicio, humedad_fin, duracion,consumo)
    

    def run(self):
        print("Red neuronal en funcion")
        while self.activo.is_set():
            try:
                datos_sensores = self.datos_cola.get(timeout=1)
                humedad_suelo, temp_amb, _ = map(float, datos_sensores.split(","))
                if self.evaluar_riego(humedad_suelo, temp_amb):
                    print("Red reuronal encendio el riego")
                    self.iniciar_riego()
                time.sleep(60)
            except queue.Empty:
                continue
