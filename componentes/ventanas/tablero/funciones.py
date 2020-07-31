from functools import reduce
import random, PySimpleGUI as sg
from pattern.es import parse, verbs, spelling, lexicon
import datetime, time
from random import randint
from collections import OrderedDict
from itertools import permutations
from componentes.jugador import Jugador
from os.path import join
from componentes.ventanas.general import *
from playsound import playsound as reproducir
    
    
def actualizar_tablero(window, parametros, tablero):

    window["palabra_formada"].Update(palabra_formada(tablero['jugador'].fichas, parametros['jugada']))
    window["cantidad_fichas"].Update(fichas_totales(tablero['bolsa_de_fichas']))
    
    
def actualizar_tiempo(window, contador, tiempo):

    temp = round(contador - tiempo)
    contador = 0 if temp <= 0 else temp
    window['tiempo'].Update(datetime.timedelta(seconds = contador))
    window.Refresh()
    
    return contador == 0, contador


def posicion_valida(posicion, posiciones_ocupadas, posiciones_bloqueadas, orientacion):
  '''
  Función que verifica si el usuario puede añadir una ficha al tablero o no, chequeando si
  está respetando la orientación elegida y si no está tratando de colocar la ficha en una
  posición previamente ocupada.
  '''
  
  misma_orientacion = False
  if (not posicion in posiciones_bloqueadas):
    if (not posiciones_ocupadas or posicion in posiciones_ocupadas):
      return orientacion, True
    elif ((posicion[0] - 1, posicion[1]) in posiciones_ocupadas):
      if not orientacion:
        return 'vertical', True
      else:
        misma_orientacion = orientacion == 'vertical' 
    elif ((posicion[0], posicion[1] - 1) in posiciones_ocupadas):
      if not orientacion:
        return 'horizontal', True
      else:
        misma_orientacion = orientacion == 'horizontal'
    if misma_orientacion:
      return orientacion, True
    else:
      sg.Popup('Solo se pueden agregar letras en forma horizontal, de izquierda a derecha' if orientacion == 'horizontal' else ('Solo se pueden agregar letras en forma vertical, de arriba hacia abajo' if orientacion == 'vertical' else 'Las letras sólo se pueden agregar de izquierda a derecha o de abajo hacia arriba'), **parametros_popup)
      return orientacion, False
  else:
    sg.Popup('La casilla está ocupada', **parametros_popup)
    return orientacion, False


def palabra_formada(letras, posiciones_ocupadas):
  '''
  Función que se usa para actualizar el texto mostrado en el tablero de juego que indica la palabra que
  está formando el jugador.
  '''

  return reduce(lambda anterior, posicion: anterior + letras[posicion], posiciones_ocupadas.values(), '')


def es_palabra(nivel, palabras_validas, palabra):
  '''
  Función que retorna true en caso de que la palabra sea válida para el nivel correspondiente
  '''

  palabra = palabra.lower()
  if not (palabra in verbs or (palabra in spelling and palabra in lexicon)):
    return False
  analisis = lambda palabra : parse(palabra, chunks = False).split('/')[1]
  if (nivel == 'fácil'):
    tipo = analisis(palabra)
    return tipo.find('NN') != -1 or tipo.find('VB') != -1 or tipo.find('JJ') != -1
  elif (nivel == 'medio'):
    tipo = analisis(palabra)
    return tipo.find('JJ') != -1 or tipo.find('VB') != -1
  elif (nivel == 'difícil'):
    tipo = 'JJ' if palabras_validas == 'Adjetivos' else 'VB'
    return analisis(palabra).find(tipo) != -1
      

def verificar_palabra(parametros, tablero):
  '''
  Función que verifica si la palabra ingresada por el usuario es válida, chequeando si la casilla de inicio está
  ocupada en caso de que sea la primer jugada de la partida, y chequeando que la palábra sea válida para el nivel
  '''
  
  if (tablero['primer_jugada'] and not tablero['centro'] in parametros['jugada']):
    sg.Popup('La casilla de inicio de juego no está ocupada', **parametros_popup)
    return False
  if (len(parametros['jugada']) < 2):
    sg.Popup('Palabra inválida', **parametros_popup)
    return False
  else:
    if (es_palabra(tablero['nivel'], tablero['palabras_validas'], palabra_formada(tablero['jugador'].fichas, parametros['jugada']))):
      return True
    else:
      sg.Popup('Palabra inválida', **parametros_popup)
      return False


