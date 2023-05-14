import PySimpleGUI as sg
import os
from PIL import Image
import io
import os
import csv
import ventanas.logs as logs
import mimetypes
from datetime import datetime 

directorio=os.path.abspath(os.path.dirname(__file__))
archivo_metadatos=os.path.abspath(os.path.join(directorio,"archivoMetadatos.csv"))
sg.set_options(background_color="Tan")
def get_image_files(folder):
    image_extensions = ['.png']  
    image_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(tuple(image_extensions)):
                image_files.append(os.path.join(root, file))
    return image_files

def MostrarImagen(ruta_imagen):

    imagen=Image.open(ruta_imagen)
    
    #Recorto la imagen de forma circular y la adapto a las medidas que yo busco 
    
    ancho=300
    alto=300
    formato=imagen.format
    nueva_imagen=imagen.resize((ancho,alto))
    
    # Convertir la imagen en un búfer de bytes
    
    nueva_imagen=nueva_imagen.convert('RGBA')
    with io.BytesIO() as output:
        nueva_imagen.save(output, format=formato)
        data = output.getvalue()
    
    return data

def crearMetadatos(ruta,archivo_metadatos,nickname): #tengo que ponerlo antes del mostrar imagen para tener los datos de la imagen original
    with open(archivo_metadatos, 'r+') as archivo_csv:
        imagen = Image.open(ruta)
        tags=[]
        descripcion=""
        tamaño = os.path.getsize(ruta)
        resolucion = (imagen.size[0],imagen.size[1])
        ult_perfil= nickname
        fecha_actual = datetime.now()
        tipo = mimetypes.guess_type(ruta)[0]
        fecha_formateada = fecha_actual.strftime('%Y-%M-%D')
        hora_formateada = fecha_actual.strftime('%H:%M:%S')
        ult_fecha= (fecha_formateada , hora_formateada)
        escritor = csv.writer(archivo_csv)
        metadatos=[ruta,descripcion,resolucion,tipo,tamaño,tags,ult_perfil,ult_fecha]
        escritor.writerow(metadatos)
    return metadatos

def buscarMetadatos(archivo_metadatos,ruta,nickname):
    if os.path.exists(archivo_metadatos):
        with open(archivo_metadatos, 'r+') as archivo_csv: 
            escritor = csv.reader(archivo_csv)
            contenido_csv = list(escritor)
            datos_imagen = [] 
            for linea in contenido_csv:
                if ruta in linea: 
                    datos_imagen.append(linea) 
            if not datos_imagen:
                return crearMetadatos(ruta, archivo_metadatos,nickname)
        return datos_imagen[(len(datos_imagen) - 1)]
    else:
        with open(archivo_metadatos, 'w') as archivo_csv: 
            escritor = csv.reader(archivo_csv)
            return crearMetadatos(ruta, archivo_metadatos,nickname)

def hacerLog(direccion_imagen,metadato):
    with open(archivo_metadatos, 'r+') as archivo_csv: 
            lector= csv.reader(archivo_csv)
            contenido_csv = list(lector)
            cant=0
            for linea in contenido_csv:
                if direccion_imagen in linea: 
                    escritor=csv.writer(archivo_csv) 
                    escritor.writerow(metadato)
                    return ""
def agregarEtiquetas(tag, metadato,tag_Boolean):
    if (metadato[5] != '') and (metadato[5] != []):
        tag_Boolean=True
    else:    
        tag_Boolean=False
    tags = metadato[5].split(',') if metadato[5] else []
    tags.append(tag)
    metadato[5] = ','.join(tags)
    metadato[7] = str(datetime.now())
    hacerLog(metadato[0], metadato)
    return tag_Boolean

def eliminarEtiquetas (metadato):
    metadato[5] = ''
    metadato[7] = str(datetime.now())
    hacerLog(metadato[0],metadato)
    return metadato

