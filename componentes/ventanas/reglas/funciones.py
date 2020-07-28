import PySimpleGUI as sg
from componentes.ventanas.parametros import parametros_ventana
    
  

def crear_ventana_reglas():

    layout = [
        [sg.Text("Reglas del juego", size=(60, 1), justification = 'center', background_color = '#1d3557')],
        [sg.Text('')],
        [sg.Button("Fácil", size=(7, 1)), sg.Button("Medio", size=(7, 1)), sg.Button("Difícil", size=(7, 1))],
        [sg.Text('')],
        [sg.Multiline("Seleccione un nivel", key="nivel", disabled=True, size = (60, 3))],
        [sg.Text('')],
        [sg.Button("Volver", size=(7, 1))],
    ]
    return sg.Window("Reglas", layout, **parametros_ventana)
    
    
def mostrar_texto(ventana_reglas, event, color, texto, ultimo_presionado):

    if ultimo_presionado != "":
        ventana_reglas[ultimo_presionado].Update(button_color=sg.DEFAULT_BUTTON_COLOR)
    ventana_reglas[event].Update(button_color=color)
    ultimo_presionado = event
    ventana_reglas["nivel"].Update(texto)
    
    return ultimo_presionado
    