def sumar_casilla(casillas_especiales, posicion, letra, puntos_jugada, multiplicador, tablero):
  '''
  Función que actualiza la cantidad de puntos de la jugada de la computadora, obtenidos al pasar por 
  una casilla, sumando el puntaje de la ficha. Si la casilla es especial, también se suma el modificador 
  correspondiente o se acumula el multiplicador de la palabra.
  '''
  
  tablero['posiciones_ocupadas'][posicion] = letra
  temp = tablero['bolsa_de_fichas'][letra]['puntaje']
  if (posicion in casillas_especiales):
    if (casillas_especiales[posicion]['modificador'] < 10):
      puntos_jugada += temp + casillas_especiales[posicion]['modificador']
    elif (casillas_especiales[posicion]['modificador'] < 20):
      puntos_jugada += temp * (casillas_especiales[posicion]['modificador'] % 10)
    else:
      puntos_jugada += temp
      multiplicador += (casillas_especiales[posicion]['modificador'] % 10)   
  else:
    puntos_jugada += temp
    
  return multiplicador, puntos_jugada
    

def buscar_ubicacion_mas_larga(tablero, window):

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
  

def contar_jugada(window, palabra, ubicacion_mas_larga, tablero, casillas_especiales):

    posiciones_ocupadas_pc = []
    multiplicador = puntos_jugada = 0
    for letra, posicion in zip(palabra, ubicacion_mas_larga):
        multiplicador, puntos_jugada = sumar_casilla(casillas_especiales, posicion, letra, puntos_jugada, multiplicador, tablero) 
        posiciones_ocupadas_pc += [posicion]
    puntos_jugada = 0 if puntos_jugada < 0 else (puntos_jugada if multiplicador == 0 else puntos_jugada * multiplicador)
    tablero['computadora'].puntaje += puntos_jugada
    tabla = sorted([tablero['jugador'].informacion(), tablero['computadora'].informacion()], key = lambda x : x[1], reverse = True)
    window["tabla"].Update(tabla)
    
    return posiciones_ocupadas_pc, puntos_jugada
    
        
def ubicar_palabra(window, palabra, tablero, parametros, posiciones_ocupadas_pc):

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
      
      
def finalizar_jugada(window, parametros, tablero, palabra, puntos_jugada):

    tipo = parse(palabra, chunks = False).split('/')[1] 
    tipo_palabra = 'sustantivo' if tipo.find('NN') != -1 else ('verbo' if tipo.find('VB') != -1 else 'adjetivo')
    parametros['historial'] += f'\n\n - La computadora formó la palabara "{palabra}" ({tipo_palabra}) y sumó {puntos_jugada} puntos.'
    window['historial'].Update(parametros['historial'])
    tablero['primer_jugada'] = False
    

def repartir_nuevas_fichas(tablero, parametros, window):

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
        tabla = sorted([tablero['jugador'].informacion(), tablero['computadora'].informacion()], key = lambda x : x[1], reverse = True)
        window["tabla"].Update(tabla) 
      else:
        parametros['fin_juego'] = True
        parametros['historial'] += '\n\n - Fin de la partida. La computadora no pudo formar ninguna palabra y no dispone de cambios suficientes.'
        window['historial'].Update(parametros['historial'])
    else:
      parametros['historial'] += '\n\n - Fin de la partida. La computadora no pudo formar ninguna palabra y no hay fichas suficientes para repartir.'
      window['historial'].Update(parametros['historial'])
      parametros['fin_juego'] = True



