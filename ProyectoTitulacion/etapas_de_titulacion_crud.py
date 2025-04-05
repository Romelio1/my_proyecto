from conexion import ConexionDB
from mysql.connector import Error

class EtapasDeTitulacionCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_etapa(self, nombre_etapa, descripcion, id_modalidad):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Etapas_de_Titulacion (nombre_etapa, descripcion, id_modalidad)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre_etapa, descripcion, id_modalidad))
            self.connection.commit()
            print("Etapa de Titulación creada exitosamente")
        except Error as e:
            print("Error al crear la etapa de titulación:", e)
        finally:
            cursor.close()

    def leer_etapas(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Etapas_de_Titulacion"
            cursor.execute(query)
            etapas = cursor.fetchall()
            for etapa in etapas:
                print(etapa)
        except Error as e:
            print("Error al leer las etapas de titulación:", e)
        finally:
            cursor.close()

    def actualizar_etapa(self, id_etapa, nombre_etapa=None, descripcion=None, id_modalidad=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if nombre_etapa:
                campos.append("nombre_etapa = %s")
                valores.append(nombre_etapa)
            if descripcion:
                campos.append("descripcion = %s")
                valores.append(descripcion)
            if id_modalidad:
                campos.append("id_modalidad = %s")
                valores.append(id_modalidad)
            
            valores.append(id_etapa)
            query = f"UPDATE Etapas_de_Titulacion SET {', '.join(campos)} WHERE id_etapa = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Etapa de Titulación actualizada exitosamente")
        except Error as e:
            print("Error al actualizar la etapa de titulación:", e)
        finally:
            cursor.close()

    def eliminar_etapa(self, id_etapa):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Etapas_de_Titulacion WHERE id_etapa = %s"
            cursor.execute(query, (id_etapa,))
            self.connection.commit()
            print("Etapa de Titulación eliminada exitosamente")
        except Error as e:
            print("Error al eliminar la etapa de titulación:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()
