import tkinter as tk
import tkinter.ttk as ttk
import pickle as pickle
import ModelTrainer as trainer
from tkinter import filedialog
from tkinter import messagebox
import os, sys

#Clase para crear el frame de la sección ENTRENAMIENTO DE LA RED
class FrameEntrenamientoRed(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.config(width=617, height=173,relief=tk.GROOVE, borderwidth=1)
        self.pack(fill="both", expand=1, padx=10, pady=10)
        self.crear_widgets()

    #Crear widgets de la sección y agregarlos
    def crear_widgets(self):
        # Titulo de la sección contenido en una etiqueta (Label)
        label_title = tk.Label(self, text="Entrenamiento de la red")
        # Configurar el formato del texto en la etiqueta
        label_title.config(font=("Arial", 14))
        # Colocar la etiqueta en el frame correspondiente
        label_title.place(x=40, y=5)

        ####### 1era PARTE DE LA SECCIÓN
        #Frame para la primera parte de la sección
        frame_part1 = tk.Frame(self,width=595, height=240,relief=tk.GROOVE, borderwidth=1)
        frame_part1.place(x=20, y=40)

        #Botón para importar un archivo con el listado de gestos
        button_import_gest = tk.Button(frame_part1, text="Importar gestos", width=15, command=self.importar_archivo)
        button_import_gest.place(x=50, y=10)

        #Botón para exportar un archivo con el listado de gestos que se está mostrando
        button_export_gest = tk.Button(frame_part1,text="Exportar gestos", width=15, command=self.exportar_archivo)
        button_export_gest.place(x=250, y=10)

        #Campos para ingresar un nuevo gesto
        #Etiqueta para indicar el campo del NOMBRE del gesto
        self.label_name_gest = tk.Label(frame_part1, text="Nombre:")
        self.label_name_gest.place(x=20, y=50)

        # Variables para asociar con las cajas de texto, ya que se estará cambiando su contenido
        self.name_string = tk.StringVar()
        self.path_string = tk.StringVar()
        self.path_test = tk.StringVar()

        #Caja de texto para el ingreso de caracteres que será el nombre del gesto a ingresar a la lista
        self.textbox_name_gest = tk.Entry(frame_part1, width=20, textvariable=self.name_string)
        self.textbox_name_gest.place(x=75, y=50)

        #Etiqueta para indicar el campo de la RUTA de la carpeta que contiene las imagenes del gesto
        self.label_path_gest = tk.Label(frame_part1, text="Carpeta:")
        self.label_path_gest.place(x=210, y=50)

        #Caja de texto para la selección de la ruta de la carpeta contenedora de las imagenes
        self.textbox_path_gest = tk.Entry(frame_part1, width=38, textvariable=self.path_string, state="disabled")
        self.textbox_path_gest.place(x=260, y=50)

        #Botón para seleccionar la carpeta contedora de las imagenes
        self.button_path_gest = tk.Button(frame_part1, text="Seleccionar",
                                command=self.seleccionar_carpeta)
        # Colocar el botón en el frame correspondiente
        self.button_path_gest.place(x=500, y=45)

        #Etiqueta que indica la ruta donde se encuentra la carpeta de prueba
        self.label_path_test = tk.Label(frame_part1, text="Carpeta de prueba:")
        self.label_path_test.place(x=20, y=75)

        #Caja de texto para la selección de la ruta de la carpeta contenedora de las imagenes prueba
        self.textbox_path_test = tk.Entry(frame_part1, width=38, textvariable=self.path_test, state="disabled")
        self.textbox_path_test.place(x=130, y=75)

        #Botón para seleccionar la carpeta contenedor de las imagenes prueba
        self.button_path_test = tk.Button(frame_part1, text="Seleccionar", command=self.seleccionar_carpeta_test)
        self.button_path_test.place(x=370, y=70)

        #Botón para agregar un nuevo gesto a la lista
        self.button_new_gest = tk.Button(frame_part1, text="Agregar gesto", width=15, command=self.agregar_gesto)
        self.button_new_gest.place(x=425, y=120)

        #Botón para actualizar un gesto seleccionado de la lista
        self.button_update_gest = tk.Button(frame_part1, text="Actualizar gesto", state="disabled",
                                            width=15, command=self.actualizar_gesto)
        self.button_update_gest.place(x=425, y=160)

        #Botón para elimianr un gesto seleccionado de la lista
        self.button_delete_gest = tk.Button(frame_part1, text="Eliminar gesto", state="disabled",
                                            width=15, command=self.eliminar_gesto)
        self.button_delete_gest.place(x=425, y=200)

        #Treeview para mostrar una lista de gestos
        #Frame para contener el treeview
        frame_list = tk.Frame(frame_part1, width=200, height=100,relief=tk.RAISED)
        frame_list.place(x=10, y=100)
        #Agregar al frame dos scroll: vertical y horizontal
        scrollbary = ttk.Scrollbar(frame_list, orient="vertical")
        scrollbarx = ttk.Scrollbar(frame_list, orient="horizontal")
        #Crear el treeview con sus respectivas columnas
        self.tree_list = ttk.Treeview(frame_list, columns=("NombreGesto", "Ruta", "RutaPrueba"),
                            selectmode="extended", height=4,yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set)
        #Se habulitarán los scroll cuando los elementos del treeview no tengan suficiente visibilidad
        scrollbary.config(command=self.tree_list.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.tree_list.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        #Nombrar los encabezados de acuerdo al identificador de las columnas anteriormente definidas
        self.tree_list.heading('NombreGesto', text="Nombre de gesto", anchor=tk.W)
        self.tree_list.heading('Ruta', text="Ruta", anchor=tk.W)
        self.tree_list.heading('RutaPrueba', text="Ruta de prueba", anchor=tk.W)
        #Configurar las columnas
        self.tree_list.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree_list.column('NombreGesto', stretch=tk.NO, minwidth=0, width=100)
        self.tree_list.column('Ruta', stretch=tk.NO, minwidth=0, width=150)
        self.tree_list.column('RutaPrueba', stretch=tk.NO, minwidth=0, width=150)
        #Crear etiqueta para el widget tree_list, y de esa manera identificar el evento en los items
        self.tree_list.tag_bind("tag_tree_list","<<TreeviewSelect>>",self.seleccionar_item)
        self.tree_list.pack()

        ####### 2da PARTE DE LA SECCIÓN
        #Frame que contendrá la  2da parte de la sección
        frame_part2 = tk.Frame(self,width=595, height=135,relief=tk.GROOVE, borderwidth=1)
        frame_part2.place(x=20, y=285)

        #Etiqueta para el campo del nombre del modelo
        label_model_name = tk.Label(frame_part2, text="Nombre del modelo de la red:")
        label_model_name.place(x=10, y=20)

        #Caja de texto para el campo del nombre del modelo
        self.textbox_model_name = tk.Entry(frame_part2, width=25)
        self.textbox_model_name.place(x=180, y=20)

        #Etiqueta que indica el formato del archivo a crear
        label_format = tk.Label(frame_part2, text=".tfl")
        label_format.place(x=340, y=20)

        #Etiqueta para indicar el campo de la ruta
        label_path = tk.Label(frame_part2, text="Guardar el modelo en:")
        label_path.place(x=10, y=70)

        #Caja de texto para la ruta seleccionada
        self.textbox_path_save = tk.Entry(frame_part2, width=45)
        # Se deshabilita, por lo que el usuario tendrá que elegir la ruta de una carpeta
        self.textbox_path_save.config(state="disabled")
        # Colocar la caja de texto en el frame correspondiente
        self.textbox_path_save.place(x=140, y=70)

        # Botón para la selección de la ruta que guardará el archivo del modelo
        button_path_save = tk.Button(frame_part2, text="Guardar como", command=self.guardar_como)
        # Colocar el botón en el frame correspondiente
        button_path_save.place(x=420, y=65)

        #Bitón para iniciar el entrenamiento del modelo de acuerdo con los gestos en la lista
        button_training = tk.Button(frame_part2, text="Entrenar red", command=self.inicio_entrenamiento)
        # Configurar el formato del botón
        button_training.config(font=("Arial", 10, "bold"))
        button_training.place(x=250, y=100)

    #Elegir archivo desde el explorador de archivos y obtener los datos
    def importar_archivo(self):
        try:
            #Abrir el explorador de archivos para la selección de un archivo
            open_file = filedialog.askopenfilename(initialdir="/", title="Seleccione archivo",
                                                filetypes=[("Archivos pickle","*.pickle"),("Todos los archivos","*")])
            #Abrir el archivo
            file_data = open(open_file, "rb")
            #Obtener los datos
            data_list = pickle.load(file_data)
            #Cerrar el archivo
            file_data.close()
            #Carga de los datos del archivo
            self.carga_lista(data_list)
        except:
            #Mensaje de error
            messagebox.showerror("Error", "Error al importar el archivo")

    #Cargar datos en la lista
    def carga_lista(self, data):
        try:
            # Si hay elementos en la lista, limpiarla, y colocar los nuevos elementos
            if self.tree_list.get_children():
                # Se obtienen los id's de todos los items que se encuentran en la lista
                ids_items = self.tree_list.get_children()
                # Por cada id se obtienen los valores de cada item
                for id_item in ids_items:
                    self.tree_list.delete(id_item)
            #Insertar cada nuevo elemento en la lista con los valores respectivamente
            for item in data:
                 self.tree_list.insert('', 'end', values=(item[0], item[1], item[2]),
                                          tag=("tag_tree_list",))
        except:
            #Mensaje de error
            messagebox.showerror("Error", "Error al cargar los datos en la lista")

    #Creación de archivo con la serialización de datos que contiene la lista
    def exportar_archivo(self):
        obj_items = []
        # Se obtienen los id's de todos los items que se encuentran en la lista
        ids_items = self.tree_list.get_children()
        if len(ids_items) > 0:
            # Por cada id se obtienen los valores de cada item
            for id_item in ids_items:
                #Se agrega valores de cada item a una lista
                obj_items.append(self.tree_list.item(id_item, option="values"))

            try:
                # Abrir explorador de archivos para preguntar nombre y la ubicación en que se desea guardar
                save_file = filedialog.asksaveasfilename(initialdir="/", title="Guardar como",
                                                         defaultextension=".pickle",
                                                         filetypes=[("Archivos pickle", "*.pickle"),
                                                                    ("Todos los archivos", "*")])
                #Creación del archivo binario, abrirlo en modo escritura binaria
                file_data =open(save_file,"wb")
                #Usar función de pickle para la serialización y escribir en el archivo
                pickle.dump(obj_items, file_data)
                #Cerrar el archivo
                file_data.close()
                #Borra el puntero de la memoria hacia la variable
                del file_data
                #Mensaje informativo
                messagebox.showinfo("Éxito", "Gestos importados!")
            except:
                #Mensaje de error
                messagebox.showerror("Error", "Error al exportar")
        else:
            #Mensaje de error
            messagebox.showerror("Error", "No hay ningún elemento a exportar")

    #Selección de la carpeta donde se tomarán las imágenes
    def seleccionar_carpeta(self):
        # Limpiar caja de texto de la ruta
        self.textbox_path_gest.delete(0, "end")
        #Abrir explorador de archivos para la selección
        directorio = filedialog.askdirectory()
        if directorio != "":
            os.chdir(directorio)
        # Se habilita la caja de texto para la edición de la ruta
        self.textbox_path_gest.config(state="normal")
        # Se muestra el directorio seleccionado en la caja de texto
        self.textbox_path_gest.insert(0, os.getcwd())

    # Selección de la carpeta donde se tomarán las imágenes test
    def seleccionar_carpeta_test(self):
        # Limpiar caja de texto de la ruta
        self.textbox_path_test.delete(0, "end")
        # Abrir explorador de archivos para la selección
        directorio = filedialog.askdirectory()
        if directorio != "":
            os.chdir(directorio)
        # Se habilita la caja de texto para la edición de la ruta
        self.textbox_path_test.config(state="normal")
        # Se muestra el directorio seleccionado en la caja de texto
        self.textbox_path_test.insert(0, os.getcwd())

    #Creación de un nuevo elemento de la lista con valores de NOMBRE y CARPETA seleccionada
    def agregar_gesto(self):
        #Comprobrar que los campos han sido llenados
        if self.name_string.get() != "" and self.path_string.get() != "" and self.path_test.get() != "":
            #Los datos ingresados se insertaran a la lista(widget TREEVIEW)
            self.tree_list.insert('', 'end', values=(self.name_string.get(), self.path_string.get(),
                                                     self.path_test.get()), tag=("tag_tree_list",))
            # Se vacían las cajas de texto
            self.textbox_name_gest.delete(0, tk.END)
            self.textbox_path_gest.delete(0, tk.END)
            self.textbox_path_test.delete(0, tk.END)
        else:
            #Mensaje de error
            messagebox.showerror("Error", "Verifica que todos los campos no estén vacíos.")

    # Los nuevos datos ingresados se insertaran a la lista(widget TREEVIEW),
    # y se actualizará los valores del item seleccionado
    def actualizar_gesto(self):
        # Comprobrar que los campos han sido llenados
        if self.name_string.get() != "" and self.path_string.get() != "" and self.path_test.get() != "":
            # Se obtiene el id del item seleccionado
            id_item = self.tree_list.focus()
            # Se obtiene el item
            item = self.tree_list.item(id_item)
            # Se actualizan los datos del item en la lista
            self.tree_list.item(id_item, values=(self.name_string.get(), self.path_string.get(),
                                                 self.path_test.get()))

            # Limpiar selección de la lista
            #self.tree_list.selection_remove(id_item)
            self.tree_list.selection_clear()
            #Reiniciar los estados de los widgets principales
            self.estado_inicial_widgets()

        else:
            #Mensaje de error
            messagebox.showerror("Error", "Verifica que todos los campos no estén vacíos.")

    #Eliminación de un item seleccionado por el usuario desde la lista(widget TREEVIEW)
    def eliminar_gesto(self):
        # Se obtiene el id del item seleccionado de la lista
        id_item = self.tree_list.focus()
        # Se elimina el item de la lista
        self.tree_list.delete(id_item)
        # Reiniciar los estados de los widgets principales
        self.estado_inicial_widgets()

    #Función vinculada con el evento TreeviewSelect, al seleccionar cualquier elemento
    #el usuario podrá realizar dos acciones: Actualizar y eliminar un item de la lista(widget TREEVIEW)
    def seleccionar_item(self,event):
        #Se habilitan los botones para las distintas acciones hacia un item(gesto) de la lista
        self.button_update_gest['state'] = 'normal'
        self.button_delete_gest['state'] = 'normal'
        #Se deshabilita el botón de agregar un nuevo gesto
        self.button_new_gest['state'] = 'disabled'

        #Se obtiene el id del item seleccionado
        id_item= self.tree_list.focus()
        #Se obtiene los valores de item seleccionado a partir del id
        values = self.tree_list.item(id_item, option="values")

        #Mostrar los valores en las cajas de texto respectivamente
        self.name_string.set(values[0])
        self.path_string.set(values[1])
        self.path_test.set(values[2])

    #Reiniciar el estado de los principales widgets para agregar, actualizar o eliminar un elemento de la lista
    def estado_inicial_widgets(self):
        # Se vacían las cajas de texto: NOMBRE y CARPETA
        self.textbox_name_gest.delete(0, tk.END)
        self.textbox_path_gest.delete(0, tk.END)
        self.textbox_path_test.delete(0, tk.END)
        # Deshabiliar botón de eliminar
        self.button_delete_gest['state'] = 'disabled'
        # Deshabiliar botón de actualizar
        self.button_update_gest['state'] = 'disabled'
        # Habilitar botón de agrear
        self.button_new_gest['state'] = 'normal'

    #Se guardará en la ruta seleccionada un archivo que ha sido creado
    def guardar_como(self):
        # Limpiar caja de texto de la ruta
        self.textbox_path_save.delete(0, "end")
        directorio = filedialog.askdirectory()
        if directorio != "":
            os.chdir(directorio)
        # Se habilita la caja de texto para la edición de la ruta
        self.textbox_path_save.config(state="normal")
        # Se muestra el directorio seleccionado en la caja de texto
        self.textbox_path_save.insert(0, os.getcwd())


    #Dar inicio al entrenamiento del modelo
    def inicio_entrenamiento(self):
        list_data = []
        #Comprobar que los campos de NOMBRE y GUARDAR CÓMO no estén vacíos, y hay items en la lista
        if self.textbox_model_name.get() != "" and self.textbox_path_save.get():
            # Se obtienen los id's de todos los items que se encuentran en la lista
            ids_items = self.tree_list.get_children()
            if len(ids_items) >0:
                #Por cada id se obtienen los valores de cada item
                for id_item in ids_items:
                    #Obtener valores
                    list_data.append(self.tree_list.item(id_item,option="values"))
                try:
                    trainer.ModelTrainer(list_data, self.textbox_model_name.get(), self.textbox_path_save.get())
                    messagebox.showinfo("Éxito!", "El modelo ha sido entrenado")
                except Exception:
                    e = sys.exc_info()[1]
                    print(e.args[0])
                    #Mensaje de error
                    messagebox.showerror("Error", "Ocurrió un error, vuelve a intentarlo")
            else:
                #Mensaje de error
                messagebox.showerror("Error", "No hay elementos en la lista")
        else:
            #Mensaje de error
            messagebox.showerror("Error", "Verifica que los campos del nombre y ruta del modelo no estén vacíos")
