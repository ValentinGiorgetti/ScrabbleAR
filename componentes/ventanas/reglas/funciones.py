"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo que contiene las funciones usadas por la ventana de reglas.
"""


import PySimpleGUI as sg
from componentes.ventanas.general import parametros_ventana, colores, titulos


def crear_ventana_reglas():
    """
    Función usada para crear la ventana de reglas.

    Retorna:
        - (sg.Window): la ventana de reglas.
    """

    tamanio = (7, 1)
    layout = [
        [sg.Text("Reglas del juego", **titulos, size = (49, 1))],
        [sg.Text("")],
        [sg.Button("Fácil", size=tamanio), sg.Button("Medio", size=tamanio), sg.Button("Difícil", size=tamanio)],
        [sg.Text("")],
        [sg.Multiline("Seleccione un nivel", key="nivel", disabled=True, size=(60, 4))],
        [sg.Text("")],
        [sg.Button("Volver", size=tamanio)]
    ]

    return sg.Window(" Reglas", layout, **parametros_ventana)


def mostrar_texto(ventana_reglas, event, ultimo_presionado):
    """
    Función usada para mostrar las reglas de un nivel.
    
    Actualiza los widgets de la ventana y muestra el texto correspondiente
    al nivel seleccionado.

    Parámetros:
        - ventana_reglas (sg.Window): ventana de reglas.
        - event (str): dificultad seleccionada.
        - ultimo_presionado (str): anterior dificultad seleccionada.

    Retorna:
        - ultimo_presionado (str): dificultad seleccionada.
    """

    textos = {
        "Fácil": "Palabras válidas: adjetivos, sustantivos y verbos.\n\nTamaño del tablero: 19 x 19.",
        "Medio": "Palabras válidas: adjetivos y verbos.\n\nTamaño del tablero: 17 x 17.",
        "Difícil": "Palabras válidas: adjetivos o verbos, se selecciona en forma aleatoria.\n\nTamaño del tablero: 15 x 15.",
    }

    if ultimo_presionado:
        ventana_reglas[ultimo_presionado].Update(button_color=sg.DEFAULT_BUTTON_COLOR)
    ventana_reglas[event].Update(button_color=colores[event])
    ultimo_presionado = event
    ventana_reglas["nivel"].Update(textos[event])

    return ultimo_presionado