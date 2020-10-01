import tkinter as tk
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
        label_title = tk.Label(self, text="Captura de imágenes")
        #Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        #Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        #Instrucción para la sección
        label_instruction = tk.Label(self, text="Selecciona la carpeta para el almacenamiento de imágenes")
        #Colocar la etiqueta en el frame correspondiente
        label_instruction.place(x=60, y=45)

        #Caja de texto para mostrar la ruta seleccionada en el cual, se guardarán las capturas de imágenes
        self.textbox_path = tk.Entry(self, width=50)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de una carpeta
        self.textbox_path.config(state="disabled")
        #Colocar la caja de texto en el frame correspondiente
        self.textbox_path.place(x=100, y=85)

        #Botón para la selección de la ruta que guardará las capturas de imágenes
        button_path = tk.Button(self, text="Seleccionar carpeta", command=self.seleccionar_carpeta)
        #Colocar el botón en el frame correspondiente
        button_path.place(x=410, y=80)

        #Etiqueta para indicar campo de numero de capturas
        label_num_cap = tk.Label(self, text="No. de capturas")
        label_num_cap.place(x=100, y=115)
        #Combobox para elegir el numero de imagenes que se capturaran con la camara web
        self.combo_num_cap = ttk.Combobox(self,state="readonly", width=10)
        self.combo_num_cap["values"]=[100,1000]
        self.combo_num_cap.current(0)
        self.combo_num_cap.place(x=200, y=115)


        #Nota para señalar puntos importantes de la captura
        label_note = tk.Label(self, text="*Al hacer clic en 'Iniciar captura', debe presionar la tecla 's'")
        label_note.place(x=150, y=145)

        #Botón para iniciar la captura de imágenes
        self.button_capture = tk.Button(self, text="Iniciar captura", command=self.capturar_imagenes)
        #Configurar el formato del botón
        self.button_capture.config(font=("Arial", 10, "bold"))
        #Colocar el botón en el frame correspondiente
        self.button_capture.place(x=250, y=170)

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
        #Si no hay una cadena en la caja de texto de la ruta de la carpeta, no procederá a la captura
        if carpeta != '':
            #Crear objeto de la clase PalmTracker y pasar el string
            palm_tracker = pt.PalmTracker(carpeta, int(self.combo_num_cap.get()))
            #Llamar a la funcion main
            palm_tracker.main()
            #Liberar memoria
            palm_tracker.camera.release()
            cv2.destroyAllWindows()
            del palm_tracker.camera
            #Mensaje informativo
            messagebox.showinfo("Éxito", "Captura realizada con éxito!")
        else:
            #Si no hay una ruta seleccionada aparecera un mensaje de error
            messagebox.showerror("Error", "No hay una carpeta seleccionada, por favor seleccione una.")