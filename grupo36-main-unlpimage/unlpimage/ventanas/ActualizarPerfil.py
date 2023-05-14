import PySimpleGUI as sg
import ventanas.configuracion as confg
from PIL import Image, ImageDraw, ImageOps
import io
import os
import ventanas.logs as logs
def solo_numeros(valor):
    if valor.isdigit():
        return True
    else:
        sg.popup('Ingrese solo números')
        return False
    
def CrearVentana(dato,nickname):
    sg.set_options(background_color="Tan")
    Titulo=[[sg.Text("Nuevo Perfil",font="Italics",background_color="Tan")],
            [sg.Button("Configuracion")]]
    Datos_perfil=[[sg.Text("Nickname o Alias",background_color="Tan")],
                [sg.Input(nickname[0],disabled=True,size=(30, 3),key="-nickname-")],
                [sg.Text("Nombre",background_color="Tan")],
                [sg.Input(default_text=dato[0],size=(30, 3),key="-nombre-")],
                [sg.Text("Edad",background_color="Tan")],
                [sg.Input(default_text=dato[1],size=(30, 3),enable_events=True,key="-edad-")],
                [sg.Text("Genero",background_color="Tan")],
                [sg.Input(default_text=dato[2],size=(30, 3),enable_events=True,key="-genero-")],
                [sg.Button("Guardar")]
    ]
    
    visualizar_imagen=[
            [sg.Image(filename=dato[3],key='imagen',size=(250,250),background_color="Tan")],
            [sg.Text("Seleccione una imagen",justification="Centre",background_color="Tan")],
            [sg.Input(default_text=dato[3],size=(25, 3), key='InputImagen'), 
            sg.FileBrowse("Seleccionar", file_types=(("JPEG Files", ".jpg;.jpeg"), ("PNG Files", ".png;.PNG"), ("GIF Files", "*.gif")), enable_events=True, key='seleccion')],
            [sg.Button('Mostrar', key='Mostrar')]
    ] 
    
    radio_seleccion=False
    
    layout=[[sg.Column(Datos_perfil,background_color="Tan"),
            sg.Column(visualizar_imagen,background_color="Tan")]
    ] 
    window = sg.Window("Nuevo Perfil",
                    layout,grab_anywhere=True,
                    background_color=("Tan"),finalize=True)
    dicc={}
    window.set_min_size((750,750))
    while True:
        event, values = window.read()
        if event=="salir" or event==sg.WIN_CLOSED:
            break
       
        elif event == '-edad-' and not solo_numeros(values['-edad-']):
                window['-edad-'].update('')
       
        elif(event=="otro"):
           
            if(radio_seleccion==False):
                window["-genero-"].update(disabled=True)
                window["nobinario"].update(disabled=False)
                radio_seleccion=True
                window["otro"].update(value=radio_seleccion)
            else:
                window["-genero-"].update(disabled=False)
                window["nobinario"].update(disabled=True)
                radio_seleccion=False
                window["otro"].update(value=radio_seleccion)
        
        elif(event=="Guardar"):
            if (values['InputImagen']==""):
                sg.popup_error("Falta seleccionar una imagen de perfil",title="Error")    
            elif(values["-nombre-"]!="" and values["-edad-"]!=""):
                nombre=values["-nombre-"]
                edad=values["-edad-"]
                if(not radio_seleccion):
                    genero=values["-genero-"]
                else:
                    genero=values["nobinario"]
                directorio=os.path.abspath(os.path.dirname(__file__))
                directorio_direcciones=os.path.abspath(os.path.join(directorio,"..","imagenes",f"{nickname[0]}.png"))
                nueva_imagen.save(directorio_direcciones)
                dato=[nombre,edad,dato[2],directorio_direcciones] 
                sg.popup('Perfil guardado correctamente', title='Éxito')
                break
            else:
                sg.popup("Hay un campo que no tiene informacion, rellenalo",title="Error")
        
        elif(event=='Mostrar'):
            ruta_imagen=values['InputImagen']
            if (ruta_imagen==""):
                sg.popup_error('no se introdujo una ruta, intente de nuevo',
                    title="Error")
            else:
                # Abrir la imagen con PIL
                imagen=Image.open(ruta_imagen)
                #Recorto la imagen de forma circular y la adapto a las medidas que yo busco 
                ancho=250
                alto=250
                nueva_imagen=imagen.resize((ancho,alto))
                mask = Image.new('L', nueva_imagen.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + nueva_imagen.size, fill=350)
                nueva_imagen = ImageOps.fit(nueva_imagen, mask.size)
                nueva_imagen.putalpha(mask)
                # Convertir la imagen en un búfer de bytes
                nueva_imagen=nueva_imagen.convert('RGBA') 
                with io.BytesIO() as output:
                    nueva_imagen.save(output, format='PNG')
                    data = output.getvalue()
                window['imagen'].update(size=(ancho,alto),data=data)
    oracion_Logs="Cambio en la configuracion del sistema"
    logs.Actualizacion(dato[0],oracion_Logs)
    window.close()
    return dato
