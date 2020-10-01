import tkinter as tk
from tkinter import ttk
from PIL import Image
from tkinter import messagebox
import sys, time

class ResizeImages:
    basewidth = 100

    def __init__(self,carpeta, pixW, pixH, numC, f_window):
        self.directorio = carpeta
        self.pixel_width = pixW
        self.pixel_heigth = pixH
        self.num_capture = numC
        self.father_window = f_window

        #Crear ventana hija para mostrar el progreso de la redimensión
        self.child_window = tk.Toplevel(self.father_window)
        #Configurar ventana hija
        self.child_window.title("Recortando")
        #Centrar ventana hija
        self.centrar_ventana()
        #self.child_window.geometry('350x100')
        self.child_window.grab_set()
        self.child_window.transient(self.father_window)
        self.child_window.resizable(width=False, height=False)

        #Agregar descripcion
        label_description = tk.Label(self.child_window,text="Recortando imagenes, espere.")
        label_description.pack()
        #Configurar el progressbar
        self.bar = ttk.Progressbar(self.child_window, length=200, mode="determinate")
        self.bar.pack()
        self.bar['value'] = 0
        self.bar['maximum'] = 100

        #Agregar botón para cancelar la redimensión
        self.button_cancel = tk.Button(self.child_window, text="Cancelar", command=self.cancel)
        self.button_cancel.config(font=("Arial", 10, "bold"))
        self.button_cancel.pack(pady=10)
        self.main()

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

    def progress(self, current_value):
        self.bar['value'] = current_value

    def cancel(self):
        # Destruir la ventana
        self.child_window.destroy()

    def main(self):
        value = 0
        try:
            for i in range(0, self.num_capture):
                #Calcular el valor del proceso basado en un 100%
                value = (i*100)/self.num_capture
                #Mostrar el porcentaje en el progressbar
                self.bar.after(500,self.progress(value))
                self.bar.update()
                #Redimensionar las imagenes
                self.configurarImagen(self.directorio+"\\gest_" + str(i) + '.png')
            #Destruir la ventana
            self.child_window.destroy()
            #Cuando la redimensión termine y termine exitosamente, se mostrará un mensaje
            messagebox.showinfo("Éxito", "La redimensión de imágenes ha sido un éxto.")
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            #En caso de una excepción se mostrará un mensaje de error
            messagebox.showerror("Error", "No se ha podido completar el proceso, intenta de nuevo")

    def configurarImagen(self, imageName):
        #Se abre la imagen con el nombre respectivo
        img = Image.open(imageName)
        #Porcentaje del ancho, entre valor default del ancho de la imagen y el real
        wpercent = (self.basewidth / float(img.size[0]))
        #Obtener el tamaño de la altura, img.size[1] -> altura de la imagen
        hsize = int((float(img.size[1]) * float(wpercent)))
        #Devuelve una copia redimensionada de la imagen
        #img = img.resize((self.basewidth, hsize), Image.ANTIALIAS)
        img = img.resize((self.pixel_width, self.pixel_heigth), Image.ANTIALIAS)
        #Guarda esta imagen con el nombre de archivo dado
        img.save(imageName)