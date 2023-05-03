import tkinter as tk
from PIL import Image, ImageTk
import ContinousGesturePredictor as gp
import pickle as pickle
from tkinter import filedialog
from tkinter import messagebox
import sys


#Clase para crear el frame de la sección CAPTURA DE IMÁGENES
class FramePredictor(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.config(width=717, height=370,relief=tk.GROOVE, borderwidth=1)
        self.pack( padx=10, pady=10)
        self.crear_widgets()

    def crear_widgets(self):
        # Agregar titulo de la sección
        label_title = tk.Label(self, text="Iniciar reconocimiento")
        # Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        # Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        #Agregar instrucción a la sección
        label_instruction1 = tk.Label(self, text="Ingrese los datos"
                                                " utilizados en el entrenamiento.")
        label_instruction1.config(font=("Arial", 11))
        label_instruction1.place(x=10, y=45)

        #Etiqueta para numero de imágenes
        label_num_img = tk.Label(self, text="No. de imágenes")
        label_num_img.place(x=10, y=80)
        #Etiqueta para el primer conjunto de imágenes : entrenamiento
        label_num_en = tk.Label(self, text="Entrenamiento:")
        label_num_en.place(x=10, y=105)
        #Caja de texto para el conjunto: entrenamiento
        self.num_ent = tk.Entry(self, width=9)
        self.num_ent.place(x=100, y=105)
        #Etiqueta para el segundo conjunto de imágenes: validación
        label_num_val = tk.Label(self, text="Validación:")
        label_num_val.place(x=175, y =105)
        #Caja de texto para el conjunto: validación
        self.num_val = tk.Entry(self, width=9)
        self.num_val.place(x=240, y= 105)

        # Etiqueta para tamaño de imagen
        label_size_img = tk.Label(self, text="Tamaño de imagen")
        label_size_img.place(x=320, y=80)
        # Etiqueta para el ancho
        label_w = tk.Label(self, text="Ancho:")
        label_w.place(x=320, y=105)
        # Caja de texto para el ancho
        self.textbox_w = tk.Entry(self, width=9)
        self.textbox_w.place(x=365, y=105)
        # Etiqueta para la altura
        label_h = tk.Label(self, text="Alto:")
        label_h.place(x=430, y=105)
        # Caja de texto para la altura
        self.textbox_h = tk.Entry(self, width=9)
        self.textbox_h.place(x=465, y=105)

        # Agregar instrucción a la sección
        label_instruction2 = tk.Label(self, text="Ingrese los archivos"
                                                " generados en el entrenamiento.")
        label_instruction2.config(font=("Arial", 11))
        label_instruction2.place(x=10, y=150)

        # Instrucción para la sección
        label_load_modelo = tk.Label(self, text="Carga del modelo entrenado:")
        # Colocar la etiqueta en el frame correspondiente
        label_load_modelo.place(x=20, y=190)

        # Caja de texto para mostrar la ruta seleccionada en el cual se cargara el modelo de red
        self.textbox_path = tk.Entry(self, width=55)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de un archivo
        self.textbox_path.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path.place(x=200, y=190)

        # Hacer referencias al icono del directorio
        image = ImageTk.PhotoImage(Image.open("icons/directorio.png"))

        # Botón para la selección de la ruta del archivo del modelo entrenado
        button_path = tk.Button(self, command=self.seleccionar_archivo)
        # Configurar icono del directorio
        button_path.image_names = image
        button_path.config(image=image)
        # Colocar el botón en el frame correspondiente
        button_path.place(x=540, y=185)

        #Etiqueta de carga de datos
        label_load_data = tk.Label(self, text="Carga de lista de gestos")
        label_load_data.place(x=20, y=230)

        #Caja de texto para mostrar la ruta seleccionada en el cual se cargaran los datos
        self.textbox_path_data = tk.Entry(self, width=55)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de un archivo
        self.textbox_path_data.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path_data.place(x=200, y=230)

        # Botón para la selección de la ruta del archivo de los datos
        button_path_data = tk.Button(self, command=self.seleccionar_archivo_datos)
        # Configurar icono del directorio
        button_path_data.image_names = image
        button_path_data.config(image=image)
        # Colocar el botón en el frame correspondiente
        button_path_data.place(x=540, y=225)

        #Instrucción para el reconocimiento
        label_ins_reco = tk.Label(self, text="Para empezar con el reconocimiento,"
                                             " presionar 's'. Para detenerlo, presionar 'q'.")
        label_ins_reco.config(font=("Arial", 11))
        label_ins_reco.place(x=10, y=265)

        #Botón para el inicio del reconocimiento
        button_start = tk.Button(self, text="Encender cámara", command=self.inicio_reconocimiento)
        # Configurar el formato del botón
        button_start.config(font=("Arial", 13, "bold"))
        button_start.place(x=290, y=305)

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
            num_ent_img = self.num_ent.get()
            num_val_img = self.num_val.get()
            size_w = self.textbox_w.get()
            size_h = self.textbox_h.get()
            #Confirmar que los campos no estén vacíos
            if self.textbox_path_data.get() != "" and self.textbox_path.get() != ""\
                    and num_ent_img and num_val_img\
                    and size_w and size_h:
                #Validar los numeros enteros
                if num_val_img.isdigit() and num_ent_img.isdigit() and size_w.isdigit() and size_h.isdigit():
                     gp.ContinuousGesturePredictor(self.textbox_path.get(),self.data_list,
                                                  int(num_ent_img),int(num_val_img),
                                                  int(size_w), int(size_h))
                else:
                    # Mensaje de error
                    messagebox.showerror("Error", "Revisa que los números sean enteros")
            else:
                #Mensaje de error
                messagebox.showerror("Error", "Revisa que los campos no estén vacíos")
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])