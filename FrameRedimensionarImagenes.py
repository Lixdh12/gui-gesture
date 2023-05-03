import tkinter as tk
from PIL import Image, ImageTk
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
        label_title = tk.Label(self, text="Redimensionar imágenes")
        # Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        # Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        # Instrucción para la sección
        label_instruction = tk.Label(self, justify=tk.LEFT, text="Seleccione la carpeta,"
                                                                 " ingrese la cantidad y las nuevas"
                                                                 " dimensiones de las imágenes.")
        label_instruction.config(font=("Arial", 11))
        # Colocar la etiqueta en el frame correspondiente
        label_instruction.place(x=30, y=45)

        # Caja de texto para mostrar la ruta seleccionada en el cual, se guardarán las capturas de imágenes
        self.textbox_path = tk.Entry(self, width=62)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de una carpeta
        self.textbox_path.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path.place(x=30, y=105)

        # Hacer referencias al icono del directorio
        image = ImageTk.PhotoImage(Image.open("icons/directorio.png"))

        # Botón para la selección de la ruta que guardará las capturas de imágenes
        button_path = tk.Button(self,  command=self.seleccionar_carpeta)
        # Configurar icono del directorio
        button_path.image_names = image
        button_path.config(image=image)
        # Colocar el botón en el frame correspondiente
        button_path.place(x=410, y=100)

        #Etiqueta para el titulo 'Pixeles'
        label_pixeles = tk.Label(self, text="Nuevas dimensiones")
        label_pixeles.config(font=(4))
        label_pixeles.place(x=60, y=135)
        #Etiqueta para "Alto"
        label_pixeles = tk.Label(self, text="Ancho:")
        label_pixeles.place(x=110, y=160)
        #variables para los pixeles
        self.value_pixel1 = tk.StringVar()
        self.value_pixel2 = tk.StringVar()
        self.value_pixel1.set('100')
        self.value_pixel2.set('89')
        #1era Caja de texto para el ancho de la imagen
        self.textbox_pixel_1 = tk.Entry(self, width=10, textvariable=self.value_pixel1)
        self.textbox_pixel_1.place(x=160, y=160)
        #Etiqueta 'X'
        label_x = tk.Label(self, text="Alto:")
        label_x.place(x=245, y=160)
        #2da Caja de texto para la altura de la imagen
        self.textbox_pixel_2 = tk.Entry(self, width=10, textvariable=self.value_pixel2)
        self.textbox_pixel_2.place(x=285, y=160)

        # Etiqueta para indicar campo de numero de capturas
        label_num_cap = tk.Label(self, text="No. de imágenes")
        label_num_cap.place(x=465, y=100)
        # Caja de texto para elegir el numero de imagenes que se capturaran con la camara web
        self.num_img = tk.Entry(self, width=10)#ttk.Combobox(self, state="readonly", width=10)
        #self.combo_num_cap["values"] = [100, 1000]
        #self.combo_num_cap.current(0)
        self.num_img.place(x=568, y=100)

        # Hacer referencias al icono de información
        img_info = ImageTk.PhotoImage(Image.open("icons/info.png"))
        # Botón para la selección de la ruta que guardará las capturas de imágenes
        button_info = tk.Button(self, command=self.message_infor)
        # Configurar icono del directorio
        button_info.image_names = img_info
        button_info.config(image=img_info)
        # Colocar el botón en el frame correspondiente
        button_info.place(x=635, y=95)

        # Botón para iniciar la redimension de imágenes
        self.button_resize = tk.Button(self, text="Iniciar redimensión", command=self.redimensionar_imagenes)
        # Configurar el formato del botón
        self.button_resize.config(font=("Arial", 10, "bold"))
        # Colocar el botón en el frame correspondiente
        self.button_resize.place(x=270, y=200)

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
        num_imgs = self.num_img.get()
        #Comprobar que se han incresado caracteres en las cajas de texto de esta sección
        if carpeta != "" and pixel_cad1 != "" and pixel_cad2 != "" and num_imgs:
            #Comprobar que los caracteres que se ingresaron sean númericos
            if pixel_cad1.isdigit() and pixel_cad2.isdigit() and num_imgs.isdigit():
                # Crear objeto de la clase RisizeImages y pasar el string
                resize = ri.ResizeImages(carpeta, int(pixel_cad1), int(pixel_cad2), int(num_imgs), self.f_window)
                # Llamar a la función principal de la clase
                #resize.main()
            else:
                # Se mostrará un mensaje de error
                messagebox.showerror("Error", "Revise que los números sean enteros")
        else:
            #Se mostrará un mensaje de error
            messagebox.showerror("Error", "Revise que los campos de esta sección estén completos")

    def message_infor(self):
        messagebox.showinfo("Redimensionar imágenes", "Para el entrenamiento de la red, un conjunto de imágenes"
                                                      " debe ser mayor que otro conjunto del mismo tipo."
                                                      " \n Ej. Gesto: Palma"
                                                      " \n- Para entrenamiento - 1000"
                                                      " \n- Para la validación    - 100")