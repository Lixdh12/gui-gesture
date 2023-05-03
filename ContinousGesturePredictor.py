import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
import cv2, imutils

class ContinuousGesturePredictor:
    bg = None
    basewidth = 100
    model = None
    camera = None

    def __init__(self, file_model, list_data, num_ent_img, num_val_img,size_w, size_h):
        self.file_model = file_model
        self.list_data = list_data
        self.num_ent_img = num_ent_img
        self.num_val_img = num_val_img
        self.size_w = size_w
        self.size_h = size_h
        self.model = self.definirModelo()
        self.main()
        #Liberar memoria de la cámara
        self.free_memory_c()


    def configurarImagen(self, imageName):
        #Se abre la imagen con el nombre respectivo
        img = Image.open(imageName)
        #Porcentaje del ancho, entre valor default del ancho de la imagen y el real
        #wpercent = (self.basewidth / float(img.size[0]))
        #Obtener el tamaño de la altura, img.size[1] -> altura de la imagen
        #hsize = int((float(img.size[1]) * float(wpercent)))
        #Devuelve una copia redimensionada de la imagen
        img = img.resize((self.size_w, self.size_h), Image.ANTIALIAS)
        #Guarda esta imagen con el nombre de archivo dado
        img.save(imageName)

    def run_avg(self, image, aWeight):
        # Inicializar el background
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        # Calcular el promedio ponderado, acumularlo y actualizar el background
        cv2.accumulateWeighted(image, self.bg, aWeight)

    def segment(self, image, threshold=25 ):
        # Encontrar las diferencias absolutas entre el backgroud y el frame actual
        diff = cv2.absdiff(self.bg.astype("uint8"), image)

        # Obtener el umbral de la imagen
        thresholded = cv2.threshold(diff,
                                    threshold,
                                    255,
                                    cv2.THRESH_BINARY)[1]

        # Obtener los contornos del umbral
        (_, cnts, _) = cv2.findContours(thresholded.copy(),
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # En caso de no detectar contornos, return None
        if len(cnts) == 0:
            return
        else:
            # Obtener el contorno máximo
            segmented = max(cnts, key=cv2.contourArea)
            return (thresholded, segmented)

    def main(self):
        # inicializar peso
        aWeight = 0.5

        # Obtener referencia de la camara web
        self.camera = cv2.VideoCapture(0)

        # Coordenadas de la region de interes(ROI)
        top, right, bottom, left = 10, 350, 225, 590

        # Numero de frames
        num_frames = 0
        start_recording = False

        #
        while (True):
            # Obtener el frame actual
            (grabbed, frame) = self.camera.read()

            # Redimensionar frame
            frame = imutils.resize(frame, width=700)

            # Voltea el frame para que no sea la vista del espejo
            frame = cv2.flip(frame, 1)

            # Clonar el frame
            clone = frame.copy()

            # Obtener dimensiones del frame
            (height, width) = frame.shape[:2]

            # Obtener el ROI
            roi = frame[top:bottom, right:left]

            # convertir el ROI a escala grises
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            # Para obtener el background, buscar hasta alcanzar un umbral
            # para calibrar el modelo
            if num_frames < 30:
                self.run_avg(gray, aWeight)
            else:
                # Segmentar la imagen
                hand = self.segment(gray)

                # Revisar si se segmentó correctamente
                if hand is not None:
                    # Descomprimir la imagen con el umbral y la región segmentada
                    (thresholded, segmented) = hand

                    # Dibujar la región segmentada y mostrar el frame
                    cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                    if start_recording:
                        cv2.imwrite('Temp.png', thresholded)
                        self.configurarImagen('Temp.png')
			#Predecir clase de la imagen
                        predictedClass, confidence = self.getPredictedClass()
                        #Mostrar porcentaje de predicción de la clase
			self.showStatistics(predictedClass, confidence)
                    cv2.imshow("Thesholded", thresholded)

            # Dibujar la región segmentada
            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

            # Incrementar núm de frames
            num_frames += 1

            # Mostrar el frame y la región segmentada
            cv2.imshow("Video Feed", clone)

            # Espera de tecleo
            keypress = cv2.waitKey(1) & 0xFF

            # Si el usuario teclea "q", se detendrá
            if keypress == ord("q"):
                break

            if keypress == ord("s"):
                start_recording = True

    def getPredictedClass(self):
        sum_prediction = 0
        # Predicción
        image = cv2.imread('Temp.png')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        prediction = self.model.predict([gray_image.reshape(self.size_h, self.size_w, 1)])

        #print(prediction)

        #Obtener la suma de todos los elementos de prediction, teniendo en cuenta
        #  que tiene el mismo tamaño que la lista de datos
        for i in range(0, len(self.list_data)):
            sum_prediction = sum_prediction + prediction[0][i]

    #    return np.argmax(prediction), (np.amax(prediction) / (prediction[0][0] + prediction[0][1] + prediction[0][2]))
        return np.argmax(prediction), (np.amax(prediction) / sum_prediction)

    def showStatistics(self, predictedClass, confidence):

        textImage = np.zeros((300, 512, 3), np.uint8)
        className = ""

        # if predictedClass == 0:
        #     className = "Swing"
        # elif predictedClass == 1:
        #     className = "Palm"
        # elif predictedClass == 2:
        #     className = "Fist"

        #Obtener los nombres de los gestos, y clasificar
        for i in range(0, len(self.list_data)):
            #Si el valor de predictedClass es igual al indice de la lista
            if i == predictedClass:
                #Asignar el nombre del gesto a la variable className
                className = self.list_data[i][0]

        cv2.putText(textImage, "Clase: " + className,
                    (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        cv2.putText(textImage, "Confianza: " + str(confidence * 100) + '%',
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)
        cv2.imshow("Statistics", textImage)

    def definirModelo(self):
        # Definir el modelo de red neuronal
        tf.reset_default_graph()
        convnet = input_data(shape=[None, self.size_h, self.size_w, 1], name='input')
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

        convnet = fully_connected(convnet, self.num_ent_img, activation='relu')
        convnet = dropout(convnet, 0.75)

        convnet = fully_connected(convnet, len(self.list_data), activation='softmax')

        convnet = regression(convnet, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy',
                             name='regression')

        self.model = tflearn.DNN(convnet, tensorboard_verbose=0)

        #obtener string del nombre del archivo
        name_file = self.file_model.split('.')

        # Cargar modelo
        self.model.load(name_file[0]+'.tfl',weights_only=True)

        return self.model
    #Liberar memoria
    def free_memory_c(self):
        self.camera.release()
        cv2.destroyAllWindows()
        del self.camera
