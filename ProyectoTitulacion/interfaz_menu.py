import tkinter as tk
from tkinter import font
from tkinter import messagebox
import subprocess

class MenuPrincipalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal del Sistema de Titulación")
        self.root.geometry("400x600")  # Tamaño de la ventana
        self.root.resizable(False, False)  # No permitir cambiar el tamaño
        self.root.configure(bg="#f4f4f4")  # Color de fondo suave

        # Fuente y estilo de botones
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")

        # Título del menú
        title_label = tk.Label(root, text="Menú Principal", font=self.title_font, bg="#f4f4f4")
        title_label.pack(pady=20)

        # Frame para contener los botones de manera ordenada
        frame = tk.Frame(root, bg="#f4f4f4")
        frame.pack(pady=10)

        # Botones con estilo
        self.create_button(frame, "Asignación de Tutor", self.abrir_asignacion_tutor)
        self.create_button(frame, "Gestión de Docentes", self.abrir_gestion_docentes)
        self.create_button(frame, "Gestión de Estudiantes", self.abrir_gestion_estudiantes)
        self.create_button(frame, "Etapas de Titulación", self.abrir_etapas_titulacion)
        self.create_button(frame, "Modalidades de Titulación", self.abrir_modalidades)
        self.create_button(frame, "Monitoreo de Titulación", self.abrir_monitoreo)
        self.create_button(frame, "Pagos de Titulación", self.abrir_pagos)

        # Botón para salir
        exit_button = tk.Button(root, text="Salir", width=30, height=2, command=root.quit, font=self.button_font, bg="#ff6666", fg="white", relief="flat")
        exit_button.pack(pady=20)

    def create_button(self, parent, text, command):
        """Crea un botón con estilo personalizado"""
        button = tk.Button(parent, text=text, width=30, height=2, command=command, font=self.button_font, bg="#4CAF50", fg="white", relief="flat", bd=0)
        button.pack(pady=8)
        button.bind("<Enter>", lambda e: self.on_enter(button))  # Hover effect
        button.bind("<Leave>", lambda e: self.on_leave(button))  # Hover effect

    def on_enter(self, button):
        """Efecto hover cuando el ratón entra en el botón"""
        button.config(bg="#45a049")

    def on_leave(self, button):
        """Efecto hover cuando el ratón sale del botón"""
        button.config(bg="#4CAF50")

    def abrir_asignacion_tutor(self):
        """Abrir la interfaz de Asignación de Tutor"""
        subprocess.run(["python", "interfaz_asignacion_tutor.py"])

    def abrir_gestion_docentes(self):
        """Abrir la interfaz de Gestión de Docentes"""
        subprocess.run(["python", "interfaz_docentes.py"])

    def abrir_gestion_estudiantes(self):
        """Abrir la interfaz de Gestión de Estudiantes"""
        subprocess.run(["python", "interfaz_estudiantes.py"])

    def abrir_etapas_titulacion(self):
        """Abrir la interfaz de Etapas de Titulación"""
        subprocess.run(["python", "interfaz_etapasDeTitulacionCRUD.py"])

    def abrir_modalidades(self):
        """Abrir la interfaz de Modalidades de Titulación"""
        subprocess.run(["python", "interfaz_modalidades.py"])

    def abrir_monitoreo(self):
        """Abrir la interfaz de Monitoreo de Titulación"""
        subprocess.run(["python", "interfaz_monitoreo.py"])

    def abrir_pagos(self):
        """Abrir la interfaz de Pagos de Titulación"""
        subprocess.run(["python", "interfaz_pagos.py"])

# Crear ventana principal
root = tk.Tk()
app = MenuPrincipalApp(root)
root.mainloop()
