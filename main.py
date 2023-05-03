import FrameCapturaImagenes as captura
import FrameRedimensionarImagenes as redimensionar
import FrameEntrenamientoRed as entrenamiento
import FramePredictor as reconocimiento
#import ProgressCallback as pc
import ResizeImages as resize
import tkinter as tk
from tkinter import ttk

class Sistema:

    def __init__(self):
        #Inicializar la ventana de la aplicación
        #Se crea objeto de Tkinter, para crear la ventana principal
        self.ventana_principal = tk.Tk()
        #Se agrega titulo a la ventana
        self.ventana_principal.title("Sistema de administración y almacenamiento para el reconocimiento de patrones gestuales")
        self.centrar_ventana()
        #Se configura las dimensiones de la ventana
        #self.ventana_principal.geometry("700x520")
        self.ventana_principal.resizable(width=False, height=False)
        #Llamada a la función a la ventana
        self.inicializar_frames()
        #La ventana se visualiza
        self.ventana_principal.mainloop()

    def centrar_ventana(self):
        #Dimensiones de la ventana
        w = 800
        h = 620
        #Determinar la anchira y longitud de la pantalla
        sw = self.ventana_principal.winfo_screenwidth()
        sh = self.ventana_principal.winfo_screenheight()
        #Calcular las coordenadas x / y
        x = (sw-w)/2
        y = (sh-h)/2
        #Dar dimensiones y ubicacion a la ventana
        self.ventana_principal.geometry('%dx%d+%d+%d'% (w,h,x,y))

    def inicializar_frames(self):
        # Crear frame principal
        frame_principal = tk.Frame(self.ventana_principal, width=670, height=470,relief=tk.GROOVE, borderwidth=5)
        #Empaquetar el frame a la ventana raíz, con un margen de 'x'=15 y en 'y'=15
        frame_principal.pack(fill="both", expand=1, padx=15, pady=15)

        #Notebook para las pestañas de las secciones
        tab_padre = ttk.Notebook(frame_principal)
        #Pestañas para las diferentes secciones del sistema
        #Pestaña para las secciones de Captura y Redimensión de imagenes
        tab_captura_redimension = ttk.Frame(tab_padre)
        # Se agrega al Nootebook
        tab_padre.add(tab_captura_redimension, text="1. Capturar/Redimensionar imágenes")
        #Pestaña para la sección de Entrenamiento de la red
        tab_entrenamiento = ttk.Frame(tab_padre)
        # Se agrega al Nootebook
        tab_padre.add(tab_entrenamiento, text="2. Entrenamiento de la red")
        #Pestaña para la sección del Inicio del Reconocimiento
        tab_reconocimiento = ttk.Frame(tab_padre)
        #Se agrega al Nootebook
        tab_padre.add(tab_reconocimiento, text="3. Iniciar reconocimiento")

        #Se agrega el Notebook al frame principal de la ventana
        tab_padre.pack(fill="both", expand=1)

        #Llamar a los otros frames que contienen los widgets para agregarlos al frame_principal
        captura.FrameCapturaImagenes(tab_captura_redimension)
        redimensionar.FrameRedimensionarImagenes(tab_captura_redimension, self.ventana_principal)
        entrenamiento.FrameEntrenamientoRed(tab_entrenamiento, self.ventana_principal)
        reconocimiento.FramePredictor(tab_reconocimiento)

        #pc.ProgressCallback(self.ventana_principal)

        #Pasar ventana padre, para crear ventajas hijas
        #resize.father_window = self.ventana_principal

sis = Sistema()