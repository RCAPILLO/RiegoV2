import datetime
import mysql.connector
import os

class Riego:
    def __init__(self, host, user, password, database, archivo_sd="riego.txt"):
        self.host = host
        self.user = user
        self.password =password
        self.database = database
        self.archivo_sd = archivo_sd

    # Conectar a MySQL
    def conectar_base_datos(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conexion
        except Exception as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    # Guardar datos en MySQL
    def guardar_en_riego(self, hora_inicio, hora_fin, humedad_inicio, humedad_fin, duracion):
        conexion = self.conectar_base_datos()
        if not conexion:
            print(" No hay conexión, guardando en SD...")
            self.guardar_en_sd(hora_inicio, hora_fin, humedad_inicio, humedad_fin, duracion)
            return

        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO registro_riego (hora_inicio, hora_fin, humedad_inicio, humedad_fin, duracion) VALUES (%s, %s, %s, %s, %s)"
            valores = (hora_inicio, hora_fin, humedad_inicio, humedad_fin, duracion)
            cursor.execute(sql, valores)
            conexion.commit()
            print("!! Datos guardados en MySQL.")
        except Exception as e:
            print(f"Error al guardar en MySQL: {e}")
        finally:
            conexion.close()

    # Guardar datos en SD
    def guardar_en_sd(self, hora_inicio, hora_fin, humedad_inicio, humedad_fin, duracion):
        try:
            with open(self.archivo_sd, "a") as archivo:
                archivo.write(f"{hora_inicio},{hora_fin},{humedad_inicio},{humedad_fin},{duracion}\n")
            print("Datos guardados en SD.")
        except Exception as e:
            print(f"Error al guardar en SD: {e}")

    # Sincronizar SD con MySQL
    def sincronizar_desde_sd(self):
        if not os.path.exists(self.archivo_sd):
            print(" No hay datos locales pendientes.")
            return

        with open(self.archivo_sd, "r") as archivo:
            lineas = archivo.readlines()

        if not lineas:
            print("Archivo vacío, nada que sincronizar.")
            return

        for linea in lineas:
            datos = linea.strip().split(",")
            if len(datos) == 5:
                self.guardar_en_riego(*datos)

        os.remove(self.archivo_sd)  # Elimina el archivo tras la sincronización
        print(" Datos locales sincronizados con MySQL.")

    def guardar_cultivo(self, cultivo, zona, fecha_siembra):
        conexion = self.conectar_base_datos()
        if not conexion:
            print("No hay conexión")
            self.guardar_en_sd(cultivo, zona, fecha_siembra)
            return

        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO cultivos (nombre, zona, fecha_siembra) VALUES (%s, %s, %s)"
            valores = (cultivo, zona, fecha_siembra)
            cursor.execute(sql, valores)
            conexion.commit()
            print(" Cultivo guardado en MySQL.")
        except Exception as e:
            print(f" Error al guardar en MySQL: {e}")
        finally:
            conexion.close()
    def ultimo_riego_programado(self):
        conexion = self.conectar_base_datos()
        if not conexion:
            print("Error: No hay conexión a la base de datos.")
            return None

        try:
            cursor = conexion.cursor()
            consulta = """
            SELECT nombre, zona, fecha_siembra
            FROM cultivos
            ORDER BY fecha_siembra DESC
            LIMIT 1;
            """
            cursor.execute(consulta)
            resultado = cursor.fetchone()
            return resultado if resultado else None

        except mysql.connector.Error as e:
            print(f"Error al recuperar los datos: {e}")
            return None
