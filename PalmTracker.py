# organizar librerías
import cv2
import imutils
from tkinter import messagebox
import numpy as np

class PalmTracker:
    bg = None
    camera = None

    def __init__(self,carpeta, nums_img):
        self.directorio = carpeta
        self.num_capture = nums_img

    def run_avg(self, image, aWeight):
        #inicializar el background
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        #calcular el promedio ponderado, acumularlo y actualizar el background
        cv2.accumulateWeighted(image, self.bg, aWeight)

    def segment(self, image, threshold=25 ):
        #global bg
        # Encontrar las diferencias absolutas entre el backgroud y el actual frame
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


        # Obtener referencia de la webcam
        self.camera = cv2.VideoCapture(0)

        # Coordenadas de la region de interes(ROI)
        top, right, bottom, left = 10, 350, 225, 590

        # Numero de frames
        num_frames = 0
        image_num = 0

        start_recording = False

        
        while (True):
            # Obtener el frame actual
            (grabbed, frame) = self.camera.read()
            if (grabbed == True):

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

                # Convertir el ROI a escala grises
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (7, 7), 0)

                # para obtener el fondo, siga buscando hasta que se alcance un umbral
                #  para que nuestro modelo promedio de funcionamiento se calibre
                if num_frames < 30:
                    self.run_avg(gray, aWeight)
                    #print(num_frames)
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
                            # Ruta donde se almacenará las imagenes
                            cv2.imwrite(self.directorio+"\\"+"gest_" + str(image_num) + '.png', thresholded)
                            image_num += 1

                        cv2.putText(thresholded,"No. capturas: " + str(image_num), (20, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.imshow("Thresholded", thresholded)


                # Dibujar la región segmentada
                cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

                # Incrementar núm de frames
                num_frames += 1

                # Mostrar el frame y la región segmentada
                cv2.imshow("Video Feed", clone)

                # Espera de tecleo
                keypress = cv2.waitKey(1) & 0xFF

                # Si se teclea "q", entonces se detendrá el ciclo o hasta que se tomen n imagenes
                if keypress == ord("q"):
                    break

                if image_num > self.num_capture:
                    # Mensaje informativo
                    messagebox.showinfo("Éxito", "Captura realizada con éxito!")
                    break

                if keypress == ord("s"):
                    start_recording = True

                #Si teclea "p" se pausará la captura de imagenes
                if keypress == ord("p"):
                    start_recording = False

            else:
                print("[Warning!] Error input, Please check your(camara Or video)")
                break