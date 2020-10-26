import ProgressCallback as pc
import tkinter as tk
from tkinter import ttk
import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from sklearn.utils import shuffle
import cv2, sys, time

#Clase para el entrenamiendo del modelo de red
class ModelTrainer:
 #   model = None
 #   loadedImages = []
 #   outputVectors = []
 #   testImages = []
#    testLabels = []

    def __init__(self, list_dat, name, path_s, f_window):
        self.father_window = f_window
        self.list_data = list_dat
        self.name_model = name
        self.path_save = path_s

        #Crear la ventana
        self.creacion_ventana()


        self.carga_imagenes()
        self.output_vector()
        self.pruebas_carga_vector()
        self.modelo_cnn()

        #Parar bar
        self.stop_progress()

        self.reorganizacion()



    #Carga de las imagenes a partir de ubicaciones
    def carga_imagenes(self):
        self.loadedImages = []
        try:
            # Inciar bar
            self.start_progress()
            for item in self.list_data:
                #Obtener de cada item el valor que contiene la ruta
                path = item[1] # item(nombre_de_gesto, ruta_de_gesto, ruta_test)
                #carga de las imagenes desde la ruta de cada item
                for i in range(0, 1000):
                    # Actualizar ventana hija
                    self.child_window.update_idletasks()
                    self.child_window.update()
                   #Obtener las imagenes
                    image = cv2.imread(path+'\\gest_' + str(i) + '.png')
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    self.loadedImages.append(gray_image.reshape(89, 100, 1))

        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])

    #Create OutputVector
    def output_vector(self):
        self.outputVectors = []
        #Obtener la longitud de la lista de los datos
        length_data = len(self.list_data)
        #lista
        n = []
        #Agregar elemento 0 de acuerdo a la longitud de los datos
        for i in range(0, length_data):
            n.append(0)

        for i in range(0,length_data):
            # Reasignar 0 a la posición i del objeto n
            if i > 0:
                n[i - 1] = 0
            #Asignar 1 a la posición i, los demás elementos de objeto serán 0's
            n[i] = 1
            #Copiar la lista a una nueva variable
            new_list = n.copy()
            for j in range(0, 1000):
                # Actualizar ventana hija
                self.child_window.update_idletasks()
                self.child_window.update()
                #Agregar el objeto al vector
                self.outputVectors.append(new_list)
            #Reasignar 0 a la posición i del objeto n
            #n[i] = 0

    #Realizar pruebas con carga de imagenes  de testeo y etiquetado
    def pruebas_carga_vector(self):
        self.testImages =[]
        for item in self.list_data:
            # Obtener de cada item el valor que contiene la ruta
            path_test = item[2]  # item(nombre_de_gesto, ruta_de_gesto, ruta_test)
            # carga de las imagenes desde la ruta de cada item
            for i in range(0, 100):
                #Actualizar ventana hija
                self.child_window.update_idletasks()
                self.child_window.update()

                image = cv2.imread(path_test + '\\gest_' + str(i) + '.png')
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                self.testImages.append(gray_image.reshape(89, 100, 1))


        self.testLabels = []
        #Obtener la longitud de la lista de los datos
        self.length_data = len(self.list_data)
        #lista
        n = []
        #Agregar elemento 0 de acuerdo a la longitud de los datos
        for i in range(0, self.length_data):
            n.append(0)

        for i in range(0,self.length_data):
            # Reasignar 0 a la posición i del objeto n
            if i > 0:
                n[i - 1] = 0
            #Asignar 1 a la posición i, los demás elementos de objeto serán 0's
            n[i] = 1
            #Crear una copia de la lista
            new_list = n.copy()
            for j in range(0, 100):
                # Actualizar ventana hija
                self.child_window.update_idletasks()
                self.child_window.update()

                #Agregar el objeto al vector de etiquetas
                self.testLabels.append(new_list)
            #Reasignar 0 a la posición i del objeto n
            #n[i] = 0

    #Definir el modelo CNN
    def modelo_cnn(self):
        self.child_window.update_idletasks()
        self.child_window.update()
        self.name_optimizer = 'adam'
        tf.reset_default_graph()
        convnet = input_data(shape=[None, 89, 100, 1], name='input')
        convnet = conv_2d(convnet, 32, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        convnet = conv_2d(convnet, 64, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)

        convnet = conv_2d(convnet, 128, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)

        convnet = conv_2d(convnet, 256, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)

        convnet = conv_2d(convnet, 256, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)

        convnet = conv_2d(convnet, 128, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)

        convnet = conv_2d(convnet, 64, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)

        convnet = fully_connected(convnet, 1000, activation='relu')
        convnet = dropout(convnet, 0.75)

        convnet = fully_connected(convnet, self.length_data, activation='softmax')

        convnet = regression(convnet, optimizer=self.name_optimizer, learning_rate=0.001, loss='categorical_crossentropy',
                              name='regression')

        self.model = tflearn.DNN(convnet, tensorboard_verbose=0)

    # Reorganizar datos de entrenamiento
    def reorganizacion(self):

        self.loadedImages, self.outputVectors = shuffle(self.loadedImages, self.outputVectors, random_state=0)

        #Calcular el numero de iteraciones para el entrenamiento, la longitud de los datos por numero de unidades
        # en la capa fully_connected (int), por default 1000
        num_iter = self.length_data * 1000
        num_epoch = 50

        try:
            # Train model
            self.model.fit(self.loadedImages, self.outputVectors, n_epoch = num_epoch,
                           validation_set=(self.testImages, self.testLabels),
                           snapshot_step=100,show_metric=True, run_id='convnet_coursera',
                           # Llamar a la clase ProgressCallback, previamente personalizada
                           callbacks=pc.ProgressCallback(self.father_window, num_iter, num_epoch, self.name_optimizer))
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])

        #Guardar modelo
        self.model.save(self.path_save+"\\"+self.name_model+".tfl")

