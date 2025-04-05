from conexion import ConexionDB
from mysql.connector import Error

class PagosTitulacionCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_pago(self, id_estudiante, monto, fecha_pago, descripcion):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Pagos_Titulacion (id_estudiante, monto, fecha_pago, descripcion)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_estudiante, monto, fecha_pago, descripcion))
            self.connection.commit()
            print("Pago registrado exitosamente")
        except Error as e:
            print("Error al registrar el pago:", e)
        finally:
            cursor.close()

    def leer_pagos(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Pagos_Titulacion"
            cursor.execute(query)
            pagos = cursor.fetchall()
            for pago in pagos:
                print(pago)
        except Error as e:
            print("Error al leer los pagos:", e)
        finally:
            cursor.close()

    def actualizar_pago(self, id_pago, id_estudiante=None, monto=None, fecha_pago=None, descripcion=None):
        try:
            cursor = self.connection.cursor()
            campos = []
            valores = []
            
            if id_estudiante:
                campos.append("id_estudiante = %s")
                valores.append(id_estudiante)
            if monto:
                campos.append("monto = %s")
                valores.append(monto)
            if fecha_pago:
                campos.append("fecha_pago = %s")
                valores.append(fecha_pago)
            if descripcion:
                campos.append("descripcion = %s")
                valores.append(descripcion)
            
            valores.append(id_pago)
            query = f"UPDATE Pagos_Titulacion SET {', '.join(campos)} WHERE id_pago = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Pago actualizado exitosamente")
        except Error as e:
            print("Error al actualizar el pago:", e)
        finally:
            cursor.close()

    def eliminar_pago(self, id_pago):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Pagos_Titulacion WHERE id_pago = %s"
            cursor.execute(query, (id_pago,))
            self.connection.commit()
            print("Pago eliminado exitosamente")
        except Error as e:
            print("Error al eliminar el pago:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()
