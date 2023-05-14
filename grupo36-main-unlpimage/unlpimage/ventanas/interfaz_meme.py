import PySimpleGUI as sg
def crearVentana():
    #sg.set_options(font=("Cooper Black",16))

    layout = [ [sg.Text("Seleccione un meme!")],
            [sg.Input(size=(20,3))],
            [sg.Button(button_text= "Guardar"),
            sg.Button(button_text= "Volver")]
    ]

    window=sg.Window("Interfaz Meme",layout,margins=(250,250),element_justification="center")
    window.BackgroundColor=("Tan")

    while True:
        event, values = window.read()
        if event == ("Volver") or event == (sg.WINDOW_CLOSED):
            break
        elif event == ("Guardar"):
            sg.popup("aca guardaria")
    window.close()