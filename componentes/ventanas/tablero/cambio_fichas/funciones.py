"""
Módulo que contiene las funciones usadas en la ventana de cambio de fichas.
"""


import random, PySimpleGUI as sg
from componentes.ventanas.general import parametros_popup, parametros_ventana
from componentes.ventanas.tablero.logica.funciones import *


def crear_ventana_cambio_fichas(letras_jugador):
    """
    Función usada para crear la ventana de cambio de fichas.

    Parámetros:
        - letras_jugador (list): lista con las fichas del jugador.

    Retorna:
        - (sg.Window): ventana de cambio de fichas.
    """

    layout_cambiar_fichas = [
        [sg.Text("Seleccione las fichas que quiere intercambiar")],
        [sg.Text("")],
        [
            sg.Button(letras_jugador[i], size=(3, 1), key=i, pad=(0.5, 0.5), button_color=("white", "green"))
            for i in range(7)
        ],
        [sg.Text("")],
        [sg.Button("Aceptar"), sg.Button("Cambiar todas", key="todas"), sg.Button("Cancelar")],
    ]

    return sg.Window("  Cambiar fichas", layout_cambiar_fichas, **parametros_ventana)


def cambiar_todas(window, bolsa_de_fichas, parametros, letras_jugador):
    """
    Función para que el jugador cambie todas sus fichas.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - bolsa_de_fichas (dict): diccionario con las fichas en la bolsa.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - letras_jugador (list): lista con las fichas del jugador.

    Retorna:
        - (bool): devuelve si se pudieron cambiar las fichas.
    """

    if len(fichas_totales(bolsa_de_fichas)) >= 7:
        for letra in letras_jugador:
            bolsa_de_fichas[letra]["cantidad_fichas"] += 1
        letras_jugador.clear()
        repartir_fichas(bolsa_de_fichas, letras_jugador)
        for i in range(7):
            window[i].Update(letras_jugador[i], button_color=("white", "green"))
        parametros["historial"] += "\n\n - Se cambiaron todas las fichas del jugador."
        window["historial"].Update(parametros["historial"])
        return True
    else:
        sg.Popup("No quedan suficientes fichas en la bolsa\n", **parametros_popup)
        return False


def cambiar_seleccionadas(window, bolsa_de_fichas, seleccionadas, letras_jugador, parametros):
    """
    Función que cambia las fichas seleccionadas por el jugador.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - bolsa_de_fichas (dict): diccionario con las fichas en la bolsa.
        - seleccionadas (dict): diccionario con las fichas elegidas para cambiar.
        - letras_jugador (list): lista de las fichas del jugador.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.

    Retorna:
        - (bool): devuelve si se pudieron cambiar las fichas.
    """

    if not seleccionadas:
        sg.Popup("Debe seleccionar alguna letra\n", **parametros_popup)
        return False
    if len(fichas_totales(bolsa_de_fichas)) >= len(seleccionadas):
        for i in seleccionadas:
            bolsa_de_fichas[seleccionadas[i]]["cantidad_fichas"] += 1
            letra = letra_random(bolsa_de_fichas)
            window[i].Update(letra, button_color=("white", "green"))
            letras_jugador[i] = letra
        parametros["historial"] += "\n\n - Se cambiaron algunas fichas del jugador."
        window["historial"].Update(parametros["historial"])
        return True
    else:
        sg.Popup("No quedan suficientes fichas en la bolsa", **parametros_popup)
        return False


def seleccionar_ficha(ventana, event, seleccionadas, ficha):
    """
    Función para que el jugador seleccione una ficha.

    Parámetros:
        - ventana (sg.Window): ventana de cambio de fichas.
        - event (int): entero que indica la posición de la ficha a seleccionar.
        - seleccionadas (dict): diccionario donde se guardan las fichas seleccionadas.
        - ficha (str): letra de la ficha a seleccionar.
    """

    if event in seleccionadas:
        ventana[event].Update(button_color=("white", "green"))
        del seleccionadas[event]
    else:
        ventana[event].Update(button_color=("white", "red"))
        seleccionadas[event] = ficha


def actualizar_tablero(window, tablero, cambio, parametros, jugador):
    """
    Función para actualizar la ventana del tablero con el cambio de fichas.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - tablero (dict): diccionario con la información del tablero.
        - cambio (bool): indica si se cambiaron fichas.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - jugador (Jugador): instancia de la clase Jugador que representa al usuario.
    """

    if cambio:
        jugador.cambios_restantes -= 1
        actualizar_tabla(jugador, tablero["computadora"], window)
        reiniciar_parametros(parametros)
        if not jugador.cambios_restantes:
            window["cambiar"].Update(disabled=True)
        tablero["turno"] = "Computadora"
        window["turno"].Update("Computadora")