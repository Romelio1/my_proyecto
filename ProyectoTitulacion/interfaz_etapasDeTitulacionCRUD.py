import tkinter as tk
from tkinter import messagebox, ttk
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
            messagebox.showinfo("Éxito", "Etapa de Titulación creada exitosamente")
        except Error as e:
            messagebox.showerror("Error", f"Error al crear la etapa de titulación: {e}")
        finally:
            cursor.close()

    def leer_etapas(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Etapas_de_Titulacion"
            cursor.execute(query)
            etapas = cursor.fetchall()
            return etapas
        except Error as e:
            messagebox.showerror("Error", f"Error al leer las etapas de titulación: {e}")
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
            messagebox.showinfo("Éxito", "Etapa de Titulación actualizada exitosamente")
        except Error as e:
            messagebox.showerror("Error", f"Error al actualizar la etapa de titulación: {e}")
        finally:
            cursor.close()

    def eliminar_etapa(self, id_etapa):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Etapas_de_Titulacion WHERE id_etapa = %s"
            cursor.execute(query, (id_etapa,))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Etapa de Titulación eliminada exitosamente")
        except Error as e:
            messagebox.showerror("Error", f"Error al eliminar la etapa de titulación: {e}")
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()


class InterfazEtapas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Etapas de Titulación")
        self.root.geometry("700x500")
        self.crud = EtapasDeTitulacionCRUD()

        # Frame para los campos de entrada
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.nombre_label = tk.Label(self.frame, text="Nombre de la Etapa:")
        self.nombre_label.grid(row=0, column=0, padx=10, pady=5)
        self.nombre_entry = tk.Entry(self.frame)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        self.descripcion_label = tk.Label(self.frame, text="Descripción:")
        self.descripcion_label.grid(row=1, column=0, padx=10, pady=5)
        self.descripcion_entry = tk.Entry(self.frame)
        self.descripcion_entry.grid(row=1, column=1, padx=10, pady=5)

        self.modalidad_label = tk.Label(self.frame, text="ID Modalidad:")
        self.modalidad_label.grid(row=2, column=0, padx=10, pady=5)
        self.modalidad_entry = tk.Entry(self.frame)
        self.modalidad_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones de acción
        self.btn_crear = tk.Button(self.root, text="Crear Etapa", command=self.crear_etapa)
        self.btn_crear.pack(pady=10)

        self.btn_actualizar = tk.Button(self.root, text="Actualizar Etapa", command=self.actualizar_etapa)
        self.btn_actualizar.pack(pady=10)

        self.btn_eliminar = tk.Button(self.root, text="Eliminar Etapa", command=self.eliminar_etapa)
        self.btn_eliminar.pack(pady=10)

        # Tabla para mostrar los registros
        self.treeview = ttk.Treeview(self.root, columns=("ID", "Nombre", "Descripción", "ID Modalidad"), show="headings")
        self.treeview.pack(pady=20)

        # Definir las columnas
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre de la Etapa")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.heading("ID Modalidad", text="ID Modalidad")

        self.treeview.column("ID", width=50)
        self.treeview.column("Nombre", width=200)
        self.treeview.column("Descripción", width=250)
        self.treeview.column("ID Modalidad", width=100)

        self.cargar_etapas()

    def cargar_etapas(self):
        etapas = self.crud.leer_etapas()
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        if etapas:
            for etapa in etapas:
                self.treeview.insert("", "end", values=etapa)

    def crear_etapa(self):
        nombre_etapa = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        id_modalidad = self.modalidad_entry.get()

        if not nombre_etapa or not descripcion or not id_modalidad:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        self.crud.crear_etapa(nombre_etapa, descripcion, id_modalidad)
        self.cargar_etapas()

    def actualizar_etapa(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una etapa para actualizar.")
            return

        id_etapa = self.treeview.item(selected_item[0], "values")[0]
        nombre_etapa = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        id_modalidad = self.modalidad_entry.get()

        self.crud.actualizar_etapa(id_etapa, nombre_etapa, descripcion, id_modalidad)
        self.cargar_etapas()

    def eliminar_etapa(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una etapa para eliminar.")
            return

        id_etapa = self.treeview.item(selected_item[0], "values")[0]
        self.crud.eliminar_etapa(id_etapa)
        self.cargar_etapas()


if __name__ == "__main__":
    root = tk.Tk()
    interfaz = InterfazEtapas(root)
    root.mainloop()
