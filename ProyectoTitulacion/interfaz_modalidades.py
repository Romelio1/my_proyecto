import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from modalidades_crud import ModalidadesGraduacionCRUD  # Asegúrate de importar correctamente tu clase

class InterfazCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Modalidades de Graduación")
        self.root.geometry("600x400")
        self.root.config(bg="white")
        
        # Crear una instancia de ModalidadesGraduacionCRUD
        self.modalidad_crud = ModalidadesGraduacionCRUD()

        self.id_var = tk.StringVar()
        self.nombre_modalidad_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()

        # Crear la tabla para mostrar modalidades
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre Modalidad", "Descripción"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre Modalidad", text="Nombre Modalidad")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        # Agregar registros a la tabla
        self.cargar_modalidades()

        # Crear entradas para agregar o editar modalidades
        self.id_label = tk.Label(self.root, text="ID", bg="white", fg="black")
        self.id_label.grid(row=1, column=0)
        self.id_entry = tk.Entry(self.root, textvariable=self.id_var, bg="lightgray")
        self.id_entry.grid(row=1, column=1)

        self.nombre_modalidad_label = tk.Label(self.root, text="Nombre Modalidad", bg="white", fg="black")
        self.nombre_modalidad_label.grid(row=2, column=0)
        self.nombre_modalidad_entry = tk.Entry(self.root, textvariable=self.nombre_modalidad_var, bg="lightgray")
        self.nombre_modalidad_entry.grid(row=2, column=1)

        self.descripcion_label = tk.Label(self.root, text="Descripción", bg="white", fg="black")
        self.descripcion_label.grid(row=3, column=0)
        self.descripcion_entry = tk.Entry(self.root, textvariable=self.descripcion_var, bg="lightgray")
        self.descripcion_entry.grid(row=3, column=1)

        # Botones de acción
        self.btn_add = tk.Button(self.root, text="Agregar", command=self.agregar_modalidad, bg="black", fg="white")
        self.btn_add.grid(row=4, column=0, pady=10)

        self.btn_update = tk.Button(self.root, text="Actualizar", command=self.actualizar_modalidad, bg="black", fg="white")
        self.btn_update.grid(row=4, column=1, pady=10)

        self.btn_delete = tk.Button(self.root, text="Eliminar", command=self.eliminar_modalidad, bg="black", fg="white")
        self.btn_delete.grid(row=4, column=2, pady=10)

    def cargar_modalidades(self):
        # Limpiar los registros existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener y mostrar las modalidades en la tabla
        modalidades = self.modalidad_crud.leer_modalidades()
        for modalidad in modalidades:
            self.tree.insert("", "end", values=(modalidad[0], modalidad[1], modalidad[2]))

    def agregar_modalidad(self):
        nombre_modalidad = self.nombre_modalidad_var.get()
        descripcion = self.descripcion_var.get()
        if nombre_modalidad and descripcion:
            self.modalidad_crud.crear_modalidad(nombre_modalidad, descripcion)
            self.cargar_modalidades()
            self.limpiar_entradas()
            messagebox.showinfo("Éxito", "Modalidad de graduación agregada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    def actualizar_modalidad(self):
        id_modalidad = self.id_var.get()
        nombre_modalidad = self.nombre_modalidad_var.get()
        descripcion = self.descripcion_var.get()

        if id_modalidad:
            self.modalidad_crud.actualizar_modalidad(id_modalidad, nombre_modalidad, descripcion)
            self.cargar_modalidades()
            self.limpiar_entradas()
            messagebox.showinfo("Éxito", "Modalidad de graduación actualizada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID válido.")

    def eliminar_modalidad(self):
        id_modalidad = self.id_var.get()
        if id_modalidad:
            self.modalidad_crud.eliminar_modalidad(id_modalidad)
            self.cargar_modalidades()
            self.limpiar_entradas()
            messagebox.showinfo("Éxito", "Modalidad de graduación eliminada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID válido.")

    def limpiar_entradas(self):
        self.id_var.set("")
        self.nombre_modalidad_var.set("")
        self.descripcion_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    interfaz = InterfazCRUD(root)
    root.mainloop()
