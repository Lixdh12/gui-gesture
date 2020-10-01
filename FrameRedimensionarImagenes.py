import tkinter as tk
import ResizeImages as ri
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os, sys

#Clase para crear el frame de la sección REDIMENSIÓN DE IMÁGENES
class FrameRedimensionarImagenes(tk.Frame):

    def __init__(self, master, father_window):
        super().__init__(master)
        self.f_window = father_window
        self.config(width=617, height=173,relief=tk.GROOVE, borderwidth=1)
        self.pack(fill="both", expand=1, padx=10, pady=10)
        self.agregar_widgets()

    def agregar_widgets(self):
        #Titulo de la sección contenido en una etiqueta (Label)
        label_title = tk.Label(self, text="Redimensión de imágenes")
        # Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        # Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        # Instrucción para la sección
        label_instruction = tk.Label(self, text="Cambiar el tamaño de las imágenes de la carpeta "
                                                "seleccionada de acuerdo a los pixeles")
        # Colocar la etiqueta en el frame correspondiente
        label_instruction.place(x=50, y=45)

        # Caja de texto para mostrar la ruta seleccionada en el cual, se guardarán las capturas de imágenes
        self.textbox_path = tk.Entry(self, width=50)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de una carpeta
        self.textbox_path.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path.place(x=100, y=85)

        # Botón para la selección de la ruta que guardará las capturas de imágenes
        button_path = tk.Button(self, text="Seleccionar carpeta",  command=self.seleccionar_carpeta)
        # Colocar el botón en el frame correspondiente
        button_path.place(x=410, y=80)

        #Etiqueta para el titulo 'Pixeles'
        label_pixeles = tk.Label(self, text="Pixeles")
        label_pixeles.place(x=110, y=120)

        #variables para los pixeles
        self.value_pixel1 = tk.StringVar()
        self.value_pixel2 = tk.StringVar()
        self.value_pixel1.set('100')
        self.value_pixel2.set('89')
        #1era Caja de texto para el ancho de la imagen
        self.textbox_pixel_1 = tk.Entry(self, width=10, textvariable=self.value_pixel1)
        self.textbox_pixel_1.place(x=160, y=120)
        #Etiqueta 'X'
        label_x = tk.Label(self, text="X")
        label_x.place(x=235, y=120)
        #2da Caja de texto para la altura de la imagen
        self.textbox_pixel_2 = tk.Entry(self, width=10, textvariable=self.value_pixel2)
        self.textbox_pixel_2.place(x=260, y=120)

        # Etiqueta para indicar campo de numero de capturas
        label_num_cap = tk.Label(self, text="No. de capturas")
        label_num_cap.place(x=330, y=120)
        # Combobox para elegir el numero de imagenes que se capturaran con la camara web
        self.combo_num_cap = ttk.Combobox(self, state="readonly", width=10)
        self.combo_num_cap["values"] = [100, 1000]
        self.combo_num_cap.current(0)
        self.combo_num_cap.place(x=420, y=120)

        # Botón para iniciar la redimension de imágenes
        self.button_resize = tk.Button(self, text="Iniciar redimensión", command=self.redimensionar_imagenes)
        # Configurar el formato del botón
        self.button_resize.config(font=("Arial", 10, "bold"))
        # Colocar el botón en el frame correspondiente
        self.button_resize.place(x=240, y=165)

    # Definir función para abrir un directorio
    def seleccionar_carpeta(self):
        # Limpiar caja de texto de la ruta
        self.textbox_path.delete(0, "end")
        directorio = filedialog.askdirectory()
        if directorio != "":
            os.chdir(directorio)
        # Se habilita la caja de texto para la edición de la ruta
        self.textbox_path.config(state="normal")
        # Se muestra el directorio seleccionado en la caja de texto
        self.textbox_path.insert(0, os.getcwd())

    # Función para iniciar la redimensión de imagenes
    def redimensionar_imagenes(self):
        # Obtener el string del directorio seleccionado
        carpeta = self.textbox_path.get()
        pixel_cad1 = self.value_pixel1.get()
        pixel_cad2 = self.value_pixel2.get()
        #Comprobar que se han incresado caracteres en las cajas de texto de esta sección
        if carpeta != "" and pixel_cad1 != "" and pixel_cad2 != "":
            #Comprobar que los caracteres que se ingresaron sean númericos
            if pixel_cad1.isdigit() and pixel_cad2.isdigit():
                # Crear objeto de la clase RisizeImages y pasar el string
                resize = ri.ResizeImages(carpeta, int(pixel_cad1), int(pixel_cad2), int(self.combo_num_cap.get()), self.f_window)
                # Llamar a la función principal de la clase
                #resize.main()
            else:
                # Se mostrará un mensaje de error
                messagebox.showerror("Error", "Revise que los pixeles sean números")
        else:
            #Se mostrará un mensaje de error
            messagebox.showerror("Error", "Revise que los campos de esta sección estén completos")