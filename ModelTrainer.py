import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from sklearn.utils import shuffle
import cv2, sys

#Clase para el entrenamiendo del modelo de red
class ModelTrainer:
 #   model = None
 #   loadedImages = []
 #   outputVectors = []
 #   testImages = []
#    testLabels = []

    def __init__(self, list_dat, name, path_s):
        self.list_data = list_dat
        self.name_model = name
        self.path_save = path_s
        self.carga_imagenes()
        self.output_vector()
        self.pruebas_carga_vector()
        self.modelo_cnn()
        self.reorganizacion()

    #Carga de las imagenes a partir de ubicaciones
    def carga_imagenes(self):
        self.loadedImages = []
        try:
            for item in self.list_data:
                #Obtener de cada item el valor que contiene la ruta
                path = item[1] # item(nombre_de_gesto, ruta_de_gesto, ruta_test)
                #carga de las imagenes desde la ruta de cada item
                for i in range(0, 1000):
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
            #Asignar 1 a la posición i, los demás elementos de objeto serán 0's
            n[i] = 1
            for j in range(0, 1000):
                #Agregar el objeto al vector
                self.outputVectors.append(n)
            #Reasignar 0 a la posición i del objeto n
            n[i] = 0


    #Realizar pruebas con carga de imagenes  de testeo y etiquetado
    def pruebas_carga_vector(self):
        self.testImages =[]
        for item in self.list_data:
            # Obtener de cada item el valor que contiene la ruta
            path_test = item[2]  # item(nombre_de_gesto, ruta_de_gesto, ruta_test)
            # carga de las imagenes desde la ruta de cada item
            for i in range(0, 100):
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
            #Asignar 1 a la posición i, los demás elementos de objeto serán 0's
            n[i] = 1
            for j in range(0, 100):
                #Agregar el objeto al vector de etiquetas
                self.testLabels.append(n)
            #Reasignar 0 a la posición i del objeto n
            n[i] = 0

    #Definir el modelo CNN
    def modelo_cnn(self):
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

        convnet = regression(convnet, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy',
                              name='regression')

        self.model = tflearn.DNN(convnet, tensorboard_verbose=0)

    # Reorganizar datos de entrenamiento
    def reorganizacion(self):

        self.loadedImages, self.outputVectors = shuffle(self.loadedImages, self.outputVectors, random_state=0)

        # Train model
        self.model.fit(self.loadedImages, self.outputVectors, n_epoch=50,
                       validation_set=(self.testImages, self.testLabels),
                       snapshot_step=100, show_metric=True, run_id='convnet_coursera')

        #Guardar modelo
        self.model.save(self.path_save+"\\"+self.name_model+".tfl")
