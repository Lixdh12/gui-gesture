import tkinter as tk
from PIL import Image, ImageTk
import PalmTracker as pt
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import cv2

#Clase para crear el frame de la sección CAPTURA DE IMÁGENES
class FrameCapturaImagenes(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.config(width=617, height=173,relief=tk.GROOVE, borderwidth=1)
        self.pack(fill="both", expand=1, padx=10, pady=10)
        self.agregar_widgets()
        # En caso de no tener ninguna cadena la caja de texto, el button_capture estará deshabilitado
        # if self.textbox_path.get() == '':
        #    print(self.textbox_path.get() + "dentro")
        #   self.button_capture['state'] = tk.DISABLED
        #else:
        #    print(self.textbox_path.get())
        #    self.button_capture['state'] = tk.NORMAL

    def agregar_widgets(self):
        #Agregar titulo de la sección
        label_title = tk.Label(self, text="Capturar imágenes")
        #Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        #Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        #Instrucción para la sección
        label_instruction = tk.Label(self, text="Seleccione la carpeta para el almacenamiento y la cantidad"
                                                " de imágenes.")
        label_instruction.config(font=("Arial", 11))
        #Colocar la etiqueta en el frame correspondiente
        label_instruction.place(x=30, y=45)

        #Caja de texto para mostrar la ruta seleccionada en el cual, se guardarán las capturas de imágenes
        self.textbox_path = tk.Entry(self, width=62)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de una carpeta
        self.textbox_path.config(state="disabled")
        #Colocar la caja de texto en el frame correspondiente
        self.textbox_path.place(x=30, y=85)

        #Hacer referencias al icono del directorio
        image = ImageTk.PhotoImage(Image.open("icons/directorio.png"))

        #Botón para la selección de la ruta que guardará las capturas de imágenes
        button_path = tk.Button(self,  command=self.seleccionar_carpeta)
        #Configurar icono del directorio
        button_path.image_names=image
        button_path.config(image=image)
        #Colocar el botón en el frame correspondiente
        button_path.place(x=410, y=80)

        #Etiqueta para indicar campo de numero de capturas
        label_num_cap = tk.Label(self, text="No. de imágenes: ")
        label_num_cap.place(x=465, y=80)
        #Combobox para elegir el numero de imagenes que se capturaran con la camara web
        self.num_img = tk.Entry(self, width=10)
        #self.num_img["values"]=[100,1000]
        #self.num_img.current(0)
        self.num_img.place(x=568, y=80)

        # Hacer referencias al icono de información
        img_info = ImageTk.PhotoImage(Image.open("icons/info.png"))
        # Botón para la selección de la ruta que guardará las capturas de imágenes
        button_info = tk.Button(self, command=self.message_infor)
        # Configurar icono del directorio
        button_info.image_names = img_info
        button_info.config(image=img_info)
        # Colocar el botón en el frame correspondiente
        button_info.place(x=635, y=75)


        #Nota para señalar puntos importantes de la captura
        label_note = tk.Label(self, text="Una vez encendida la cámara: presionar 's' para iniciar la captura, 'p' "
                                         "para pausar y 'q' para salir.")
        label_note.place(x=60, y=125)

        #Botón para iniciar la captura de imágenes
        self.button_capture = tk.Button(self, text="Encender cámara", command=self.capturar_imagenes)
        #Configurar el formato del botón
        self.button_capture.config(font=("Arial", 10, "bold"))
        #Colocar el botón en el frame correspondiente
        self.button_capture.place(x=270, y=170)

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

    # Función para iniciar el proceso de captura de imagenes
    def capturar_imagenes(self):
        #Obtener el string del directorio seleccionado
        carpeta = self.textbox_path.get()
        num_imgs = self.num_img.get()
        #Si no hay una cadena en la caja de texto de la ruta de la carpeta, no procederá a la captura
        if carpeta != '' and num_imgs and num_imgs.isdigit():
            #Crear objeto de la clase PalmTracker y pasar el string
            palm_tracker = pt.PalmTracker(carpeta, int(num_imgs))
            #Llamar a la funcion main
            palm_tracker.main()
            #Liberar memoria
            palm_tracker.camera.release()
            cv2.destroyAllWindows()
            del palm_tracker.camera
        else:
            #Si no hay una ruta seleccionada aparecera un mensaje de error
            messagebox.showerror("Error", "Revisa que todos los campos no estén vacíos.")

    def message_infor(self):
        messagebox.showinfo("Redimensionar imágenes", "Para el entrenamiento de la red, un conjunto de imágenes"
                                                      " debe ser mayor que otro conjunto del mismo tipo."
                                                      " \n Ej. Gesto: Palma"
                                                      " \n- Para entrenamiento - 1000"
                                                      " \n- Para la validación    - 100")