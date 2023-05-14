import ventanas.nuevoperfil as nuevo 
import ventanas.configuracion as conf
import os 
import json  
import PySimpleGUI as sg
import ventanas.Menu_Principal as menu
sg.set_options(font=("Cooper Black",13))

#direccion donde se almacenan los perfiles
direcciones={}
dicc={}
directorio=os.path.abspath(os.path.dirname(__file__))
directorio_direcciones=os.path.abspath(os.path.join(directorio,"perfiles.json"))
archivo=open(directorio_direcciones,"r") 
dicc=json.load(archivo)
archivo.close
texto=[[sg.Text("UNLPImage",font=("Cooper Black",16),background_color="Tan",justification="Left")] ]
seleccion=[
            [sg.Image(key='imagen',size=(70,70),background_color="Tan")],
            [sg.Text("Elija un perfil",background_color=("Tan"),justification="Center")],
            [sg.Listbox(key="perfiles",values=list(dicc.keys()),select_mode=True,enable_events=True, size=(25, 1))],
            [sg.Text(" ",background_color=("Tan"))],
            [sg.Button("Agregar",pad=(91,1),button_color="DarkBlue",key="agregar")]
]

layout= [ [[sg.Column(texto,background_color="Tan",justification="Left")],
           sg.Column(seleccion,background_color="Tan",justification="Center")]   
    ]   
window=sg.Window("Inicio",layout,resizable=True,
                 finalize=True,background_color="tan",margins=(1,1),)
window.set_min_size((750,750))
while True:
    event, values = window.read()
    if event == (sg.WINDOW_CLOSED):
        break
    elif event == ("agregar"):
        dicc.update(nuevo.CrearVentana())
        window["perfiles"].update(values=dicc)
        archivo= open(directorio_direcciones,"w")
        json.dump(dicc,archivo)
        archivo.close()
    elif event=="perfiles":
        perfil=values["perfiles"]
        menu.crearVentana(dicc[perfil[0]],perfil)
window.close()
    
    
##A. Inicio
    # Si existe el archivo de usuarios_del_sistema.json
        #Leer el json
            # "nombre" , "edad", "nick", "genero", "avatar : link absoluto de la imagen"
        # Traer al menos los primeros tres
        #Si hay más, mostrar el boton ver más
        # Hay al menos tres botones que tienen un boton que esta asociado a cada dato de los tres traidos del json
        # Cada boton tiene debajo el nombre de usuario
        # Cada boton de estos puede abrir el mennu principal. tiene que mandar una key para saber cual usuario entro
    # Sino, abrir Nuevo Perfil
#B. Nuevo perfil
#C. Menú principal
    # Tiene 4 botones en modo de lista, centrados en pantalla, que acceden a cada menu segun su leyenda: "Etiquetar Foto", "Generar meme", "Generar collage","salir"
#D. Editar perfil
#E. Configuración
#F. Generador de memes (sólo interfaz)
#G. Generador de collage (sólo interfaz)
#H. Etiquetar imágenes