def jugar_computadora(window, parametros, tablero):
  '''
  Función que permite que la computadora pueda colocar en una orientación y posición random del tablero, la palabra de
  mayor longitud que pueda formar. De esta forma puede ganar puntos y competir contra el jugador.

  Lo primero que se hace es calcular todas las permutaciones que se pueden formar con las fichas que dispone la computadora.
  Luego se itera sobre todas esas permutaciones, desde la palabra de mayor longitud a la de menor longitud, hasta encontrar 
  una palabra válida para el nivel.
  Si no se encontró ningúna palabra válida, entonces se reparten nuevas fichas a la computadora y se actualizan los cambios
  disponibles. Si no dispone de cambios suficientes, al retornar de la función terminará la partida.
  Si se encontró una palabra válida, se elige una orientación al azar para ubicar la palabra. Si es la primer jugada, la palabra
  se ubica comenzando desde la casilla de inicio. Si no es la primer jugada, se elige una posición de inicio al azar, hasta encontrar
  una donde la palabra no ocupe alguna posición ocupada anteriormente.
  Finalmente se retornan los puntos ganados en la jugada.
  '''
  
  parametros['fin_juego'], ubicacion_mas_larga = buscar_ubicacion_mas_larga(tablero, window)
  if not parametros['fin_juego']:
    parametros['fin_juego'], palabra = buscar_palabra(len(ubicacion_mas_larga), tablero, window)
  if (palabra and not parametros['fin_juego']):
    posiciones_ocupadas_pc, puntos_jugada = contar_jugada(window, palabra, ubicacion_mas_larga, tablero, parametros['casillas_especiales'])
    ubicar_palabra(window, palabra, tablero, parametros, posiciones_ocupadas_pc)
    finalizar_jugada(window, parametros, tablero, palabra, puntos_jugada)
    if (parametros['fin_juego']):
        parametros['historial'] += '\n\n - Fin de la partida. No hay fichas suficientes para repartir.'
        window['historial'].Update(parametros['historial'])
  else:
    repartir_nuevas_fichas(tablero, parametros, window)
    
  tablero['turno'] = "jugador"
  window["turno"].Update("jugador")
    
    
