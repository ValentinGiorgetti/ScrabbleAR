"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo principal de la ventana de reglas.
"""


from webbrowser import open
from componentes.ventanas.general import leer_evento
from componentes.ventanas.reglas.funciones import crear_ventana_reglas, mostrar_texto


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
        if event == "mas_informacion":
            open("https://github.com/ValentinGiorgetti/ScrabbleAR/blob/master/README.md#reglas-del-juego")
            continue
        if event in (None, "Volver"):
            break
        else:
            ultimo_presionado = mostrar_texto(window, event, ultimo_presionado)
            
    window.Close()
