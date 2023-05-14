import PySimpleGUI as sg
import ventanas.configuracion as confg
import os
import ventanas.GeneradorImagen as img
import ventanas.interfaz_meme as meme
import ventanas.ActualizarPerfil as act
from PIL import Image, ImageDraw, ImageOps
import io
import os
import json
import ventanas.Ayuda as ayuda
import ventanas.EtiquetarImagenes as etiquetar

def MostrarImagen(ruta_imagen):
    imagen=Image.open(ruta_imagen)
    
    #Recorto la imagen de forma circular y la adapto a las medidas que yo busco 
    
    ancho=50
    alto=50
    imagen = imagen.resize((ancho, alto))
    mascara = Image.new('L', (ancho, alto), 0)
    dibujo = ImageDraw.Draw(mascara)
    dibujo.ellipse((0, 0, ancho, alto), fill=350)
    imagen = ImageOps.fit(imagen, mascara.size, centering=(0.5, 0.5))
    imagen.putalpha(mascara)
    imagen = imagen.convert('RGBA')
    # Convertir la imagen en un búfer de bytes
    with io.BytesIO() as output:
        imagen.save(output, format='PNG')
        data = output.getvalue()
    return data

def crearVentana(datos,nickname):
    print(datos)
    directorio=os.path.abspath(os.path.dirname(__file__))
    directorio_imagenes=os.path.abspath(os.path.join(directorio,"..","imagenes"))
    directorio_perfil=os.path.abspath(os.path.join(directorio_imagenes,nickname[0]+".png"))
    #sg.set_options(font=("Cooper Black",16))
    data=MostrarImagen(directorio_perfil)

    menu =[ [sg.Image(background_color="tan",size=(5,5))],
            [sg.Button('Generador de Memes',key="-mem-",size=(25,1))],
            [sg.Image(background_color="tan",size=(5,5))],
            [sg.Button('Generador de Collage',key="-collage-",size=(25,1))],
            [sg.Image(background_color="tan",size=(5,5))],
            [sg.Button('Etiquetar Imágenes',key="-img-",size=(25,1))], 
            [sg.Image(background_color="tan",size=(5,5))],
            [sg.Button('Salir',pad=(90,2))]
        ]
    barra_layout =[sg.Column(
        [
            [sg.Button(image_data=data, enable_events=True, image_subsample=2, border_width=0, button_color="Tan", key="-actualizar-")],
            [sg.Text(" "+nickname[0], font=("Black",11), background_color="Tan")]
        ],
            element_justification="left",
            justification="left",
            background_color="Tan"
        ),sg.Push("Tan"),
                sg.Column(
                    [[                    
                    sg.Button(image_filename=os.path.abspath(os.path.join(directorio_imagenes,"configuracion.png")),button_color="Tan",key="config",border_width=0), 
                    
                    sg.Image(background_color="tan",size=(5,5)),
                    
                    sg.Button(image_filename=os.path.abspath(os.path.join(directorio_imagenes,"ayuda.png")),button_color="Tan", border_width=0,key='help'), 
                    ]])
    ]

    
    layout = [[
                barra_layout,
                sg.Column(menu,background_color="Tan",)]
    ]
    
    window = sg.Window("Menú Principal", layout,finalize=True,resizable=True,element_justification="Center")
    window.set_min_size((500,500))
    window.BackgroundColor=("Tan")
    directorio=os.path.abspath(os.path.dirname(__file__))
    directorio_direcciones=os.path.abspath(os.path.join(directorio,"direcciones.txt"))
    try:
        lectura=open(directorio_direcciones,"r")
    except FileNotFoundError:
        escritura=open(directorio_direcciones,"w")
        escritura.write (directorio_imagenes+"@"+directorio_imagenes+"@"+directorio_imagenes)
        escritura.close()
        lectura=open(directorio_direcciones,"r")
    lista=lectura.readline()
    lista=lista.split("@")
    for e in lista:
        dir_im=lista[0]
        dir_coll=lista[1]
        dir_mem=lista[2]
    lectura.close()
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Salir'):
            break
        elif event == ('help'):
            ayuda.crearVentana()
        elif event=="-actualizar-":
            dicc={}
            directorio=os.path.abspath(os.path.dirname(__file__))
            directorio_direcciones=os.path.abspath(os.path.join(directorio,"..","perfiles.json"))
            archivo=open(directorio_direcciones,"r") 
            dicc=json.load(archivo)
            archivo.close()
            lista=act.CrearVentana(datos,nickname)
            print(lista)
            datos=lista
            dicc[nickname[0]]=lista
            archivo= open(directorio_direcciones,"w")
            json.dump(dicc,archivo)
            archivo.close()
            window["-actualizar-"].update(image_data=MostrarImagen(dicc[nickname[0]][3]))
        elif event == 'config':
            confg.CrearVentana()
        elif event == '-mem-':
            meme.crearVentana()
        elif event == "-collage-":
            img.crearVentana()
        elif event=="-img-":
            etiquetar.crearVentana(dir_im,nickname)
    window.close()
    
