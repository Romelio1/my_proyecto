import tkinter as tk
from tkinter import ttk, messagebox
from estudiantes_crud import EstudiantesCRUD  # Asumiendo que tu clase EstudiantesCRUD está en este archivo

class EstudiantesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Estudiantes")
        self.crud = EstudiantesCRUD()
        self.create_widgets()

    def create_widgets(self):
        # Definir el diseño (grid) de la ventana principal
        self.tree = ttk.Treeview(self.root, columns=("ID", "CI", "RU", "Nombre", "Apellidos", "Correo", "Estado", "Modalidad"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("CI", text="CI")
        self.tree.heading("RU", text="RU")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Modalidad", text="Modalidad")

        # Ajustar el tamaño de las columnas al contenido
        for col in self.tree["columns"]:
            self.tree.column(col, width=100, anchor="center", stretch=True)

        # Hacer que las columnas se ajusten automáticamente al contenido
        self.tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Botones de operaciones CRUD
        self.btn_crear = tk.Button(self.root, text="Crear Estudiante", width=20, command=self.crear_estudiante)
        self.btn_crear.grid(row=1, column=0, padx=10, pady=5)

        self.btn_actualizar = tk.Button(self.root, text="Actualizar Estudiante", width=20, command=self.actualizar_estudiante)
        self.btn_actualizar.grid(row=1, column=1, padx=10, pady=5)

        self.btn_eliminar = tk.Button(self.root, text="Eliminar Estudiante", width=20, command=self.eliminar_estudiante)
        self.btn_eliminar.grid(row=1, column=2, padx=10, pady=5)

        # Cargar los estudiantes en la tabla
        self.cargar_estudiantes()

    def cargar_estudiantes(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        estudiantes = self.crud.leer_estudiantes()  # Obtener los estudiantes desde la base de datos
        if estudiantes:
            for estudiante in estudiantes:
                self.tree.insert("", "end", values=estudiante)
        else:
            messagebox.showinfo("Información", "No se encontraron estudiantes.")

    def crear_estudiante(self):
        # Ventana emergente para crear un nuevo estudiante
        def guardar_estudiante():
            CI = entry_CI.get()
            RU = entry_RU.get()
            nombre = entry_nombre.get()
            apellidos = entry_apellidos.get()
            correo = entry_correo.get()
            estado = entry_estado.get()
            id_modalidad = entry_modalidad.get()

            if all([CI, RU, nombre, apellidos, correo, estado, id_modalidad]):
                self.crud.crear_estudiante(CI, RU, nombre, apellidos, correo, estado, id_modalidad)
                self.cargar_estudiantes()
                ventana_crear.destroy()
            else:
                messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")

        ventana_crear = tk.Toplevel(self.root)
        ventana_crear.title("Crear Estudiante")
        
        # Campos para ingresar los datos
        tk.Label(ventana_crear, text="CI:").grid(row=0, column=0, padx=10, pady=5)
        entry_CI = tk.Entry(ventana_crear)
        entry_CI.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana_crear, text="RU:").grid(row=1, column=0, padx=10, pady=5)
        entry_RU = tk.Entry(ventana_crear)
        entry_RU.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(ventana_crear, text="Nombre:").grid(row=2, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(ventana_crear)
        entry_nombre.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(ventana_crear, text="Apellidos:").grid(row=3, column=0, padx=10, pady=5)
        entry_apellidos = tk.Entry(ventana_crear)
        entry_apellidos.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(ventana_crear, text="Correo:").grid(row=4, column=0, padx=10, pady=5)
        entry_correo = tk.Entry(ventana_crear)
        entry_correo.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(ventana_crear, text="Estado:").grid(row=5, column=0, padx=10, pady=5)
        entry_estado = tk.Entry(ventana_crear)
        entry_estado.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(ventana_crear, text="Modalidad:").grid(row=6, column=0, padx=10, pady=5)
        entry_modalidad = tk.Entry(ventana_crear)
        entry_modalidad.grid(row=6, column=1, padx=10, pady=5)

        # Botón para guardar el estudiante
        btn_guardar = tk.Button(ventana_crear, text="Guardar", command=guardar_estudiante)
        btn_guardar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def actualizar_estudiante(self):
        messagebox.showinfo("Funcionalidad", "Funcionalidad de actualización aún no implementada.")

    def eliminar_estudiante(self):
        messagebox.showinfo("Funcionalidad", "Funcionalidad de eliminación aún no implementada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EstudiantesGUI(root)
    root.mainloop()

