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
             
    ultimo_presionado = ""

    window = crear_ventana_reglas()

    while True:
        event = leer_evento(window)[0]
        if event in (None, "Volver"):
            break
        else:
          ultimo_presionado = mostrar_texto(window, event, ultimo_presionado)
    window.Close()