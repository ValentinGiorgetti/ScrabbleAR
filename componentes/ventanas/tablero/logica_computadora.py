"""
Módulo que contiene funciones usadas por la computadora.
"""

import time, random
from pattern.es import parse
from itertools import permutations
from componentes.ventanas.tablero.funciones import actualizar_tiempo, reproducir_sonido_palabra, es_palabra, actualizar_fichas_totales, quedan_fichas
from componentes.ventanas.tablero.funciones import *


def jugar_computadora(window, parametros, tablero):
  """
  Función que permite que la computadora pueda colocar una palabra en el tablero y sumar puntos.
  """
  
  for key in ('Posponer', 'Pausa', 'Terminar', 'confirmar', 'cambiar', 'Pasar'):
    window[key].Update(button_color = sg.DEFAULT_BUTTON_COLOR, disabled = True)

  parametros['fin_juego'], ubicacion_mas_larga = buscar_ubicacion_mas_larga(tablero, window)
  if not parametros['fin_juego']:
    parametros['fin_juego'], palabra = buscar_palabra(len(ubicacion_mas_larga), tablero, window)
  if (palabra and not parametros['fin_juego']):
    posiciones_ocupadas_pc, puntos_jugada = contar_jugada(window, palabra, ubicacion_mas_larga, tablero, parametros['casillas_especiales'])
    ubicar_palabra(window, palabra, tablero, parametros, posiciones_ocupadas_pc)
    reproducir_sonido_palabra(True)
    finalizar_jugada(window, parametros, tablero, palabra, puntos_jugada, tablero['computadora'], 'La computadora')
    if (parametros['fin_juego']):
        parametros['historial'] += '\n\n - Fin de la partida. No hay fichas suficientes para repartir.'
        window['historial'].Update(parametros['historial'])
  else:
    reproducir_sonido_palabra(False)
    repartir_nuevas_fichas(tablero, parametros, window)

  for key in ('Posponer', 'Pausa', 'Terminar', 'confirmar', 'Pasar'):
    window[key].Update(button_color = sg.DEFAULT_BUTTON_COLOR, disabled = False)
  if (tablero['jugador'].cambios_restantes):
    window['cambiar'].Update(disabled = False)
    
  tablero['turno'] = "Jugador"
  window["turno"].Update("Jugador")
    

def buscar_ubicacion_mas_larga(tablero, window):
  """
  Función que retorna la ubicación más larga donde se pueda colocar una palabra.
  """

  fin_juego = False
  tamanio = tablero['tamanio']
  centro = tablero['centro']
  orientacion = random.choice(('v', 'h'))
  if (tablero['primer_jugada']):
    i = centro[0]
    j = centro[1]
    ubicacion_mas_larga = [(i, j + x) if orientacion == 'h' else (i + x, j) for x in range(7)]
  else:
    ubicacion_mas_larga = []
    encontre = False
    cant = 0
    while (not encontre and not fin_juego):
      tiempo_inicio = time.time()
      i = random.randint(0, tamanio - 1)
      j = random.randint(0, tamanio - 3)
      cant += 1
      temp = []
      for x in range(7):
        posicion = (i, j + x) if orientacion == 'h' else (i + x, j)
        if (not posicion in tablero['posiciones_ocupadas'] and (posicion[0] < tamanio and posicion[1] < tamanio)):
          temp += [posicion]
        else:
          break
      if (len(temp) >= 2):
        ubicacion_mas_larga = temp
      if cant > 100 or len(ubicacion_mas_larga) == 7:
        encontre = True
      fin_juego, tablero['contador'] = actualizar_tiempo(window, tablero['contador'], time.time() - tiempo_inicio)
        
  return fin_juego, ubicacion_mas_larga
  

