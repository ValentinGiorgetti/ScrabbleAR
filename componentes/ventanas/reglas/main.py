import PySimpleGUI as sg
from playsound import playsound as reproducir
from os.path import join
from componentes.ventanas.reglas.funciones import *

def main():
    """
    Función que muestra una ventana con información sobre cada nivel: tipo de palabras válidas
    y tamaño del tablero.
    """

    textos = {'Fácil' : "Palabras válidas: cualquier palabra que la librería Pattern considere válida.\nTamaño del tablero: 19 x 19.",
             'Medio' : "Palabras válidas: adjetivos y verbos.\nTamaño del tablero: 17 x 17.",
             'Difícil': "Palabras válidas: adjetivos o verbos, se selecciona en forma aleatoria.\nTamaño del tablero: 15 x 15."}
             
    ultimo_presionado = ""
    colores = {'Fácil' : ("white", "green"), 'Medio' : ("white", "orange"), 'Difícil' : ('white', 'red')}

    window = crear_ventana_reglas()

    while True:
        event = window.Read()[0]
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        if event in (None, "Volver"):
            break
        else:
          ultimo_presionado = mostrar_texto(window, event, colores[event], textos[event], ultimo_presionado)
    window.Close()