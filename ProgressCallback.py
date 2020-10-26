#Definir callback personalizado para mostrar
# una salida en cada epoca del entrenamineto de la red
import tflearn as tf
import tkinter as tk
import tkinter.scrolledtext as sc
from tkinter import ttk
import time, sys

class ProgressCallback(tf.callbacks.Callback):
    father_window = None
    current_value = 0

    def __init__(self, fwindow, num_data, num_epoch, n_optimizer):
        self.train_loss = []
        self.father_window = fwindow
        self.total_iter = num_data
        self.epochs = num_epoch
        self.noptimizer = n_optimizer

    def on_train_begin(self, training_state):
        self.create_window()
        self.center_window()
        self.add_widgets()
        #self.child_window.mainloop()
        print("Ventana abierta!")
        self.progress_bar()
        self.child_window.update_idletasks()
        self.child_window.update()

    def on_epoch_begin(self, training_state, logs =None, snapshot=False):
        self.child_window.update_idletasks()
        self.child_window.update()
        #Actulizar la etiqueta con la época actual
        self.var.set("Época del entrenamiento: %d / %d" % (training_state.epoch, self.epochs))
       # print("Inicia - iter : ", training_state.current_iter)
       # type(training_state.current_iter)

    # Actualizar ventana al inicio del batch
    def on_batch_begin(self, training_state):
        self.child_window.update_idletasks()
        self.child_window.update()

    # Actualiza ventana al final del batch
    def on_batch_end(self, training_state, snapshot=False):
        self.child_window.update_idletasks()
        self.child_window.update()

        #Insertar primeros valores del batch -> Step, época, iteracion y total de iteraciones
        self.text_area.insert(tk.END, "\n == Training Step: %d | Epoch: %d -- Iter: %d / %d =="
                                  % (training_state.step, training_state.epoch, training_state.current_iter, self.total_iter))

        #Insertar valores del batch en el textArea: Precisión y pérdida
        self.text_area.insert(tk.END, "\n\t"+self.noptimizer+" | Accuracy: %.4f - Loss: %.4f"
                           % (training_state.acc_value or 0.0, training_state.loss_value or 0.0))

        #Ver ultima linea insertada en el textArea
        self.text_area.see(tk.END)

    # Actualizar ventana al finalizar una época
    def on_epoch_end(self, training_state):
        self.child_window.update_idletasks()
        self.child_window.update()

        self.progress_bar()
        #Insertar validación de precisión y validación de pérdida
        self.text_area.insert(tk.END, "\n\t Validation Accuracy: %.4f - Validation Loss: %.4f"
                              % (training_state.val_acc or 0.0, training_state.val_loss or 0.0))

        #Insertar valores globales: mejor precision, precisión y pérdida
        #self.text_area.insert(tk.END, "\n\t Best Accuracy: %.4f - Global Accuaracy %.4f- Global Loss: %.4f"
        #                      % (training_state.best_accuracy or 0.0, training_state.global_acc or 0.0, training_state.global_loss or 0.0))

        # Ver ultima linea insertada en el textArea
        self.text_area.see(tk.END)

    # Actualizar ventana al finalizar el entrenamiento
    def on_train_end(self, training_state):
        self.child_window.update_idletasks()
        self.child_window.update()

        #Detener el progressbar
        self.stop_bar()
        #Actualizar label
        self.var.set('Entrenamiento finalizado!')
        #Insertar mensaje de que ha terminado el entrenamiento
        self.text_area.insert(tk.END, "\n === El entrenamiento ha tenido éxito, los archivos se "
                                         "han creado correctamente. ===")
        # Ver ultima linea insertada en el textArea
        self.text_area.see(tk.END)

    def create_window(self):
        # Crear ventana hija para mostrar el progreso de la redimensión
        self.child_window = tk.Toplevel(self.father_window)
        # Configurar ventana hija
        self.child_window.title("Entrenando")
        # Centrar ventana hija
        self.center_window()
        # self.child_window.geometry('350x100')
        self.child_window.grab_set()
        self.child_window.transient(self.father_window)
        self.child_window.resizable(width=False, height=False)

    def add_widgets(self):
        self.var = tk.StringVar()
        self.var.set('Entrenando red neuronal')
        # Agregar descripcion
        self.label_description = tk.Label(self.child_window, textvariable=self.var)
        self.label_description.pack()
        # Configurar el progressbar
        self.bar = ttk.Progressbar(self.child_window, length=200, mode="determinate")
        self.bar.pack()
        self.bar['value'] = 0
        self.bar['maximum'] = self.epochs

        #Agregar scrolledText para mostrar las epocas del entrenamiento
        self.text_area = sc.ScrolledText(self.child_window, width=100, height=12,
                                         font=("Times New Roman", 10))
        self.text_area.pack(pady=10, padx=20)
        self.text_area.insert(tk.INSERT, "Iniciando...")
        #self.text_area.config(state="disabled")

        # Agregar botón para cancelar la redimensión
        self.button_cancel = tk.Button(self.child_window, text="Cancelar", command=self.cancel)
        self.button_cancel.config(font=("Arial", 10, "bold"))
        self.button_cancel.pack(pady=10)

    def center_window(self):
        # Dimensiones de la ventana hija
        w = 550
        h = 300
        # Determinar la anchira y longitud de la pantalla
        sw = self.child_window.winfo_screenwidth()
        sh = self.child_window.winfo_screenheight()
        # Calcular las coordenadas x / y
        x = (sw - w) / 2
        y = (sh - h) / 2
        # Dar dimensiones y ubicacion a la ventana
        self.child_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def progress_bar(self):
        self.current_value+=1
        self.bar['value'] = self.current_value
        #self.bar.start(50)

    # Detener el progressbar
    def stop_bar(self):
        self.bar.stop()
        self.bar['value'] = 100

    def cancel(self):
        # Destruir la ventana
        self.child_window.destroy()
        raise StopIteration
