from conexion import ConexionDB
from mysql.connector import Error

class PagosEtapasEvaluacionCRUD:
    def __init__(self):
        # Usar la clase ConexionDB para obtener la conexión
        self.conexion_db = ConexionDB()
        self.connection = self.conexion_db.get_connection()

    def crear_pago_etapa(self, id_estudiante, id_etapa, monto, fecha_pago):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Pagos_Etapas_Evaluacion (id_estudiante, id_etapa, monto, fecha_pago)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_estudiante, id_etapa, monto, fecha_pago))
            self.connection.commit()
            print("Pago de etapa registrado exitosamente")
        except Error as e:
            print("Error al registrar el pago de etapa:", e)
        finally:
            cursor.close()

    def leer_pagos_etapas(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Pagos_Etapas_Evaluacion"
            cursor.execute(query)
            pagos = cursor.fetchall()
            for pago in pagos:
                print(pago)
        except Error as e:
            print("Error al leer los pagos de etapas:", e)
        finally:
            cursor.close()

    def actualizar_pago_etapa(self, id_pago_etapa, id_estudiante=None, id_etapa=None, monto=None, fecha_pago=None):
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
            if monto:
                campos.append("monto = %s")
                valores.append(monto)
            if fecha_pago:
                campos.append("fecha_pago = %s")
                valores.append(fecha_pago)
            
            valores.append(id_pago_etapa)
            query = f"UPDATE Pagos_Etapas_Evaluacion SET {', '.join(campos)} WHERE id_pago_etapa = %s"
            cursor.execute(query, tuple(valores))
            self.connection.commit()
            print("Pago de etapa actualizado exitosamente")
        except Error as e:
            print("Error al actualizar el pago de etapa:", e)
        finally:
            cursor.close()

    def eliminar_pago_etapa(self, id_pago_etapa):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Pagos_Etapas_Evaluacion WHERE id_pago_etapa = %s"
            cursor.execute(query, (id_pago_etapa,))
            self.connection.commit()
            print("Pago de etapa eliminado exitosamente")
        except Error as e:
            print("Error al eliminar el pago de etapa:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()
