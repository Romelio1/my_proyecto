import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        # Datos de conexión
        self.host = "localhost"  # el host
        self.database = "monitorear_titulacion"  #el name de la base de datos
        self.user = "root"  #el usuario
        self.password = "vida"  #la contraseña
        
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print("Error al conectar a la base de datos:", e)
            self.connection = None

    def get_connection(self):
        return self.connection

    def cerrar_conexion(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada")

