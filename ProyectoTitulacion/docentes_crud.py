from conexion import ConexionDB
from mysql.connector import Error

class DocentesCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_docente(self, nombre, apellidos, correo):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Docentes (nombre, apellidos, correo)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre, apellidos, correo))
            self.connection.commit()
            print("Docente creado exitosamente")
        except Error as e:
            print("Error al crear el docente:", e)
        finally:
            cursor.close()

    def leer_docentes(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Docentes"
            cursor.execute(query)
            docentes = cursor.fetchall()
            return docentes if docentes else []  # Devuelve una lista vacía si no hay resultados
        except Error as e:
            print("Error al leer los docentes:", e)
            return []  # Devuelve una lista vacía en caso de error
        finally:
            cursor.close()

    def actualizar_docente(self, id_docente, nombre=None, apellidos=None, correo=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if nombre:
                campos.append("nombre = %s")
                valores.append(nombre)
            if apellidos:
                campos.append("apellidos = %s")
                valores.append(apellidos)
            if correo:
                campos.append("correo = %s")
                valores.append(correo)
            
            valores.append(id_docente)
            query = f"UPDATE Docentes SET {', '.join(campos)} WHERE id_docente = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Docente actualizado exitosamente")
        except Error as e:
            print("Error al actualizar el docente:", e)
        finally:
            cursor.close()

    def eliminar_docente(self, id_docente):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Docentes WHERE id_docente = %s"
            cursor.execute(query, (id_docente,))
            self.connection.commit()
            print("Docente eliminado exitosamente")
        except Error as e:
            print("Error al eliminar el docente:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()