def buscar_palabra(longitud, tablero, window):
  """
  Función para buscar una palabra válida a partir de las fichas de la computadora.
  """

  encontrada = ''
  fin_juego = False
  for i in range(longitud, 1, -1):
    permutaciones = set("".join(permutacion) for permutacion in permutations(tablero['computadora'].fichas, i))
    tiempo_inicio = time.time()
    for permutacion in permutaciones:
      if es_palabra(tablero['nivel'], tablero['palabras_validas'], permutacion) and not fin_juego:
        encontrada = permutacion
        break
    fin_juego, tablero['contador'] = actualizar_tiempo(window, tablero['contador'], time.time() - tiempo_inicio)
    if (encontrada or fin_juego):
      break
  return fin_juego, encontrada


def ubicar_palabra(window, palabra, tablero, parametros, posiciones_ocupadas_pc):
    """
    Función que coloca en el tablero la palabra encontrada por la computadora.
    """

    bolsa_de_fichas = tablero['bolsa_de_fichas']
    computadora = tablero['computadora']
    fichas = actualizar_fichas_totales(bolsa_de_fichas)
    posiciones_atril = {}
    nuevas_fichas = computadora.fichas[:]
    for i in range(8, 15):
      letra = computadora.fichas[i-8]
      posiciones_atril[letra] = posiciones_atril[letra] + [i] if letra in posiciones_atril else [i]
    quedan = quedan_fichas(bolsa_de_fichas, len(palabra))
    for letra, posicion in zip(palabra, posiciones_ocupadas_pc):
      nuevas_fichas.remove(letra)
      x = posiciones_atril[letra][0]
      posiciones_atril[letra].remove(x)
      window[x].Update(button_color = ('white', 'red'))
      window[posicion].Update(letra, button_color = computadora.color)
      time.sleep(1)
      parametros['fin_juego'], tablero['contador'] = actualizar_tiempo(window, tablero['contador'], 1)
      if (parametros['fin_juego']):
        break
      if (quedan):
        letra_nueva = random.choice(fichas)
        while (bolsa_de_fichas[letra_nueva]['cantidad_fichas'] <= 0):
          letra_nueva = random.choice(fichas)
        nuevas_fichas += [letra_nueva]
        bolsa_de_fichas[letra_nueva]['cantidad_fichas'] -= 1
        fichas = actualizar_fichas_totales(bolsa_de_fichas)
    if (quedan and not parametros['fin_juego']):
      for i in range(8, 15):
        window[i].Update(button_color = ('white', 'green'))
      computadora.fichas = nuevas_fichas
    else:
      parametros['fin_juego'] = True
    

def repartir_nuevas_fichas(tablero, parametros, window):
    """
    Función usada para repartir nuevas fichas a la computadora.
    """

    bolsa_de_fichas = tablero['bolsa_de_fichas']
    computadora = tablero['computadora']
    if (quedan_fichas(bolsa_de_fichas)):
      if (computadora.cambios_restantes > 0):
        computadora.cambios_restantes -= 1
        for letra in computadora.fichas:
          bolsa_de_fichas[letra]['cantidad_fichas'] += 1
        computadora.fichas.clear()
        for i in range(8, 15):
          window[i].Update(button_color = ('white', 'green'))
        repartir_fichas(bolsa_de_fichas, computadora.fichas)
        parametros['historial'] += '\n\n - La computadora no pudo formar ninguna palabra, se le repartieron nuevas fichas.'
        window['historial'].Update(parametros['historial'])
        actualizar_tabla(window, tablero['jugador'], tablero['computadora'])
      else:
        parametros['fin_juego'] = True
        parametros['historial'] += '\n\n - Fin de la partida. La computadora no pudo formar ninguna palabra y no dispone de cambios suficientes.'
        window['historial'].Update(parametros['historial'])
    else:
      parametros['historial'] += '\n\n - Fin de la partida. La computadora no pudo formar ninguna palabra y no hay fichas suficientes para repartir.'
      window['historial'].Update(parametros['historial'])
      parametros['fin_juego'] = True