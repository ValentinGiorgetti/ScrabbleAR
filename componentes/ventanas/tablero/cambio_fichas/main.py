"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo principal de la ventana de cambio de fichas.
"""


import PySimpleGUI as sg
from componentes.ventanas.general import leer_evento, parametros_popup
from componentes.ventanas.tablero.logica.funciones import fichas_totales, actualizar_tiempo
from componentes.ventanas.tablero.cambio_fichas.funciones import (
    crear_ventana_cambio_fichas, seleccionar_ficha, cambiar_todas, 
    cambiar_seleccionadas, actualizar_tablero
)


def main(window, tablero, parametros):
    """
    Función que muestra una ventana donde el jugador puede cambiar algunas o todas sus fichas.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - tablero (dict): diccionario con la información del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
    """

    jugador = tablero["jugador"]
    letras_jugador = jugador.fichas
    bolsa_de_fichas = tablero["bolsa_de_fichas"]

    if parametros["jugada"]:
        sg.Popup("Primero debe levantar sus fichas\n", **parametros_popup)
        return

    ventana = crear_ventana_cambio_fichas(letras_jugador)

    fichas = fichas_totales(bolsa_de_fichas)

    seleccionadas = {}

    cambio = False

    while not cambio:
        event, values, tiempo = leer_evento(ventana, 1000, "esperar")
        parametros["fin_juego"], tablero["contador"] = actualizar_tiempo(window, tablero["contador"], tiempo)
        if parametros["fin_juego"] or event in ("cancelar", None):
            break
        elif event == "esperar":
            continue
        elif event == "todas":
            cambio = cambiar_todas(window, bolsa_de_fichas, parametros, letras_jugador)
        elif event == "algunas":
            cambio = cambiar_seleccionadas(window, bolsa_de_fichas, seleccionadas, letras_jugador, parametros)
        else:
            seleccionar_ficha(ventana, event, seleccionadas, letras_jugador[event])

    ventana.Close()
    
    if cambio:
        actualizar_tablero(window, tablero, parametros, jugador)
