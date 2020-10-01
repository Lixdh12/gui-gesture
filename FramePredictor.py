import tkinter as tk
import ContinousGesturePredictor as gp
import pickle as pickle
from tkinter import filedialog
from tkinter import messagebox
import os, sys


#Clase para crear el frame de la sección CAPTURA DE IMÁGENES
class FramePredictor(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.config(width=617, height=200,relief=tk.GROOVE, borderwidth=1)
        self.pack(expand=1, padx=10, pady=10)
        self.crear_widgets()

    def crear_widgets(self):
        # Agregar titulo de la sección
        label_title = tk.Label(self, text="Iniciar reconocimiento")
        # Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        # Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        #Agregar instrucción a la sección
        label_instruction = tk.Label(self, text="Para esta sección es importante tener los dos archivos"
                                                " creados en la anterior sección.")
        label_instruction.place(x=10, y=45)

        # Instrucción para la sección
        label_load_modelo = tk.Label(self, text="Carga del modelo entrenado:")
        # Colocar la etiqueta en el frame correspondiente
        label_load_modelo.place(x=20, y=75)

        # Caja de texto para mostrar la ruta seleccionada en el cual se cargara el modelo de red
        self.textbox_path = tk.Entry(self, width=40)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de un archivo
        self.textbox_path.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path.place(x=200, y=75)

        # Botón para la selección de la ruta del archivo del modelo entrenado
        button_path = tk.Button(self, text="Seleccionar archivo", command=self.seleccionar_archivo)
        # Colocar el botón en el frame correspondiente
        button_path.place(x=450, y=70)

        #Etiqueta de carga de datos
        label_load_data = tk.Label(self, text="Carga de datos")
        label_load_data.place(x=20, y=120)

        #Caja de texto para mostrar la ruta seleccionada en el cual se cargaran los datos
        self.textbox_path_data = tk.Entry(self, width=40)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de un archivo
        self.textbox_path_data.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path_data.place(x=200, y=120)

        # Botón para la selección de la ruta del archivo de los datos
        button_path_data = tk.Button(self, text="Seleccionar archivo", command=self.seleccionar_archivo_datos)
        # Colocar el botón en el frame correspondiente
        button_path_data.place(x=450, y=115)

        #Botón para el inicio del reconocimiento
        button_start = tk.Button(self, text="Comenzar", command=self.inicio_reconocimiento)
        # Configurar el formato del botón
        button_start.config(font=("Arial", 10, "bold"))
        button_start.place(x=250, y=160)

    # Definir función para abrir un archivo del modelo entrenado
    def seleccionar_archivo(self):
        # Limpiar caja de texto de la ruta
        self.textbox_path.delete(0, "end")
        try:
            #Abrir el explorador de archivos para la selección de un archivo
            self.open_file_model = filedialog.askopenfilename(initialdir="/", title="Seleccione archivo",
                                                filetypes=[("Todos los Archivos","*.*")])
            # Se habilita la caja de texto para la edición de la ruta
            self.textbox_path.config(state="normal")
            #Insertar la ruta del archivo a la caja de texto
            self.textbox_path.insert(0,self.open_file_model)
        except:
            #Mensaje de error
            messagebox.showerror("Error", "Error al importar el archivo")

    #Obtención de datos desde un archivo de datos
    def seleccionar_archivo_datos(self):
        # Limpiar caja de texto de la ruta
        self.textbox_path_data.delete(0, "end")
        try:
            # Abrir el explorador de archivos para la selección de un archivo
            self.open_file_data = filedialog.askopenfilename(initialdir="/", title="Seleccione archivo",
                                                              filetypes=[("Archivos pickle", "*.pickle"), ("Todos los archivos", "*.*")])
            # Se habilita la caja de texto para la edición de la ruta
            self.textbox_path_data.config(state="normal")
            # Insertar la ruta del archivo a la caja de texto
            self.textbox_path_data.insert(0, self.open_file_data)

            #Abrir archivo
            file_data = open(self.open_file_data, "rb")
            # Obtener los datos
            self.data_list = pickle.load(file_data)
            # Cerrar el archivo
            file_data.close()
        except:
            # Mensaje de error
            messagebox.showerror("Error", "Error al importar el archivo")

    #Iniciar reconocimiento de gestos
    def inicio_reconocimiento(self):
        try:
            #Confirmar que los campos no estén vacíos
            if self.textbox_path_data.get() != "" and self.textbox_path.get() != "":
                gp.ContinuousGesturePredictor(self.textbox_path.get(),self.data_list)
            else:
                #Mensaje de error
                messagebox.showerror("Error", "Revisa que los campos no estén vacíos")
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])