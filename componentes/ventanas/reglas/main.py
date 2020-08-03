"""
Módulo principal de la ventana de reglas.
"""


from componentes.ventanas.reglas.funciones import *
from componentes.ventanas.general import leer_evento


def main():
    """
    Función que muestra la ventana de reglas.
    
    Informa el tipo de palabras válidas y tamaño del tablero de acuerdo
    al nivel seleccionado.
    """

    textos = {'Fácil' : "Palabras válidas: cualquier palabra que la librería Pattern considere válida.\nTamaño del tablero: 19 x 19.",
             'Medio' : "Palabras válidas: adjetivos y verbos.\nTamaño del tablero: 17 x 17.",
             'Difícil': "Palabras válidas: adjetivos o verbos, se selecciona en forma aleatoria.\nTamaño del tablero: 15 x 15."}
             
    ultimo_presionado = ""
    colores = {'Fácil' : ("white", "green"), 'Medio' : ("white", "orange"), 'Difícil' : ('white', 'red')}

    window = crear_ventana_reglas()

    while True:
        event = leer_evento(window)[0]
        if event in (None, "Volver"):
            break
        else:
          ultimo_presionado = mostrar_texto(window, event, colores[event], textos[event], ultimo_presionado)
    window.Close()