def crearVentana(direccion,nickname):
    layout = [
        [
            sg.Column(
                [
                    [sg.Listbox(values=[], size=(40, 20), key='-LISTBOX-', enable_events=True)],
                    [sg.Input(direccion,key='-FOLDER-'), sg.FolderBrowse(target='-FOLDER-')],
                    [sg.Button('Cargar Imágenes'), sg.Button('Salir')]
                ],
                element_justification='center'
            ),
            sg.Column(
                [
                    [sg.Image(key='-IMAGE-', size=(300, 300),background_color="Tan")],
                    [sg.Text('Descripción:', pad=(0, (20, 0)),background_color="Tan")],
                    [sg.Input(key='-DESCRIPTION-', size=(30, 5),disabled=True)],
                    [sg.Button('Guardar', key='-SAVE_DESCRIPTION-'),sg.Button('Modificar',key='-Modificar-')]
                ],
                element_justification='center'
            )
        ],
        [sg.Text('Etiquetas:           ',background_color="Tan"),sg.Input(key='-TAGS-', size=(30, 1),disabled=True)],
        [sg.Text('Agrega etiquetas:',background_color="Tan"),sg.Input(size=(30,1),key='-AgregarTags-')],
        [sg.Button('Guardar'),sg.Button('Eliminar')]
    ]

    tag_Boolean=False
    window = sg.Window('Etiquetador de Imágenes', layout)
    image_files = []
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == 'Cargar Imágenes':
            folder = values['-FOLDER-']
            if not folder:
                sg.popup_error("Selecciona una carpeta de imágenes")
                continue

            image_files = get_image_files(folder)
            if not image_files:
                sg.popup_error("No se encontraron imágenes en la carpeta seleccionada")
                continue
            window['-LISTBOX-'].update(values=[os.path.basename(file) for file in image_files])

        
        
        if event == '-LISTBOX-':
            
            try:
                selected_image = values['-LISTBOX-'][0]
                image_file = next(file for file in image_files if os.path.basename(file) == selected_image)
                data=MostrarImagen(image_file)
                window['-IMAGE-'].update(data=data)
                try: 
                    selected_image = values['-LISTBOX-'][0]
                    datos_imagen=buscarMetadatos(archivo_metadatos,image_file,nickname)
                    print(datos_imagen)
                    window['-TAGS-'].update(datos_imagen[5])
                    window["-DESCRIPTION-"].update(datos_imagen[1])
                except KeyError:
                     window['-TAGS-'].update("")
                window['-SAVE_DESCRIPTION-'].update(disabled=False)
            except (IndexError, StopIteration):
                sg.popup_error("No se pudo encontrar la imagen seleccionada en la lista de archivos",background_color=("Tan"))

        elif event == 'Eliminar':
            try:
                selected_image = values['-LISTBOX-'][0]
            except IndexError:
                sg.popup("No hay ninguna imagen seleccionada")
            try:
                eliminarEtiquetas(datos_imagen)
                image_file = next(file for file in image_files if os.path.basename(file) == selected_image)
                window["-TAGS-"].update(datos_imagen[5])
            except StopIteration:
                sg.popup_error("No se pudo encontrar la imagen seleccionada en la lista de archivos")
        
        elif event == 'Guardar':
            try:
                selected_image = values['-LISTBOX-'][0]
            except IndexError:
                sg.popup("No hay ninguna imagen seleccionada")
            tag= values['-AgregarTags-']
            try:
                tag_Boolean=agregarEtiquetas(tag,datos_imagen,tag_Boolean)
                image_file = next(file for file in image_files if os.path.basename(file) == selected_image)
                window["-TAGS-"].update(datos_imagen[5])
                if (tag_Boolean==False):
                    oracion_Logs="Nueva imagen clasificada"
                    logs.Actualizacion(nickname,oracion_Logs)
                else:    
                    oracion_Logs="Modificacion de imagen previamente clasificada"
                    logs.Actualizacion(nickname,oracion_Logs)
            except StopIteration:
                sg.popup_error("No se pudo encontrar la imagen seleccionada en la lista de archivos")
        elif event=='-Modificar-':
            window['-DESCRIPTION-'].update(disabled=False)
        elif event == '-SAVE_DESCRIPTION-':
            datos_imagen[1]=values['-DESCRIPTION-']
            window['-DESCRIPTION-'].update(disabled=True)
            hacerLog(datos_imagen[0],datos_imagen)
    window.close()