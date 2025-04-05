from conexion import ConexionDB
from mysql.connector import Error

class MonitoreoTitulacionCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_monitoreo(self, id_estudiante, id_etapa, fecha_inicio, fecha_fin, estado):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Monitoreo_Titulacion (id_estudiante, id_etapa, fecha_inicio, fecha_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_estudiante, id_etapa, fecha_inicio, fecha_fin, estado))
            self.connection.commit()
            print("Monitoreo de titulación registrado exitosamente")
        except Error as e:
            print("Error al registrar el monitoreo de titulación:", e)
        finally:
            cursor.close()

    def leer_monitoreos(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Monitoreo_Titulacion"
            cursor.execute(query)
            monitoreos = cursor.fetchall()
            for monitoreo in monitoreos:
                print(monitoreo)
        except Error as e:
            print("Error al leer los monitoreos de titulación:", e)
        finally:
            cursor.close()

    def actualizar_monitoreo(self, id_monitoreo, id_estudiante=None, id_etapa=None, fecha_inicio=None, fecha_fin=None, estado=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if id_estudiante:
                campos.append("id_estudiante = %s")
                valores.append(id_estudiante)
            if id_etapa:
                campos.append("id_etapa = %s")
                valores.append(id_etapa)
            if fecha_inicio:
                campos.append("fecha_inicio = %s")
                valores.append(fecha_inicio)
            if fecha_fin:
                campos.append("fecha_fin = %s")
                valores.append(fecha_fin)
            if estado:
                campos.append("estado = %s")
                valores.append(estado)
            
            valores.append(id_monitoreo)
            query = f"UPDATE Monitoreo_Titulacion SET {', '.join(campos)} WHERE id_monitoreo = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Monitoreo de titulación actualizado exitosamente")
        except Error as e:
            print("Error al actualizar el monitoreo de titulación:", e)
        finally:
            cursor.close()

    def eliminar_monitoreo(self, id_monitoreo):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Monitoreo_Titulacion WHERE id_monitoreo = %s"
            cursor.execute(query, (id_monitoreo,))
            self.connection.commit()
            print("Monitoreo de titulación eliminado exitosamente")
        except Error as e:
            print("Error al eliminar el monitoreo de titulación:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()
