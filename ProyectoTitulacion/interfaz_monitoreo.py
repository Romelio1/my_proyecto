import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conexion import ConexionDB
from mysql.connector import Error
import tkinter.font as tkfont

# Clase principal de la interfaz gráfica
class MonitoreoTitulacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoreo de Titulación")

        # Instanciar CRUD
        self.monitoreo_crud = MonitoreoTitulacionCRUD()

        # Crear componentes de entrada
        tk.Label(root, text="ID Estudiante").grid(row=0, column=0)
        tk.Label(root, text="ID Etapa").grid(row=1, column=0)
        tk.Label(root, text="Fecha Inicio (YYYY-MM-DD)").grid(row=2, column=0)
        tk.Label(root, text="Fecha Fin (YYYY-MM-DD)").grid(row=3, column=0)
        tk.Label(root, text="  Estado   ").grid(row=4, column=0)

        self.id_estudiante = tk.Entry(root)
        self.id_etapa = tk.Entry(root)
        self.fecha_inicio = tk.Entry(root)
        self.fecha_fin = tk.Entry(root)
        self.estado = tk.Entry(root)

        self.id_estudiante.grid(row=0, column=1)
        self.id_etapa.grid(row=1, column=1)
        self.fecha_inicio.grid(row=2, column=1)
        self.fecha_fin.grid(row=3, column=1)
        self.estado.grid(row=4, column=1)

        # Botones para CRUD
        tk.Button(root, text="Crear Monitoreo", command=self.crear_monitoreo).grid(row=5, column=0)
        tk.Button(root, text="Actualizar Monitoreo", command=self.actualizar_monitoreo).grid(row=5, column=1)
        tk.Button(root, text="Eliminar Monitoreo", command=self.eliminar_monitoreo).grid(row=5, column=2)

        # Tabla para mostrar monitoreos
        self.tree_monitoreos = ttk.Treeview(root, columns=("ID Monitoreo", "ID Estudiante", "ID Etapa", "Fecha Inicio", "Fecha Fin", "Estado"), show='headings')
        self.tree_monitoreos.heading("ID Monitoreo", text="ID Monitoreo")
        self.tree_monitoreos.heading("ID Estudiante", text="ID Estudiante")
        self.tree_monitoreos.heading("ID Etapa", text="ID Etapa")
        self.tree_monitoreos.heading("Fecha Inicio", text="Fecha Inicio")
        self.tree_monitoreos.heading("Fecha Fin", text="Fecha Fin")
        self.tree_monitoreos.heading("Estado", text="Estado")

        # Ajustar el tamaño de las columnas según el texto
        font = tkfont.Font()
        for column in self.tree_monitoreos["columns"]:
            self.tree_monitoreos.column(column, width=font.measure(column), anchor="w")

        self.tree_monitoreos.grid(row=6, column=0, columnspan=3, pady=10, padx=10)

        # Cargar datos en la tabla
        self.cargar_datos()

        # Enlace al evento de selección de la tabla
        self.tree_monitoreos.bind("<<TreeviewSelect>>", self.seleccionar_registro)

    def cargar_datos(self):
        """Carga los monitoreos en la tabla."""
        for item in self.tree_monitoreos.get_children():
            self.tree_monitoreos.delete(item)

        monitoreos = self.monitoreo_crud.leer_monitoreos()
        for monitoreo in monitoreos:
            self.tree_monitoreos.insert("", "end", values=monitoreo)

    def seleccionar_registro(self, event):
        """Rellena los campos con los datos del registro seleccionado."""
        selected_item = self.tree_monitoreos.selection()
        if selected_item:
            values = self.tree_monitoreos.item(selected_item)["values"]
            self.id_estudiante.delete(0, tk.END)
            self.id_estudiante.insert(0, values[1])
            self.id_etapa.delete(0, tk.END)
            self.id_etapa.insert(0, values[2])
            self.fecha_inicio.delete(0, tk.END)
            self.fecha_inicio.insert(0, values[3])
            self.fecha_fin.delete(0, tk.END)
            self.fecha_fin.insert(0, values[4])
            self.estado.delete(0, tk.END)
            self.estado.insert(0, values[5])

    def crear_monitoreo(self):
        """Crear un nuevo monitoreo."""
        id_estudiante = self.id_estudiante.get()
        id_etapa = self.id_etapa.get()
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        estado = self.estado.get()

        if not id_estudiante or not id_etapa or not fecha_inicio or not fecha_fin or not estado:
            messagebox.showwarning("Campos incompletos", "Todos los campos deben ser llenados.")
            return

        self.monitoreo_crud.crear_monitoreo(id_estudiante, id_etapa, fecha_inicio, fecha_fin, estado)
        self.cargar_datos()

    def actualizar_monitoreo(self):
        """Actualizar un monitoreo seleccionado."""
        selected_item = self.tree_monitoreos.selection()
        if not selected_item:
            messagebox.showwarning("No seleccionado", "Selecciona un monitoreo para actualizar.")
            return

        id_monitoreo = self.tree_monitoreos.item(selected_item)["values"][0]
        id_estudiante = self.id_estudiante.get()
        id_etapa = self.id_etapa.get()
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        estado = self.estado.get()

        self.monitoreo_crud.actualizar_monitoreo(id_monitoreo, id_estudiante, id_etapa, fecha_inicio, fecha_fin, estado)
        self.cargar_datos()

    def eliminar_monitoreo(self):
        """Eliminar un monitoreo seleccionado."""
        selected_item = self.tree_monitoreos.selection()
        if not selected_item:
            messagebox.showwarning("No seleccionado", "Selecciona un monitoreo para eliminar.")
            return

        id_monitoreo = self.tree_monitoreos.item(selected_item)["values"][0]
        self.monitoreo_crud.eliminar_monitoreo(id_monitoreo)
        self.cargar_datos()


# Clase CRUD para el monitoreo de titulación
class MonitoreoTitulacionCRUD:
    def __init__(self):
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
            return monitoreos
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
        except Error as e:
            print("Error al eliminar el monitoreo de titulación:", e)
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conexion_db.cerrar_conexion()


# Crear ventana principal
root = tk.Tk()
app = MonitoreoTitulacionApp(root)
root.mainloop()
