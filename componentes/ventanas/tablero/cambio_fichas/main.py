"""
Módulo principal de la ventana de cambio de fichas.
"""


import PySimpleGUI as sg
from componentes.ventanas.general import leer_evento
from componentes.ventanas.tablero.logica.funciones import fichas_totales, actualizar_tiempo
from componentes.ventanas.tablero.cambio_fichas.funciones import *


def main(window, tablero, parametros):
  """
  Función que muestra una ventana donde el jugador puede cambiar algunas o todas sus fichas.

  Parámetros:
      - window (sg.Window): ventana del tablero.
      - tablero (dict): diccionario con la información del tablero.
      - parametros (dict): diccionario con párametros que controlan la lógica del juego.
  """

  jugador = tablero['jugador']
  letras_jugador = jugador.fichas
  bolsa_de_fichas = tablero['bolsa_de_fichas']
  
  if parametros['jugada']:
    sg.Popup("Primero debe levantar sus fichas\n", **parametros_popup)
    return

  ventana = crear_ventana_cambio_fichas(letras_jugador)

  fichas = fichas_totales(bolsa_de_fichas)

  seleccionadas = {}

  cambio = False

  while not cambio:
    event, values, tiempo = leer_evento(ventana, 1000, 'esperar')
    parametros['fin_juego'], tablero['contador'] = actualizar_tiempo(window, tablero['contador'], tiempo)
    if (parametros['fin_juego']):
      break
    elif (event == 'esperar'):
      continue
    elif (event in ('Cancelar', None)):
      break
    elif (event == 'todas'):
      cambio = cambiar_todas(window, bolsa_de_fichas, parametros, letras_jugador)
    elif (event == 'Aceptar'):
      cambio = cambiar_seleccionadas(window, bolsa_de_fichas, seleccionadas, letras_jugador, parametros)
    else:
      seleccionar_ficha(ventana, event, seleccionadas, letras_jugador[event])

  ventana.Close()
  
  actualizar_tablero(window, tablero, cambio, parametros, jugador)