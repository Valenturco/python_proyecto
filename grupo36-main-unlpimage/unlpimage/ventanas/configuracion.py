import PySimpleGUI as sg 
import os
def CrearVentana():
    directorio=os.path.abspath(os.path.dirname(__file__))
    directorio_direcciones=os.path.abspath(os.path.join(directorio,"direcciones.txt"))
    lectura=open(directorio_direcciones,"r")
    lista=lectura.readline()
    lista=lista.split("@")
    sg.set_options(background_color="Tan")
    for e in lista:
        print(e)
    dir_im=lista[0]
    dir_coll=lista[1]
    dir_mem=lista[2]
    lectura.close()
    layout = [  [sg.Push(background_color="Tan") ,sg.Button(button_text="volver", button_color="DarkBlue")],
                [sg.Text("Repositorio de Imagenes",background_color="Tan")], 
                [sg.Input(dir_im,key='-Rep-',size=(25,2),enable_events=True),sg.FolderBrowse(button_text="Seleccionar")],
                [sg.Text("Directorio de collage",background_color="Tan")],
                [sg.Input(dir_coll,key='-Coll-',size=(25,2),enable_events=True),sg.FolderBrowse(button_text="Seleccionar")],
                [sg.Text("Directorio de memes",background_color="Tan")],
                [sg.Input(dir_mem,key='-Memes-',size=(25,2),enable_events=True),sg.FolderBrowse(button_text="Seleccionar")],
                [sg.Button("Guardar todos los cambios",key="-guardar-")]
                ]
    window = sg.Window("Configuracion",
                    layout,finalize=True)
    window.set_min_size((500,500))
    while True:
        event, values = window.read()
        if event == "volver" or event == sg.WIN_CLOSED:
            break
        elif event=="-guardar-" :
            escritura=open(directorio_direcciones,"w")
            dir_im=values['-Rep-']
            dir_coll=values['-Coll-']
            dir_mem=values['-Memes-']
            print(dir_mem)
            escritura.write(dir_im+"@"+dir_coll+"@"+dir_mem)
            escritura.close()
    window.close()
