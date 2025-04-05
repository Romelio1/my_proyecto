from conexion import ConexionDB
from mysql.connector import Error

class AsignacionTutorCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_asignacion(self, id_estudiante, id_tutor, fecha_asignacion):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Asignacion_Tutor (id_estudiante, id_tutor, fecha_asignacion)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (id_estudiante, id_tutor, fecha_asignacion))
            self.connection.commit()
            print("Asignación de tutor creada exitosamente")
        except Error as e:
            print("Error al crear la asignación:", e)
        finally:
            cursor.close()

    def leer_asignaciones(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Asignacion_Tutor"
            cursor.execute(query)
            asignaciones = cursor.fetchall()
            for asignacion in asignaciones:
                print(asignacion)
        except Error as e:
            print("Error al leer las asignaciones:", e)
        finally:
            cursor.close()

    def actualizar_asignacion(self, id_asignacion, id_estudiante=None, id_tutor=None, fecha_asignacion=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if id_estudiante:
                campos.append("id_estudiante = %s")
                valores.append(id_estudiante)
            if id_tutor:
                campos.append("id_tutor = %s")
                valores.append(id_tutor)
            if fecha_asignacion:
                campos.append("fecha_asignacion = %s")
                valores.append(fecha_asignacion)
            
            valores.append(id_asignacion)
            query = f"UPDATE Asignacion_Tutor SET {', '.join(campos)} WHERE id_asignacion = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Asignación de tutor actualizada exitosamente")
        except Error as e:
            print("Error al actualizar la asignación:", e)
        finally:
            cursor.close()

    def eliminar_asignacion(self, id_asignacion):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Asignacion_Tutor WHERE id_asignacion = %s"
            cursor.execute(query, (id_asignacion,))
            self.connection.commit()
            print("Asignación de tutor eliminada exitosamente")
        except Error as e:
            print("Error al eliminar la asignación:", e)
        finally:
            cursor.close()

    def leer_estudiantes_con_tutor(self):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT e.id_estudiante, e.nombre, e.apellidos, a.fecha_asignacion
            FROM Estudiantes e
            JOIN Asignacion_Tutor a ON e.id_estudiante = a.id_estudiante
            """
            cursor.execute(query)
            estudiantes_con_tutor = cursor.fetchall()
            return estudiantes_con_tutor
        except Error as e:
            print("Error al leer los estudiantes con tutor:", e)
            return []
        finally:
            cursor.close()

    def leer_estudiantes_sin_tutor(self):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT e.id_estudiante, e.nombre, e.apellidos 
            FROM Estudiantes e
            LEFT JOIN Asignacion_Tutor a ON e.id_estudiante = a.id_estudiante
            WHERE a.id_estudiante IS NULL
            """
            cursor.execute(query)
            estudiantes_sin_tutor = cursor.fetchall()
            return estudiantes_sin_tutor
        except Error as e:
            print("Error al leer los estudiantes sin tutor:", e)
            return []
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()
