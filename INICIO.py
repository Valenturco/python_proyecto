import PySimpleGUI as sg



sg.set_options(font=("Cooper Black",16))

t1=sg.Text("UNLPImage",size=(10,1),justification="center",background_color="Tan") 

dic={}

def sumarPerfil():
    #aca traemos el perfil
    #from nuevoPerfil import nuevo
    #dic [perfil[0]] = nuevo
    print("listo")   

layout= [
    [t1],

    #separa
    [sg.Image(key='imagen',size=(70,70),background_color="Tan")],
    #separa


    [sg.Text("Elija un perfil",background_color=("Tan"))],


    #separa
    [sg.Text(" ",background_color=("Tan"))],
    #separa


    [sg.Listbox(key="perfiles", values=(dic), enable_events=True, size=(20, 1))],


    [sg.Text(" ",background_color=("Tan"))],


    [sg.Button("Agregar",button_color="DarkBlue", size=(6,1),key="agregar")]
]

window=sg.Window("Inicio",layout,margins=(250,200),element_justification='center')
window.BackgroundColor=("Tan")

while True:
    event, values = window.read()
    if event == (sg.WINDOW_CLOSED):
        break
    elif event == ("agregar"):
        sumarPerfil()
        sg.popup("aca agregamos")
window.close()