def colocar_posiciones_especiales(window, tablero):
  '''
  Función que coloca todas las casillas especiales correspondiente al nivel de la partida.
  '''
  
  malas_nivel_facil =[(4, 8), (5, 9), (4, 10), (3, 9), (8, 14), (9, 13), (10, 14), (9, 15)]
  #malas_nivel_facil =[(1, 7), (1, 11), (2, 8),(2, 10), (3, 9), (17, 7), (11, 17), (8, 16), (10, 16), (9, 15)]
  multiplicador_nivel_facil = [(0,9),(1,8),(1,10),(2,7),(2,11),(3,6),(3,12),(4,5),(4,13), (9,18),(8,17),(10,17),(7,16),(11,16),(6,15),(12,15),(5,14),(13,14)]
  
  malas_nivel_medio = [(3, 7), (3, 9), (4, 8), (5, 7), (5, 9), (7, 13), (7, 11), (9, 13), (9, 11), (8, 12)]
  multiplicador_nivel_medio = [(0, 8), (1, 7), (1, 9), (2, 6), (2, 10), (3, 5), (3, 11), (8, 16), (7, 15), (9, 15), (6, 14), (10, 14), (5, 13), (11, 13)]
  
  malas_nivel_dificil=[(0,7),(1,6),(1,8),(2,5),(2,9),(3,4),(3,10),(7,14),(6,13),(8,13),(5,12),(9,12),(4,11),(10,11)]
  #malas_nivel_dificil = [(0, 5), (0, 9), (1, 6), (1, 8), (2, 7), (3, 6), (3, 8), (4, 7), (14, 5), (14, 9), (13, 6), (13, 8), (12, 7), (11, 6), (11, 8), (10, 7)]
  multiplicador_nivel_dificil = [(2,7),(3,6),(3,8),(7,12),(6,11),(8,11)]

  mala_actual = -1
  
  nivel = tablero['nivel']
  
  casillas_especiales = {}

  for i in range(tablero['tamanio']):
    for j in range(tablero['tamanio']):
      pos = (i, j)
      pos_invertida = (j, i)
      if (j == i):
        window[pos].Update('F x2', button_color = ('white', 'blue'))      
        casillas_especiales[(i, j)] = {'color' : ('white', 'blue'), 'texto' : 'F x2', 'modificador' : 12}                              
      elif (i + j == tablero['tamanio'] - 1):
        window[pos].Update('F x3', button_color = ('white', 'blue'))
        casillas_especiales[(i, j)] = {'color': ('white', 'blue'), 'texto' : 'F x3', 'modificador' : 13}
      elif (nivel == 'fácil'):
        if ((pos in malas_nivel_facil) or (pos_invertida in malas_nivel_facil)):
          window[pos].Update('F ' + str(mala_actual), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif ((pos in multiplicador_nivel_facil) or (pos_invertida in multiplicador_nivel_facil)):
          window[pos].Update('P x3' if pos in multiplicador_nivel_facil else 'P x2', button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3' if pos in multiplicador_nivel_facil else 'P x2', 'modificador' : 23 if pos in multiplicador_nivel_facil else 22}
      elif (nivel == 'medio'):
        if ((pos in malas_nivel_medio) or (pos_invertida in malas_nivel_medio)):
          window[pos].Update('F ' + str(mala_actual), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (pos in multiplicador_nivel_medio or pos_invertida in multiplicador_nivel_medio):
          window[pos].Update('P x3' if pos_invertida in multiplicador_nivel_medio else 'P x2', button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3' if pos in multiplicador_nivel_facil else 'P x2', 'modificador' : 23 if pos_invertida in multiplicador_nivel_medio else 22}
      elif (nivel == 'difícil'):
        if ((pos in malas_nivel_dificil) or (pos_invertida in malas_nivel_dificil)):
          window[pos].Update('F ' + str(mala_actual), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (pos in multiplicador_nivel_dificil or pos_invertida in multiplicador_nivel_dificil):
          window[pos].Update('P x3' if pos in multiplicador_nivel_dificil else 'P x2', button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3' if pos in multiplicador_nivel_facil else 'P x2', 'modificador' : 23 if pos in multiplicador_nivel_dificil else 22}
  
  window[tablero['centro']].Update('Inicio', button_color = ('black', 'yellow'))
  casillas_especiales[tablero['centro']] = {'color' : ('black', 'yellow'), 'texto' : 'Inicio', 'modificador' : 1}   
  
  return casillas_especiales


def repartir_fichas(bolsa_de_fichas, letras):
  '''
  Función que reparte 7 fichas de la bolsa en forma aleatoria.
  Los jugadores reciben más vocales que consonantes para que 
  tengan mayor posibilidad de formar palabras.
  '''
  
  letras.clear()
  fichas = actualizar_fichas_totales(bolsa_de_fichas)
  for i in range(7):
    letra = random.choice(fichas)
    while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
      letra = random.choice(fichas)
    letras += [letra]
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
    fichas = actualizar_fichas_totales(bolsa_de_fichas)


def contar_puntos_jugador(parametros, tablero):
  '''
  Función que retorna la cantidad de puntos de una jugada, teniendo en cuenta
  las casillas especiales (modificadores)
  '''
  jugada = parametros['jugada']
  bolsa_de_fichas = tablero['bolsa_de_fichas']
  letras_jugador = tablero['jugador'].fichas
  casillas_especiales = parametros['casillas_especiales']
  for posicion in jugada:
    tablero['posiciones_ocupadas'][posicion] = letras_jugador[jugada[posicion]]
  multiplicador = 0
  puntos = 0
  for posicion in jugada:
    temp = bolsa_de_fichas[letras_jugador[jugada[posicion]]]['puntaje']
    if (posicion in casillas_especiales):
      if (casillas_especiales[posicion]['modificador'] < 10):
        puntos += temp + casillas_especiales[posicion]['modificador']
      elif (casillas_especiales[posicion]['modificador'] < 20):
        puntos += temp * (casillas_especiales[posicion]['modificador'] % 10)
      else:
        multiplicador += (casillas_especiales[posicion]['modificador'] % 10)
        puntos += temp
    else:
      puntos += temp
  if (puntos < 0):
    return 0
  else:
    return puntos if multiplicador == 0 else puntos * multiplicador

    
def fichas_totales(bolsa_de_fichas):
  '''
  Función que retorna la cantidad total de fichas que quedan en la bolsa.
  '''

  total = 0
  for letra in bolsa_de_fichas:
    total += bolsa_de_fichas[letra]['cantidad_fichas'] 
  return total  


def finalizar_partida(window, tablero):
  '''
  Función que muestra el mensaje de fin de la partida, detallando los puntos
  de la computadora y del jugador.
  '''
  jugador = tablero['jugador']
  computadora = tablero['computadora']
  bolsa_de_fichas = tablero['bolsa_de_fichas']
  
  for letra_jugador, letra_pc in zip(jugador.fichas, computadora.fichas):
      jugador.puntaje -= bolsa_de_fichas[letra_jugador]['puntaje']
      computadora.puntaje -= bolsa_de_fichas[letra_pc]['puntaje']
    
  tabla = sorted([jugador.informacion(), computadora.informacion()], key = lambda x : x[1], reverse = True) 
  window['tabla'].Update(tabla)

  for i, letra in zip(range(8, 15), computadora.fichas):
      window[i].Update(letra, disabled = False)
      
  for key in ('Iniciar', 'Posponer', 'Pausa', 'Terminar', 'confirmar', 'cambiar', 'pasar'):
    window[key].Update(button_color = sg.DEFAULT_BUTTON_COLOR, disabled = True)

  mensaje = ''
  if (jugador.puntaje > computadora.puntaje):
    mensaje = f'Ganó el jugador con {jugador.puntaje} puntos'
  elif (jugador.puntaje < computadora.puntaje):
    mensaje = f'Ganó la computadora con {computadora.puntaje} puntos'
  else: 
    mensaje = 'Hubo un empate'
  sg.Popup(mensaje, title = 'Fin de la partida')
  
  window['Salir'].Update(visible = True)


def ventana_cambio_fichas(letras_jugador):

    layout_cambiar_fichas = [[sg.Button('Cambiar todas', key = 'todas')],
                           [sg.Text('')],
                           [sg.Text('Seleccione las fichas que quiere intercambiar')],
                           [sg.Button(letras_jugador[i], size= (3, 1), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)],
                           [sg.Text('')],
                           [sg.Button('Aceptar'), sg.Button('Salir')]]
    return sg.Window('Cambiar fichas', layout_cambiar_fichas, **parametros_ventana)
    
    
def reiniciar_parametros(parametros):

    parametros["letra_seleccionada"] = False
    parametros["orientacion"] = parametros["primer_posicion"] = parametros["ultima_posicion"] = ''
    parametros["jugada"] = OrderedDict()


def cambiar_fichas(window, tablero, parametros):
  '''
  Esta función muestra una ventana para que el jugador pueda cambiar algunas o todas sus fichas.
  En caso de haber hecho algún cambio, actualiza las fichas del atril.
  '''

  jugador = tablero['jugador']
  letras_jugador = jugador.fichas
  bolsa_de_fichas = tablero['bolsa_de_fichas']
  
  if parametros['jugada']:
    sg.Popup("Primero debe levantar sus fichas", **parametros_popup)
    return

  ventana = ventana_cambio_fichas(letras_jugador)

  fichas = actualizar_fichas_totales(bolsa_de_fichas)

  seleccionadas = {}

  while True:
    event, values, tiempo = leer_evento(ventana, 1000, 'pasar')
    parametros['fin_juego'], tablero['contador'] = actualizar_tiempo(window, tablero['contador'], tiempo)
    if (parametros['fin_juego']):
      break
    elif (event == 'pasar'):
      continue
    elif (event in ('Salir', None)):
      break
    elif (event == 'todas'):
      if (quedan_fichas(bolsa_de_fichas)):
        for letra in letras_jugador:
          bolsa_de_fichas[letra]['cantidad_fichas'] += 1
        letras_jugador.clear()
        repartir_fichas(bolsa_de_fichas, letras_jugador)
        for i in range (7):
          window[i].Update(letras_jugador[i], button_color = ('white', 'green'))
        parametros['historial'] += '\n\n - Se cambiaron todas las fichas del jugador.'
        window['historial'].Update(parametros['historial'])
        break
      else:
        sg.Popup('No quedan suficientes fichas en la bolsa', **parametros_popup)
    elif (event == 'Aceptar'):
      if (not seleccionadas):
        sg.Popup('Debe seleccionar alguna letra', **parametros_popup)
      else:
        if (quedan_fichas(bolsa_de_fichas, len(seleccionadas))):
          for i in seleccionadas:
            bolsa_de_fichas[seleccionadas[i]]['cantidad_fichas'] += 1
            letra = random.choice(fichas)
            while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
              letra = random.choice(fichas)
            bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
            window[i].Update(letra, button_color = ('white', 'green'))
            letras_jugador[i] = letra
            fichas = actualizar_fichas_totales(bolsa_de_fichas)
          parametros['historial'] += '\n\n - Se cambiaron algunas fichas del jugador.'
          window['historial'].Update(parametros['historial'])
          break
        else:
          sg.Popup('No quedan suficientes fichas en la bolsa', **parametros_popup)
    else:
      if (event in seleccionadas):
        ventana[event].Update(button_color = ('white', 'green'))
        del seleccionadas[event]
      else:
        ventana[event].Update(button_color = ('white', 'red'))
        seleccionadas[event] = letras_jugador[event]
  ventana.Close()
  
  if not event in (None, 'Salir'):  
    jugador.cambios_restantes -= 1
    tabla = sorted([tablero['jugador'].informacion(), tablero['computadora'].informacion()], key = lambda x : x[1], reverse = True)
    window["tabla"].Update(tabla)
    reiniciar_parametros(parametros)
    if not jugador.cambios_restantes:
        window["cambiar"].Update(disabled = True, button_color = ("white", "red"))
    tablero['turno'] = 'computadora'
    window['turno'].Update('computadora')

def restaurar_tablero(window, posiciones):
    '''
    Función que restaura las posiciones ocupadas del tablero, en caso de haber
    reanudado una partida anterior.
    '''

    for posicion in posiciones:
        window[posicion].Update(posiciones[posicion], button_color = ('white', 'red')) # button_text, button_color


def quedan_fichas(bolsa_de_fichas, cantidad_fichas = 7):
    '''
    Función que chequea si hay suficientes fichas en la bolsa para repartir.
    '''

    contador = 0
    for letra in bolsa_de_fichas:
        contador += bolsa_de_fichas[letra]['cantidad_fichas']
        if (contador >= cantidad_fichas):
            return True
    return False
    
def pasar(window, parametros, tablero):

    if parametros['jugada']:
        sg.Popup("Primero debe levantar sus fichas")
    else:
        if parametros['letra_seleccionada']:
            window[parametros['letra']].Update(button_color = ("white", "green"))
            parametros['letra_seleccionada'] = False
        tablero['turno'] = 'computadora'
        window['turno'].Update('computadora')
            
def confirmar_palabra(window, parametros, tablero):
    
    fichas = actualizar_fichas_totales(tablero['bolsa_de_fichas'])
    letras_jugador = tablero['jugador'].fichas
    if parametros['letra_seleccionada']:
        window[parametros['letra']].Update(button_color = ("white", "green"))
        parametros['letra_seleccionada'] = False
    if verificar_palabra(parametros, tablero):
        tablero['primer_jugada'] = False
        puntos_jugada = contar_puntos_jugador(parametros, tablero)
        palabra = palabra_formada(letras_jugador, parametros['jugada'])
        tipo = parse(palabra).split('/')[1] 
        tipo_palabra = 'sustantivo' if tipo == 'NN' else ('verbo' if tipo == 'VB' else 'adjetivo')
        parametros['historial'] += f'\n\n - El jugador formó la palabara "{palabra}" ({tipo_palabra}) y sumó {puntos_jugada} puntos.'
        window['historial'].Update(parametros['historial'])
        tablero['jugador'].puntaje += puntos_jugada
        jugada = parametros['jugada']
        reiniciar_parametros(parametros)
        if quedan_fichas(tablero['bolsa_de_fichas'], len(jugada)):
            for posicion in jugada:
                letra = random.choice(fichas)
                while tablero['bolsa_de_fichas'][letra]["cantidad_fichas"] <=  0:
                    letra = random.choice(fichas)
                letras_jugador[jugada[posicion]] = letra
                window[jugada[posicion]].Update(
                    letra, disabled = False, button_color = ("white", "green")
                )
                tablero['bolsa_de_fichas'][letra]["cantidad_fichas"] -=  1
                fichas = actualizar_fichas_totales(tablero['bolsa_de_fichas'])
            tablero['turno'] = 'computadora'
            window['turno'].Update('computadora')
        else:
            parametros['fin_juego'] = True
            parametros['historial'] += '\n\n - Fin de la partida. No quedan suficientes fichas para repartir.'
            window['historial'].Update(parametros['historial'])
        tabla = sorted([tablero['jugador'].informacion(), tablero['computadora'].informacion()], key = lambda x : x[1], reverse = True)
        window["tabla"].Update(tabla)

def inicializar_parametros(configuracion, partida_anterior):

  if not partida_anterior:
    tablero = {
      "posiciones_ocupadas" : {},
      "palabras_usadas" : [],
      "jugador" : Jugador("Jugador", ('white', 'blue')),
      "computadora" : Jugador("Computadora", ('white', 'red')),
      "turno" : random.choice(('computadora', 'jugador')),
      "contador" : configuracion['tiempo'] * 60,
      "bolsa_de_fichas" : configuracion['fichas'],
      "primer_jugada" : True,
      "nivel" : configuracion['nivel'],
      "tamanio" : 15 if configuracion['nivel'] ==  "difícil" else (17 if configuracion['nivel'] ==  "medio" else 19),
      "centro" : (7, 7) if configuracion['nivel'] ==  "difícil" else ((8, 8) if configuracion['nivel'] ==  "medio" else (9, 9)),
      "palabras_validas" : configuracion['palabras_validas']
    }
    repartir_fichas(tablero['bolsa_de_fichas'], tablero['jugador'].fichas)
    repartir_fichas(tablero['bolsa_de_fichas'], tablero['computadora'].fichas)
  else:
    tablero = partida_anterior
  parametros = {
    "letra_seleccionada" : False,
    "orientacion" : '',
    "primer_posicion" : '',
    "ultima_posicion" : '',
    "jugada" : OrderedDict(),
    "letra" : '',
    "historial" : '                  Historial de la partida',
    "fichas_totales" : actualizar_fichas_totales(tablero['bolsa_de_fichas']),
    "fin_juego" : False,
  }
  
  return tablero, parametros
        
def actualizar_fichas_totales(bolsa_de_fichas):
    
    return "".join([letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas])
    
def crear_ventana_tablero(tablero, parametros, partida_anterior):

    tablero_juego = [
        [
            sg.Button("", size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ("white", "green"),)
            for j in range(tablero['tamanio'])
        ]
        for i in range(tablero['tamanio'])
    ]

    fichas_jugador = [
        sg.Button(tablero['jugador'].fichas[i], size = (3, 1), key = i, pad = (0.5, 0.5), button_color = ("white", "green"),)
        for i in range(7)
    ]

    fichas_pc = [
        sg.Button("?", size = (3, 1), key = i + 8, pad = (0.5, 0.5), button_color = ("white", "green"))
        for i in range(7)
    ]

    layout_columna1 = [[sg.Text("Fichas de la computadora")]] + [fichas_pc] + [[sg.Text(" ")]] + [x for x in tablero_juego]
    layout_columna1 += [[sg.Text('')]] + [[sg.Text("Fichas del jugador")]] + [fichas_jugador] + [[sg.Text('')]]
    layout_columna1 +=  [
        [
            sg.Button("Iniciar",),
            sg.Button("Posponer"),
            sg.Button("Pausa", disabled = True),
            sg.Button("Terminar"),
            sg.Button("Salir", button_color = ('white', 'red'), visible = False),
        ]
    ]

    columna1 = layout_columna1
    
    tabla = sorted([tablero['jugador'].informacion(), tablero['computadora'].informacion()], key = lambda x : x[1], reverse = True)
    
    titulo = {'font' : ("Consolas", 12), 'background_color' : '#1d3557', 'size' : (40, 1)}
    fuente = ("Helvetica", 11)
    nivel = tablero['nivel']

    columna2 = [
        [sg.Text("Tiempo restante", **titulo)], 
        [sg.Text(datetime.timedelta(seconds = tablero['contador']), key = "tiempo", font = fuente)],
        [sg.Text("Nivel", **titulo)],
        [sg.Text(nivel.capitalize(), font = fuente)],
        [sg.Text("Palabras válidas", **titulo)],
        [sg.Text(tablero['palabras_validas'], font = fuente)],
        [sg.Text("Cantidad de fichas en la bolsa", **titulo)], 
        [sg.Text(fichas_totales(tablero['bolsa_de_fichas']), font = fuente, key = "cantidad_fichas")],
        [sg.Text("Turno", **titulo)],
        [sg.Text(tablero['turno'], key = 'turno', font = fuente)],
        [sg.Text('')],
        [sg.Table(tabla, ["", "Puntaje", "Cambios restantes"], key = 'tabla', justification = 'center', num_rows = 2, hide_vertical_scroll = True)],
        [sg.Text('')],
        [sg.Multiline(parametros['historial'], size = (37, 10), key = 'historial', disabled = True, autoscroll = True)],
        [sg.Text('')],
        [
            sg.Button("Confirmar palabra", key = "confirmar"),
            sg.Button("Cambiar fichas", key = "cambiar"),
            sg.Button("Pasar", key = "pasar"),
        ],
    ]

    layout = [[sg.Column(columna1, **parametros_columna), sg.Column(columna2, pad = ((20, 0), (0, 0)), **parametros_columna)]]

    window = sg.Window("Tablero", layout, **parametros_ventana)
    
    parametros['casillas_especiales'] = colocar_posiciones_especiales(window, tablero) # {(i, j) : {'color' : ('white', 'blue'), 'texto' : 'F +2', 'modificador' : 2}}

    if partida_anterior:
        restaurar_tablero(window, tablero["posiciones_ocupadas"])
        
    return window
        
def iniciar_partida(window, parametros, partida_anterior):

    parametros['historial'] += '\n\n - El jugador ' + ('reanudó' if partida_anterior else 'inició') + ' la partida.'
    window['historial'].Update(parametros['historial'])
    window["Iniciar"].Update(disabled = True)
    window["Pausa"].Update(disabled = False)
    return True
    
def pausar(window, comenzar):

   window["Pausa"].Update(button_color = ("white", "red") if comenzar else sg.DEFAULT_BUTTON_COLOR)
   
   return not comenzar
   
def posponer(tablero, jugada):

    if (not jugada):
        sg.Popup("Se guardaron los datos de la partida", title = "Atención")
        return True, tablero
    else:
      sg.Popup("Primero debe levantar sus fichas", title = "Atención")
      return False, None
      
def seleccionar_ficha(window, parametros, event):

    if parametros['letra_seleccionada']:
        window[parametros['letra']].Update(button_color = ("white", "green"))
    window[event].Update(button_color = ("white", "red"))
    parametros['letra'] = event
    parametros['letra_seleccionada'] = True
    
def colocar_ficha(window, parametros, tablero, event):

    if parametros['letra_seleccionada']:
        parametros['orientacion'], es_valida = posicion_valida(event, parametros['jugada'], tablero['posiciones_ocupadas'], parametros['orientacion'])
        if es_valida:
            if event in parametros['jugada']:
                window[parametros['jugada'][event]].Update(button_color = ("white", "green"), disabled = False)
            else:
                parametros['ultima_posicion'] = event
            window[event].Update(tablero['jugador'].fichas[parametros['letra']], button_color = ("white", "red"))
            parametros['jugada'][event] = parametros['letra']
            window[parametros['letra']].Update(disabled = True)
            parametros['letra_seleccionada'] = False
            if len(parametros['jugada']) ==  1:
                parametros['primer_posicion'] = parametros['ultima_posicion'] = event
    else:
        if event in (parametros['primer_posicion'], parametros['ultima_posicion']):
            casillas_especiales = parametros['casillas_especiales']
            window[event].Update(
                casillas_especiales[event]["texto"] if event in casillas_especiales else " ",
                button_color = casillas_especiales[event]["color"]
                if event in casillas_especiales
                else ("white", "green"),
                disabled = False,
            )
            window[parametros['jugada'][event]].Update(button_color = ("white", "green"), disabled = False)
            del parametros['jugada'][event]
            if len(parametros['jugada']) <=  1:
                parametros['orientacion'] = ''
                if not parametros['jugada']:
                    parametros['primer_posicion'] = parametros['ultima_posicion'] = ()
            if event == parametros['primer_posicion']:
                parametros['primer_posicion'] = (
                    (event[0] + 1, event[1]) if parametros['orientacion'] == 'vertical' else (event[0], event[1] + 1)
                )
            else:
                parametros['ultima_posicion'] = (
                    (event[0] - 1, event[1]) if parametros['orientacion'] == 'vertical' else (event[0], event[1] - 1)
                )
