from conexion import ConexionDB
from mysql.connector import Error

class ModalidadesGraduacionCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_modalidad(self, nombre_modalidad, descripcion):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Modalidades_de_Graduacion (nombre_modalidad, descripcion)
            VALUES (%s, %s)
            """
            cursor.execute(query, (nombre_modalidad, descripcion))
            self.connection.commit()
            print("Modalidad de graduación creada exitosamente")
        except Error as e:
            print("Error al crear la modalidad de graduación:", e)
        finally:
            cursor.close()

    def leer_modalidades(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Modalidades_de_Graduacion"
            cursor.execute(query)
            modalidades = cursor.fetchall()

            if modalidades is None:
                print("No se encontraron modalidades de graduación.")
                return []  # Retorna una lista vacía si no hay resultados

            for modalidad in modalidades:
                print(modalidad)
            return modalidades  # Devuelve la lista de modalidades
        except Error as e:
            print("Error al leer las modalidades de graduación:", e)
            return []  # Si ocurre un error, devuelve una lista vacía
        finally:
            cursor.close()

    def actualizar_modalidad(self, id_modalidad, nombre_modalidad=None, descripcion=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if nombre_modalidad:
                campos.append("nombre_modalidad = %s")
                valores.append(nombre_modalidad)
            if descripcion:
                campos.append("descripcion = %s")
                valores.append(descripcion)
            
            valores.append(id_modalidad)
            query = f"UPDATE Modalidades_de_Graduacion SET {', '.join(campos)} WHERE id_modalidad = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Modalidad de graduación actualizada exitosamente")
        except Error as e:
            print("Error al actualizar la modalidad de graduación:", e)
        finally:
            cursor.close()

    def eliminar_modalidad(self, id_modalidad):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Modalidades_de_Graduacion WHERE id_modalidad = %s"
            cursor.execute(query, (id_modalidad,))
            self.connection.commit()
            print("Modalidad de graduación eliminada exitosamente")
        except Error as e:
            print("Error al eliminar la modalidad de graduación:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()



