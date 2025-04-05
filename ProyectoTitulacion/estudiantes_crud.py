

from conexion import ConexionDB
from mysql.connector import Error

class EstudiantesCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_estudiante(self, CI, RU, nombre, apellidos, correo, estado, id_modalidad):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Estudiantes (CI, RU, nombre, apellidos, correo, estado, id_modalidad)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (CI, RU, nombre, apellidos, correo, estado, id_modalidad))
            self.connection.commit()
            print("Estudiante creado exitosamente")
        except Error as e:
            print("Error al crear el estudiante:", e)
        finally:
            cursor.close()

    def leer_estudiantes(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Estudiantes"
            cursor.execute(query)
            estudiantes = cursor.fetchall()
            return estudiantes  # Devolver los registros en lugar de imprimirlos
        except Error as e:
            print("Error al leer los estudiantes:", e)
            return []
        finally:
            cursor.close()

    def actualizar_estudiante(self, id_estudiante, CI=None, RU=None, nombre=None, apellidos=None, correo=None, estado=None, id_modalidad=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if CI:
                campos.append("CI = %s")
                valores.append(CI)
            if RU:
                campos.append("RU = %s")
                valores.append(RU)
            if nombre:
                campos.append("nombre = %s")
                valores.append(nombre)
            if apellidos:
                campos.append("apellidos = %s")
                valores.append(apellidos)
            if correo:
                campos.append("correo = %s")
                valores.append(correo)
            if estado:
                campos.append("estado = %s")
                valores.append(estado)
            if id_modalidad:
                campos.append("id_modalidad = %s")
                valores.append(id_modalidad)
            
            valores.append(id_estudiante)
            query = f"UPDATE Estudiantes SET {', '.join(campos)} WHERE id_estudiante = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Estudiante actualizado exitosamente")
        except Error as e:
            print("Error al actualizar el estudiante:", e)
        finally:
            cursor.close()

    def eliminar_estudiante(self, id_estudiante):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Estudiantes WHERE id_estudiante = %s"
            cursor.execute(query, (id_estudiante,))
            self.connection.commit()
            print("Estudiante eliminado exitosamente")
        except Error as e:
            print("Error al eliminar el estudiante:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()
