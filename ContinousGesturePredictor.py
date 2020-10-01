import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
import cv2
import imutils

class ContinuousGesturePredictor:
    bg = None
    basewidth = 100
    model = None

    def __init__(self, file_model, list_data):
        self.file_model = file_model
        self.list_data = list_data
        print(self.list_data)
        self.model = self.definirModelo()
        self.main()

    def configurarImagen(self, imageName):
        #Se abre la imagen con el nombre respectivo
        img = Image.open(imageName)
        #Porcentaje del ancho, entre valor default del ancho de la imagen y el real
        wpercent = (self.basewidth / float(img.size[0]))
        #Obtener el tamaño de la altura, img.size[1] -> altura de la imagen
        hsize = int((float(img.size[1]) * float(wpercent)))
        #Devuelve una copia redimensionada de la imagen
        img = img.resize((self.basewidth, hsize), Image.ANTIALIAS)
        #Guarda esta imagen con el nombre de archivo dado
        img.save(imageName)

    def run_avg(self, image, aWeight):
        # global bg
        # inicializar el background
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        # calcular el promedio ponderado, acumularlo y actualizar el background
        cv2.accumulateWeighted(image, self.bg, aWeight)

    def segment(self, image, threshold=25 ):
        #global bg
        # Encontrar las diferencias absolutas entre el backgroud y el actual frame
        # find the absolute difference between background and current frame
        diff = cv2.absdiff(self.bg.astype("uint8"), image)

        # threshold the diff image so that we get the foreground
        thresholded = cv2.threshold(diff,
                                    threshold,
                                    255,
                                    cv2.THRESH_BINARY)[1]

        # get the contours in the thresholded image
        (_, cnts, _) = cv2.findContours(thresholded.copy(),
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # return None, if no contours detected
        if len(cnts) == 0:
            return
        else:
            # based on contour area, get the maximum contour which is the hand
            segmented = max(cnts, key=cv2.contourArea)
            return (thresholded, segmented)

    def main(self):
        # initialize weight for running average
        aWeight = 0.5

        # get the reference to the webcam
        camera = cv2.VideoCapture(0)

        # region of interest (ROI) coordinates
        top, right, bottom, left = 10, 350, 225, 590

        # initialize num of frames
        num_frames = 0
        start_recording = False

        # keep looping, until interrupted
        while (True):
            # get the current frame
            (grabbed, frame) = camera.read()

            # resize the frame
            frame = imutils.resize(frame, width=700)

            # flip the frame so that it is not the mirror view
            frame = cv2.flip(frame, 1)

            # clone the frame
            clone = frame.copy()

            # get the height and width of the frame
            (height, width) = frame.shape[:2]

            # get the ROI
            roi = frame[top:bottom, right:left]

            # convert the roi to grayscale and blur it
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            # to get the background, keep looking till a threshold is reached
            # so that our running average model gets calibrated
            if num_frames < 30:
                self.run_avg(gray, aWeight)
            else:
                # segment the hand region
                hand = self.segment(gray)

                # check whether hand region is segmented
                if hand is not None:
                    # if yes, unpack the thresholded image and
                    # segmented region
                    (thresholded, segmented) = hand

                    # draw the segmented region and display the frame
                    cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                    if start_recording:
                        cv2.imwrite('Temp.png', thresholded)
                        self.configurarImagen('Temp.png')
                        predictedClass, confidence = self.getPredictedClass()
                        self.showStatistics(predictedClass, confidence)
                    cv2.imshow("Thesholded", thresholded)

            # draw the segmented hand
            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

            # increment the number of frames
            num_frames += 1

            # display the frame with segmented hand
            cv2.imshow("Video Feed", clone)

            # observe the keypress by the user
            keypress = cv2.waitKey(1) & 0xFF

            # if the user pressed "q", then stop looping
            if keypress == ord("q"):
                break

            if keypress == ord("s"):
                start_recording = True

    def getPredictedClass(self):
        sum_prediction = 0
        # Predict
        image = cv2.imread('Temp.png')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        prediction = self.model.predict([gray_image.reshape(89, 100, 1)])

        print(prediction)

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

        cv2.putText(textImage, "Pedicted Class : " + className,
                    (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        cv2.putText(textImage, "Confidence : " + str(confidence * 100) + '%',
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)
        cv2.imshow("Statistics", textImage)

    def definirModelo(self):
        # Model defined
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

        convnet = fully_connected(convnet, len(self.list_data), activation='softmax')

        convnet = regression(convnet, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy',
                             name='regression')

        self.model = tflearn.DNN(convnet, tensorboard_verbose=0)

        #obtener string del nombre del archivo
        name_file = self.file_model.split('.')

        # Load Saved Model
        self.model.load(name_file[0]+'.tfl',weights_only=True)

        return self.model
