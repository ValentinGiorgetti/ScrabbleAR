import random, PySimpleGUI as sg
from componentes.jugador import Jugador
from componentes.ventanas.tablero.funciones import *
import datetime
from playsound import playsound as reproducir
from os.path import join

def main(configuracion, partida_anterior = None):
    """
    Esta es la función "principal", donde se crea el tablero de juego y se desarrolla la lógica más importante del mismo.
    Recibe la configuración elegida para la partida, y la partida guardada, en caso de que el usuario haya elegido reanudar
    la partida anterior.

    El parámetro "partida" es un diccionario que contiene la información necesaria para reconstruir el estado del tablero
    de la partida anterior. Si es None, significa que el usuario empezó una nueva partida. El parámetro "configuración" es
    otro diccionario que almacena las configuraciones de la partida.

    En caso de que "partida" sea distinto de None, el usuario eligió reanudar la partida anterior, por lo tanto las variables
    se inicializarán con los valores correspondientes del diccionario.

    Si "partida" es None, las variables se inicializarán con los valores correspondientes del diccionario "configuración".
    
    parametros_partida = {"nivel" : str, "tamanio_tablero" : int, "centro" : int, "palabras_validas" : str, "contador" : int, "bolsa_de_fichas" : {letra : {puntaje : int, cantidad_fichas : int}}} 
    """

    tablero, parametros = inicializar_parametros(configuracion, partida_anterior)

    window = crear_ventana_tablero(tablero, parametros, partida_anterior)
    
    comenzar = partida_guardada = None

    while True:
        event = window.Read(timeout = 1000, timeout_key = '')[0]  # milisegundos
  #      if (event):
  #        reproducir(join("componentes", "sonidos", "boton.mp3"))
  #      else:
  #        continue
        if event in (None, 'Salir'):
            break
        elif event ==  "Iniciar":
            comenzar = iniciar_partida(window, parametros, partida_anterior)
        elif event ==  "Pausa":
            comenzar = pausar(window, comenzar)
        elif event ==  "Posponer":
            salir, partida_guardada = posponer(tablero, parametros["jugada"])
            if salir:
              break
        elif event ==  "Terminar":
            finalizar_partida(window, tablero)
        elif comenzar:
            if tablero['turno'] == 'computadora':
              jugar_computadora(window, parametros, tablero)
            elif tablero['turno'] == 'jugador':
              if event ==  "cambiar":
                cambiar_fichas(window, tablero, parametros)
              elif event ==  "pasar":
                pasar(window, parametros, tablero)
              elif event ==  "confirmar":
                confirmar_palabra(window, parametros, tablero)
              elif event in range(7):
                seleccionar_ficha(window, parametros, event)
              elif event:
                colocar_ficha(window, parametros, tablero, event)
            if not tablero['contador'] or parametros['fin_juego']:
              finalizar_partida(window, tablero)
              comenzar = False
            window["tiempo"].Update(datetime.timedelta(seconds = tablero['contador']))
            tablero['contador'] -=  1
            window["palabra_formada"].Update(palabra_formada(tablero['jugador'].fichas, parametros['jugada']))
            window["cantidad_fichas"].Update(fichas_totales(tablero['bolsa_de_fichas']))

    window.Close()
    return partida_guardada, tablero['jugador'], tablero['computadora']
