import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from docentes_crud import DocentesCRUD  # Asegúrate de tener esta clase importada correctamente

class DocentesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Docentes")
        self.root.geometry("700x400")

        self.docentes_crud = DocentesCRUD()

        # Frame para la tabla
        self.frame_tabla = ttk.Frame(self.root)
        self.frame_tabla.pack(pady=20)

        # Crear tabla de docentes
        self.columns = ("ID", "Nombre", "Apellidos", "Correo")
        self.tabla_docentes = ttk.Treeview(self.frame_tabla, columns=self.columns, show="headings")
        for col in self.columns:
            self.tabla_docentes.heading(col, text=col)
            self.tabla_docentes.column(col, anchor=tk.W, width=150)

        self.tabla_docentes.pack()

        # Botones
        self.frame_botones = ttk.Frame(self.root)
        self.frame_botones.pack(pady=10)

        self.btn_crear = ttk.Button(self.frame_botones, text="Crear Docente", command=self.crear_docente)
        self.btn_crear.grid(row=0, column=0, padx=5)

        self.btn_actualizar = ttk.Button(self.frame_botones, text="Actualizar Docente", command=self.actualizar_docente)
        self.btn_actualizar.grid(row=0, column=1, padx=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="Eliminar Docente", command=self.eliminar_docente)
        self.btn_eliminar.grid(row=0, column=2, padx=5)

        # Entradas para creación y actualización
        self.frame_entradas = ttk.Frame(self.root)
        self.frame_entradas.pack(pady=20)

        self.lbl_nombre = ttk.Label(self.frame_entradas, text="Nombre:")
        self.lbl_nombre.grid(row=0, column=0, padx=5)

        self.entry_nombre = ttk.Entry(self.frame_entradas)
        self.entry_nombre.grid(row=0, column=1, padx=5)

        self.lbl_apellidos = ttk.Label(self.frame_entradas, text="Apellidos:")
        self.lbl_apellidos.grid(row=1, column=0, padx=5)

        self.entry_apellidos = ttk.Entry(self.frame_entradas)
        self.entry_apellidos.grid(row=1, column=1, padx=5)

        self.lbl_correo = ttk.Label(self.frame_entradas, text="Correo:")
        self.lbl_correo.grid(row=2, column=0, padx=5)

        self.entry_correo = ttk.Entry(self.frame_entradas)
        self.entry_correo.grid(row=2, column=1, padx=5)

        self.cargar_docentes()

    def cargar_docentes(self):
        """Carga los docentes en la tabla"""
        for row in self.tabla_docentes.get_children():
            self.tabla_docentes.delete(row)

        docentes = self.docentes_crud.leer_docentes()
        for docente in docentes:
            self.tabla_docentes.insert("", "end", values=docente)

    def crear_docente(self):
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        correo = self.entry_correo.get()

        if not nombre or not apellidos or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.docentes_crud.crear_docente(nombre, apellidos, correo)
            messagebox.showinfo("Éxito", "Docente creado exitosamente")
            self.cargar_docentes()  # Recargar la lista
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el docente: {e}")

    def actualizar_docente(self):
        selected_item = self.tabla_docentes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un docente")
            return

        id_docente = self.tabla_docentes.item(selected_item[0])["values"][0]
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        correo = self.entry_correo.get()

        if not nombre or not apellidos or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.docentes_crud.actualizar_docente(id_docente, nombre, apellidos, correo)
            messagebox.showinfo("Éxito", "Docente actualizado exitosamente")
            self.cargar_docentes()  # Recargar la lista
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el docente: {e}")

    def eliminar_docente(self):
        selected_item = self.tabla_docentes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un docente")
            return

        id_docente = self.tabla_docentes.item(selected_item[0])["values"][0]

        try:
            self.docentes_crud.eliminar_docente(id_docente)
            messagebox.showinfo("Éxito", "Docente eliminado exitosamente")
            self.cargar_docentes()  # Recargar la lista
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el docente: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocentesApp(root)
    root.mainloop()