#######################################################
#### CREACION DE LA VENTANA HIJA
    def creacion_ventana(self):
        print("abrir ventana")
        # Crear ventana hija para mostrar el progreso de la redimensión
        self.child_window = tk.Toplevel(self.father_window)
        # Configurar ventana hija
        self.child_window.title("Cargando imágenes")
        # Centrar ventana hija
        self.centrar_ventana()
        # self.child_window.geometry('350x100')
        self.child_window.grab_set()
        self.child_window.transient(self.father_window)
        self.child_window.resizable(width=False, height=False)
        #Agregar widgets
        self.agregar_widgets()

    def centrar_ventana(self):
        #Dimensiones de la ventana
        w = 350
        h = 100
        #Determinar la anchira y longitud de la pantalla
        sw = self.child_window.winfo_screenwidth()
        sh = self.child_window.winfo_screenheight()
        #Calcular las coordenadas x / y
        x = (sw-w)/2
        y = (sh-h)/2
        #Dar dimensiones y ubicacion a la ventana
        self.child_window.geometry('%dx%d+%d+%d'% (w,h,x,y))

    def agregar_widgets(self):
        self.var = tk.StringVar()
        self.var.set('Cargando imágenes, espere.')
        # Agregar descripcion
        label_description = tk.Label(self.child_window, textvariable=self.var)
        label_description.pack()
        # Configurar el progressbar
        self.bar = ttk.Progressbar(self.child_window, length=200, mode="indeterminate")
        self.bar.pack()
        self.bar['value'] = 0
        self.bar['maximum'] = 100

        self.var_button = tk.StringVar()
        self.var_button.set('Cancelar')

        # Agregar botón para cancelar la redimensión
        self.button_cancel = tk.Button(self.child_window, textvariable=self.var_button, command=self.salir)
        self.button_cancel.config(font=("Arial", 10, "bold"))
        self.button_cancel.pack(pady=10)


    def salir(self):
        # Destruir la ventana
        self.child_window.destroy()
        raise StopIteration

    def start_progress(self):
        self.bar.start(30)
        #self.bar['value'] = current_value

    def stop_progress(self):
        self.bar.stop()
        self.bar.config(mode="determinate")
        self.bar['value'] = 100
        self.var.set('Imágenes cargadas, espere')
        time.sleep(3)
        self.child_window.destroy()