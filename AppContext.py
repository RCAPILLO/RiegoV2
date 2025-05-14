from Comunicacion.comunicacion import Comunicacion
from queue import Queue
from Utilitarios.riego import Riego
from Ia.redNeuronal import RedNeuronal

class AppContext:
    def __init__(self):
        # Componentes compartidos
        self.datos_cola = Queue()
        self.datos_arduino = Comunicacion(self.datos_cola)
        self.datos_arduino.conexion_serial()
        self.comunicacion = None
        self.riego = Riego("localhost", "root", "", "sistema_riego")

        # Red neuronal aún no se inicia
        self.red_neuronal = None

    def iniciar_red_neuronal(self):
        if self.red_neuronal is None:
            self.red_neuronal = RedNeuronal(
                self.datos_arduino, self.riego, self.datos_cola
            )
            self.red_neuronal.start()
            print("Red neuronal iniciada")
        elif not self.red_neuronal.is_alive():
            print("El hilo de red neuronal se ha detenido.")
        else:
            print("Red neuronal ya está corriendo.")

    def activar_modo_automatico(self):
        if self.red_neuronal:
            self.red_neuronal.reanudar()

    def activar_modo_manual(self):
        if self.red_neuronal:
            self.red_neuronal.detener()

    def ia_esta_activa(self):
        return self.red_neuronal and self.red_neuronal.activo.is_set()
    
    def detener_todo(self):
        if hasattr(self, "arduino") and self.arduino:
            self.arduino.close()

        if hasattr(self, "hilo_red_neuronal") and self.hilo_red_neuronal.is_alive():
            self.hilo_red_neuronal.detener()  # Debes definir un método seguro de parada

        print("Recursos liberados correctamente.")
