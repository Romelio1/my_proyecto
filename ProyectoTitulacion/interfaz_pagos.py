import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conexion import ConexionDB
from mysql.connector import Error
import tkinter.font as tkfont

# Clase principal de la interfaz gráfica
class PagosEtapasEvaluacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pagos de Etapas de Evaluación")
        
        # Instanciar CRUD
        self.pagos_crud = PagosEtapasEvaluacionCRUD()
        
        # Crear componentes de entrada
        tk.Label(root, text="ID Estudiante").grid(row=0, column=0)
        tk.Label(root, text="ID Etapa").grid(row=1, column=0)
        tk.Label(root, text="Monto").grid(row=2, column=0)
        tk.Label(root, text="Fecha de Pago (YYYY-MM-DD)").grid(row=3, column=0)
        
        self.id_estudiante = tk.Entry(root)
        self.id_etapa = tk.Entry(root)
        self.monto = tk.Entry(root)
        self.fecha_pago = tk.Entry(root)
        
        self.id_estudiante.grid(row=0, column=1)
        self.id_etapa.grid(row=1, column=1)
        self.monto.grid(row=2, column=1)
        self.fecha_pago.grid(row=3, column=1)
        
        # Botones para CRUD
        tk.Button(root, text="Crear Pago", command=self.crear_pago).grid(row=4, column=0)
        tk.Button(root, text="Actualizar Pago", command=self.actualizar_pago).grid(row=4, column=1)
        tk.Button(root, text="Eliminar Pago", command=self.eliminar_pago).grid(row=4, column=2)
        
        # Tabla para mostrar pagos
        self.tree_pagos = ttk.Treeview(root, columns=("ID Pago", "ID Estudiante", "ID Etapa", "Monto", "Fecha Pago"), show='headings')
        self.tree_pagos.heading("ID Pago", text="ID Pago")
        self.tree_pagos.heading("ID Estudiante", text="ID Estudiante")
        self.tree_pagos.heading("ID Etapa", text="ID Etapa")
        self.tree_pagos.heading("Monto", text="Monto")
        self.tree_pagos.heading("Fecha Pago", text="Fecha Pago")
        
        # Ajustar el tamaño de las columnas según el texto
        font = tkfont.Font()
        for column in self.tree_pagos["columns"]:
            self.tree_pagos.column(column, width=font.measure(column), anchor="w")
        
        self.tree_pagos.grid(row=5, column=0, columnspan=3, pady=10, padx=10)
        
        # Cargar datos en la tabla
        self.cargar_datos()

        # Enlace al evento de selección de la tabla
        self.tree_pagos.bind("<<TreeviewSelect>>", self.seleccionar_registro)
    
    def cargar_datos(self):
        """Carga los pagos en la tabla."""
        for item in self.tree_pagos.get_children():
            self.tree_pagos.delete(item)
        
        pagos = self.pagos_crud.leer_pagos_etapas()
        for pago in pagos:
            self.tree_pagos.insert("", "end", values=pago)
    
    def seleccionar_registro(self, event):
        """Rellena los campos con los datos del registro seleccionado."""
        selected_item = self.tree_pagos.selection()
        if selected_item:
            values = self.tree_pagos.item(selected_item)["values"]
            self.id_estudiante.delete(0, tk.END)
            self.id_estudiante.insert(0, values[1])
            self.id_etapa.delete(0, tk.END)
            self.id_etapa.insert(0, values[2])
            self.monto.delete(0, tk.END)
            self.monto.insert(0, values[3])
            self.fecha_pago.delete(0, tk.END)
            self.fecha_pago.insert(0, values[4])
    
    def crear_pago(self):
        """Crear un nuevo pago."""
        id_estudiante = self.id_estudiante.get()
        id_etapa = self.id_etapa.get()
        monto = self.monto.get()
        fecha_pago = self.fecha_pago.get()
        
        if not id_estudiante or not id_etapa or not monto or not fecha_pago:
            messagebox.showwarning("Campos incompletos", "Todos los campos deben ser llenados.")
            return
        
        self.pagos_crud.crear_pago_etapa(id_estudiante, id_etapa, monto, fecha_pago)
        self.cargar_datos()
    
    def actualizar_pago(self):
        """Actualizar un pago seleccionado."""
        selected_item = self.tree_pagos.selection()
        if not selected_item:
            messagebox.showwarning("No seleccionado", "Selecciona un pago para actualizar.")
            return
        
        id_pago_etapa = self.tree_pagos.item(selected_item)["values"][0]
        id_estudiante = self.id_estudiante.get()
        id_etapa = self.id_etapa.get()
        monto = self.monto.get()
        fecha_pago = self.fecha_pago.get()
        
        self.pagos_crud.actualizar_pago_etapa(id_pago_etapa, id_estudiante, id_etapa, monto, fecha_pago)
        self.cargar_datos()
    
    def eliminar_pago(self):
        """Eliminar un pago seleccionado."""
        selected_item = self.tree_pagos.selection()
        if not selected_item:
            messagebox.showwarning("No seleccionado", "Selecciona un pago para eliminar.")
            return
        
        id_pago_etapa = self.tree_pagos.item(selected_item)["values"][0]
        self.pagos_crud.eliminar_pago_etapa(id_pago_etapa)
        self.cargar_datos()

# Clase CRUD para los pagos de etapas de evaluación
class PagosEtapasEvaluacionCRUD:
    def __init__(self):
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
            return pagos
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
        except Error as e:
            print("Error al eliminar el pago de etapa:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = PagosEtapasEvaluacionApp(root)
    root.mainloop()
