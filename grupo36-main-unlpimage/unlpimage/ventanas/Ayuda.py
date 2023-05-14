import PySimpleGUI as sg

def crearVentana():
    

    layout =[ [sg.Text("AYUDA SOBRE LA APLICACION")],
                    [sg.Button('Aceptar')]
           ]

    window = sg.Window("Ayuda", layout, margins=(100,50))
    window.BackgroundColor=("Tan")

    while True:
        event, values = window.read()
        if event == ("Aceptar") or event == (sg.WINDOW_CLOSED):
            break
    window.close()
