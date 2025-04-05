import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from conexion import ConexionDB
from asignacion_tutor_crud import AsignacionTutorCRUD  # Ensure this class is implemented

class AsignacionTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Asignación de Tutores")
        
        # Instanciar CRUD
        self.asignacion_crud = AsignacionTutorCRUD()
        
        # Crear componentes de entrada
        tk.Label(root, text="ID Estudiante").grid(row=0, column=0)
        tk.Label(root, text="ID Tutor").grid(row=1, column=0)
        tk.Label(root, text="Fecha Asignación (YYYY-MM-DD)").grid(row=2, column=0)
        
        self.id_estudiante = tk.Entry(root)
        self.id_tutor = tk.Entry(root)
        self.fecha_asignacion = tk.Entry(root)
        
        self.id_estudiante.grid(row=0, column=1)
        self.id_tutor.grid(row=1, column=1)
        self.fecha_asignacion.grid(row=2, column=1)
        
        # Botones para CRUD
        tk.Button(root, text="Crear Asignación", command=self.crear_asignacion).grid(row=3, column=0)
        tk.Button(root, text="Actualizar Asignación", command=self.actualizar_asignacion).grid(row=3, column=1)
        tk.Button(root, text="Eliminar Asignación", command=self.eliminar_asignacion).grid(row=3, column=2)
        
        # Tabla para estudiantes con tutor asignado
        self.tree_asignados = ttk.Treeview(root, columns=("ID Asignación", "ID Estudiante", "ID Tutor", "Fecha Asignación"), show='headings')
        self.tree_asignados.heading("ID Asignación", text="ID Asignación")
        self.tree_asignados.heading("ID Estudiante", text="ID Estudiante")
        self.tree_asignados.heading("ID Tutor", text="ID Tutor")
        self.tree_asignados.heading("Fecha Asignación", text="Fecha Asignación")
        self.tree_asignados.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
        
        # Ajustar el tamaño de las columnas automáticamente
        for column in self.tree_asignados["columns"]:
            self.tree_asignados.column(column, width=tk.font.Font().measure(column), anchor="w")

        # Vincular la selección para mostrar datos en campos de entrada
        self.tree_asignados.bind("<<TreeviewSelect>>", self.mostrar_seleccion)

        # Tabla para estudiantes sin tutor asignado
        self.tree_no_asignados = ttk.Treeview(root, columns=("ID Estudiante", "Nombre", "Apellido"), show='headings')
        self.tree_no_asignados.heading("ID Estudiante", text="ID Estudiante")
        self.tree_no_asignados.heading("Nombre", text="Nombre")
        self.tree_no_asignados.heading("Apellido", text="Apellido")
        self.tree_no_asignados.grid(row=5, column=0, columnspan=3, pady=10, padx=10)

        # Cargar datos en tablas
        self.cargar_datos()

    def crear_asignacion(self):
        id_estudiante = self.id_estudiante.get()
        id_tutor = self.id_tutor.get()
        fecha_asignacion = self.fecha_asignacion.get()
        if id_estudiante and id_tutor and fecha_asignacion:
            self.asignacion_crud.crear_asignacion(id_estudiante, id_tutor, fecha_asignacion)
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Asignación creada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")

    def actualizar_asignacion(self):
        id_asignacion = self.obtener_id_seleccionado(self.tree_asignados)
        if id_asignacion:
            id_estudiante = self.id_estudiante.get()
            id_tutor = self.id_tutor.get()
            fecha_asignacion = self.fecha_asignacion.get()
            self.asignacion_crud.actualizar_asignacion(id_asignacion, id_estudiante, id_tutor, fecha_asignacion)
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Asignación actualizada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona una asignación para actualizar")

    def eliminar_asignacion(self):
        id_asignacion = self.obtener_id_seleccionado(self.tree_asignados)
        if id_asignacion:
            self.asignacion_crud.eliminar_asignacion(id_asignacion)
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Asignación eliminada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona una asignación para eliminar")

    def cargar_datos(self):
        # Limpiar tablas
        for row in self.tree_asignados.get_children():
            self.tree_asignados.delete(row)
        for row in self.tree_no_asignados.get_children():
            self.tree_no_asignados.delete(row)

        # Cargar estudiantes con tutor asignado
        asignaciones = self.asignacion_crud.leer_estudiantes_con_tutor()
        for asignacion in asignaciones:
            self.tree_asignados.insert("", "end", values=asignacion)

        # Cargar estudiantes sin tutor asignado (consulta a base de datos)
        estudiantes_sin_tutor = self.asignacion_crud.leer_estudiantes_sin_tutor()
        for estudiante in estudiantes_sin_tutor:
            self.tree_no_asignados.insert("", "end", values=estudiante)

    def mostrar_seleccion(self, event):
        # Obtener datos del elemento seleccionado
        selected_item = self.tree_asignados.selection()
        if selected_item:
            item_values = self.tree_asignados.item(selected_item[0], 'values')
            # Llenar los campos de entrada con los valores seleccionados
            self.id_estudiante.delete(0, tk.END)
            self.id_estudiante.insert(0, item_values[1])
            self.id_tutor.delete(0, tk.END)
            self.id_tutor.insert(0, item_values[2])
            self.fecha_asignacion.delete(0, tk.END)
            self.fecha_asignacion.insert(0, item_values[3])

    def obtener_id_seleccionado(self, tree):
        selected = tree.selection()
        if selected:
            return tree.item(selected)["values"][0]
        return None

# Ejecutar la aplicación
root = tk.Tk()
app = AsignacionTutorApp(root)
root.mainloop()

