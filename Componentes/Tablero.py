import random, PySimpleGUI as sg
from Componentes.Jugador import Jugador
from random import randint
from pattern.es import parse, verbs, spelling, lexicon
from collections import OrderedDict
from itertools import permutations
import sys, datetime
from functools import reduce

def posicion_valida(event, posiciones_ocupadas, orientacion, posiciones_bloqueadas):
  '''
  Función que verifica si el usuario puede añadir una ficha al tablero o no, chequeando si
  está respetando la orientación elegida y si no está tratando de colocar la ficha en una
  posición previamente ocupada.
  '''
  if (not event in posiciones_bloqueadas):
    if (len(posiciones_ocupadas) == 0):
      return True
    if (event in posiciones_ocupadas):
      return True
    if ((event[0] - 1, event[1]) in posiciones_ocupadas):
      if (orientacion[0]):
        orientacion[0] = False
        return True
      elif (not orientacion[1]):
        return True
    elif ((event[0], event[1] - 1) in posiciones_ocupadas):
      if (orientacion[0]):
        orientacion[0] = False
        orientacion[1] = True
        return True
      elif (orientacion[1]):
        return True  
  sg.Popup('Solo se pueden agregar letras en forma horizontal' if orientacion[1] else 'Solo se pueden agregar letras en forma vertical', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
  return False

def palabra_formada(letras, posiciones_ocupadas):
  '''
  Función que se usa para actualizar el texto mostrado en el tablero de juego que indica la palabra que
  está formando el jugador.
  '''
  str = ''
  for clave in posiciones_ocupadas:
    str += letras[posiciones_ocupadas[clave]]
  return str

def es_palabra(nivel, palabras_validas, str):
  '''
  Función que retorna true en caso de que la palabra sea válida para el nivel correspondiente
  '''
  str = str.lower()
  if (nivel == 'facil'):
    return (str in verbs or (str in spelling and str in lexicon))
  elif (nivel == 'medio'):
    return (parse(str).split('/')[1] != 'NN' and (str in verbs or (str in spelling and str in lexicon))) 
  elif (nivel == 'dificil'):
    tipo = 'JJ' if palabras_validas == 'adjetivos' else 'VB'
    return (parse(str).split('/')[1] == tipo and (str in verbs or (str in spelling and str in lexicon))) 
      

def verificar_palabra(letras, posiciones_ocupadas, posiciones_bloqueadas, centro, primer_jugada, nivel, palabras_validas):
  '''
  Función que verifica si la palabra ingresada por el usuario es válida, chequeando si la casilla de inicio está
  ocupada en caso de que sea la primer jugada de la partida, y chequeando que la palábra sea válida para el nivel
  '''
  if (primer_jugada and not centro in posiciones_ocupadas):
    sg.Popup('La casilla de inicio de juego no está ocupada', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
    return False
  if (len(posiciones_ocupadas) < 2):
    sg.Popup('Palabra inválida', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
    return False
  else:
    str = ''
    for clave in posiciones_ocupadas:
      str += letras[posiciones_ocupadas[clave]]
    if (es_palabra(nivel, palabras_validas, str)):
      return True
    else:
      sg.Popup('Palabra inválida', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
      return False

def sumar_casilla(window, bolsa_de_fichas, casillas_especiales, posicion, letra, puntos_jugada, multiplicador, posiciones_bloqueadas, posiciones):
  '''
  Función que actualiza la cantidad de puntos de la jugada de la computadora, obtenidos al pasar por 
  una casilla, sumando el puntaje de la ficha. Si la casilla es especial, también se suma el modificador 
  correspondiente o se acumula el multiplicador de la palabra.
  '''
  window.Element(posicion).Update(letra, button_color = ('white', 'red'))
  posiciones[posicion] = letra
  puntos_jugada[0] += bolsa_de_fichas[letra]['puntaje_ficha']
  posiciones_bloqueadas += [posicion]
  if (posicion in casillas_especiales):
    if (casillas_especiales[posicion]['modificador'] < 10):
      puntos_jugada[0] += casillas_especiales[posicion]['modificador']
    else:
      multiplicador[0] += (casillas_especiales[posicion]['modificador'] % 10)

def jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas, computadora, window, FILAS, COLUMNAS, posiciones, nivel, palabras_validas):
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
  orientacion = random.randint(0, 100) % 2 == 0   # Si es par la orientacion es horizontal
  abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  print('letras pc:', letras_pc)
  puntos_jugada = [0]
  multiplicador = [0]
  if (primer_jugada):
    i = centro[0]
    j = centro[1]
  permutaciones = permutations(letras_pc)
  encontre = False
  for permutacion in permutaciones:
    if (encontre):
      break
    temp = ''.join(permutacion)
    for x in range(7, 1, -1):
      palabra = temp[0 : x + 1]
      if (es_palabra(nivel, palabras_validas, palabra)):
        encontre = True
        break
  encontre = encontre and len(palabra) > 1
  if (encontre):
    print(palabra, es_palabra(nivel, palabras_validas, palabra))
    if (primer_jugada):
      for letra in palabra:
        sumar_casilla(window, bolsa_de_fichas, casillas_especiales, (i, j), letra, puntos_jugada, multiplicador, posiciones_bloqueadas, posiciones) 
        j += 1 if orientacion else 0
        i += 1 if not orientacion else 0
    else:
      posicion_valida = False
      while (not posicion_valida):
        posicion_valida = True
        i = random.randint(0, FILAS - 1) if orientacion else random.randint(0, FILAS - 9)
        j = random.randint(0, COLUMNAS - 9) if orientacion else random.randint(0, COLUMNAS - 1)
        for x in range(len(palabra)):
          pos = (i, j + x) if orientacion else (i + x, j)
          if (pos in posiciones_bloqueadas):
            posicion_valida = False
            break
      for letra in palabra:
        sumar_casilla(window, bolsa_de_fichas, casillas_especiales, (i, j), letra, puntos_jugada, multiplicador, posiciones_bloqueadas, posiciones) 
        j += 1 if orientacion else 0
        i += 1 if not orientacion else 0
    fichas_usadas_pc.clear()
    for letra in palabra:
      x = random.randint(8, 14)
      while (x in fichas_usadas_pc):
        x = random.randint(8, 14)
        print('aca')
      window.Element(x).Update(button_color = ('white', 'red'))
      fichas_usadas_pc += [x]
      letras_pc.remove(letra)
      letra_nueva = random.choice(abecedario)
      while (bolsa_de_fichas[letra_nueva]['cantidad_fichas'] <= 0):
        letra_nueva = random.choice(abecedario)
      letras_pc += [letra_nueva]
      bolsa_de_fichas[letra_nueva]['cantidad_fichas'] -= 1
    print(puntos_jugada[0], '*', multiplicador[0])
    for i in range(8, 15):
      window.Element(i).Update(button_color = ('white', 'green'), disabled = True)
    puntos_jugada = 0 if puntos_jugada[0] < 0 else (puntos_jugada[0] if multiplicador[0] == 0 else puntos_jugada[0] * multiplicador[0])
    sg.Popup(f'Palabra formada por la computadora: {palabra}\nPuntos sumadados: {puntos_jugada}', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
    return puntos_jugada
  else:
    if (computadora.get_cambios_restantes() > 0):
      computadora.actualizar_cambios_restantes()
      for letra in letras_pc:
        bolsa_de_fichas[letra]['cantidad_fichas'] += 1
      letras_pc.clear()
      fichas_usadas_pc.clear()
      for i in range(8, 15):
        window.Element(i).Update(button_color = ('white', 'green'), disabled = True)
      repartir_fichas(bolsa_de_fichas, letras_pc)
      sg.Popup('Se repartieron nuevas fichas a la computadora', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
      print('nuevas letras pc', letras_pc)
      window.Element('cambios_pc').Update(computadora.get_cambios_restantes())
      return 0   
    else:
      return -1 

def colocar_posiciones_especiales(tablero_juego, nivel, casillas_especiales, FILAS, COLUMNAS, centro):
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

  for i in range(FILAS):
    for j in range(COLUMNAS):
      posicion = (i, j)
      posicion_invertida = (j, i)
      if(j == i):
        tablero_juego[i][j] = sg.Button('F +2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'blue'))
        casillas_especiales[(i, j)] = {'color' : ('white', 'blue'), 'texto' : 'F +2', 'modificador' : 2}
      elif(i + j == FILAS - 1):
        tablero_juego[i][j] = sg.Button('F +3', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'blue'))
        casillas_especiales[(i, j)] = {'color': ('white', 'blue'), 'texto' : 'F +3', 'modificador' : 3}
      elif (nivel == 'facil'):
        if ((posicion in malas_nivel_facil) or (posicion_invertida in malas_nivel_facil)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif ((posicion in multiplicador_nivel_facil) or (posicion_invertida in multiplicador_nivel_facil)):
          tablero_juego[i][j] = sg.Button('P x3' if posicion in multiplicador_nivel_facil else 'P x2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)]={'color': ('white', 'purple'), 'texto' : 'P x3', 'modificador' : 13 if posicion in multiplicador_nivel_facil else 12}
      elif (nivel == 'medio'):
        if ((posicion in malas_nivel_medio) or (posicion_invertida in malas_nivel_medio)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (posicion in multiplicador_nivel_medio or posicion_invertida in multiplicador_nivel_medio):
          tablero_juego[i][j] = sg.Button('P x3' if posicion_invertida in multiplicador_nivel_medio else 'P x2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3', 'modificador' : 13 if posicion_invertida in multiplicador_nivel_medio else 12}
      elif (nivel == 'dificil'):
        if ((posicion in malas_nivel_dificil) or (posicion_invertida in malas_nivel_dificil)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (posicion in multiplicador_nivel_dificil or posicion_invertida in multiplicador_nivel_dificil):
          tablero_juego[i][j] = sg.Button('P x3' if posicion in multiplicador_nivel_dificil else 'P x2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3', 'modificador' : 13 if posicion in multiplicador_nivel_dificil else 12}
          
  tablero_juego[centro[0]][centro[1]] = sg.Button('Inicio', size = (4, 2), key = (centro[0], centro[1]), pad = (0.5, 0.5), button_color = ('white', 'yellow'))
  casillas_especiales[(centro[0], centro[1])] = {'color' : ('white', 'yellow'), 'texto' : 'Inicio', 'modificador' : 1}          

def repartir_fichas(bolsa_de_fichas, letras):
  '''
  Función que reparte 7 fichas de la bolsa en forma aleatoria.
  Los jugadores reciben más vocales que consonantes para que 
  tengan mayor posibilidad de formar palabras.
  '''
  abecedario = list('AAAABCDEEEEFGHIIIIJKLMNOOOOPQRSTUUUUVWXYZ')    # las vocales se repiten para que sea más probable que "random.choice" elija una vocal
  for i in range(7):
    letra = random.choice(abecedario)
    while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):         
      letra = random.choice(abecedario)
    letras += [letra]
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1

def contar_puntos_jugador(posiciones_ocupadas, casillas_especiales, bolsa_de_fichas, letras_jugador):
  '''
  Función que retorna la cantidad de puntos de una jugada, teniendo en cuenta
  las casillas especiales (modificadores)
  '''
  multiplicador = 0
  puntos = 0
  for posicion in posiciones_ocupadas:
    puntos += bolsa_de_fichas[letras_jugador[posiciones_ocupadas[posicion]]]['puntaje_ficha']
    if (posicion in casillas_especiales):
      if (casillas_especiales[posicion]['modificador'] < 10):
        puntos += casillas_especiales[posicion]['modificador']
      else:
        multiplicador += (casillas_especiales[posicion]['modificador'] % 10)
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

def imprimir_mensaje_fin(jugador, computadora):
  '''
  Función que muestra el mensaje de fin de la partida, detallando los puntos
  de la computadora y del jugador.
  '''
  mensaje = '¡Fin de la partida!' + ('\n La computadora no puede formar ninguna palabra y no dispone de más cambios \n' if computadora.get_cambios_restantes() == -1 else '\n')
  if (jugador.get_puntaje() > computadora.get_puntaje()):
    mensaje += f'Ganó el jugador con {jugador.get_puntaje()}'
  if (jugador.get_puntaje() < computadora.get_puntaje()):
    mensaje += f'Ganó la computadora con {computadora.get_puntaje()} puntos'
  if (jugador.get_puntaje() == computadora.get_puntaje()):
    mensaje += 'Hubo un empate'
  sg.Popup(mensaje, title = 'Atención')

def cambiar_fichas(jugador, letras_jugador, bolsa_de_fichas, contador, window):
  '''
  Esta función muestra una ventana para que el jugador pueda cambiar algunas o todas sus fichas.
  En caso de haber hecho algún cambio, ctualiza las fichas del atril.
  '''
  layout_cambiar_fichas = [[sg.Button('Cambiar todas', key = 'todas'), sg.Button('Cambiar algunas', key = 'algunas')],
                           [sg.Text('Seleccione las fichas que quiere intercambiar')],
                           [sg.Button(letras_jugador[i], size= (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green'), disabled = True) for i in range(7)],
                           [sg.Button('Aceptar', disabled = True, button_color = ('white', 'red')), sg.Button('Salir')]]
  ventana = sg.Window('Cambiar fichas', layout_cambiar_fichas)

  abecedario = list('AAAAABCDEEEEEFGHIIIIIJKLMNOOOOOPQRSTUUUUUVWXYZ')

  seleccionadas = {}

  cambio = algunas = False

  while True:
    event = ventana.Read(timeout = 1000)[0]
    contador -= 1
    window.Element('tiempo').Update(contador)
    if (contador == 0):
      break
    if (event == '__TIMEOUT__'):
      continue
    if (event in ('Salir', None)):
      break
    if (event == 'todas'):
      for letra in letras_jugador:
        bolsa_de_fichas[letra]['cantidad_fichas'] += 1
      letras_jugador.clear()
      repartir_fichas(bolsa_de_fichas, letras_jugador)
      for i in range (7):
        window.Element(i).Update(letras_jugador[i], button_color = ('white', 'green'))
      sg.Popup('Se cambiaron todas las fichas del jugador', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
      cambio = True
      break
    elif (event == 'algunas'):
      if (not algunas):
        ventana.Element('todas').Update(disabled = True, button_color = ('white', 'red'))
        ventana.Element('Aceptar').Update(disabled = False, button_color = ('white', 'green')) 
        for i in range(7):
          ventana.Element(i).Update(disabled = False)
        algunas = True
      else:
        ventana.Element('todas').Update(disabled = False, button_color = ('white', 'green'))
        ventana.Element('Aceptar').Update(disabled = True, button_color = ('white', 'red')) 
        for i in range(7):
          ventana.Element(i).Update(disabled = True)
        algunas = False
    elif (event == 'Aceptar'):
      if (len(seleccionadas) == 0):
        sg.Popup('Debe seleccionar alguna letra', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
      else:
        for i in seleccionadas:
          bolsa_de_fichas[seleccionadas[i]]['cantidad_fichas'] += 1
          letra = random.choice(abecedario)
          while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
            letra = random.choice(abecedario)
          bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
          window.Element(i).Update(letra, button_color = ('white', 'green'))
          letras_jugador[i] = letra
        sg.Popup('Se cambiaron algunas fichas del jugador', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
        cambio = True
        break
    else:
      if (event in seleccionadas):
        ventana.Element(event).Update(button_color = ('white', 'green'))
        del seleccionadas[event]
      else:
        ventana.Element(event).Update(button_color = ('white', 'red'))
        seleccionadas[event] = letras_jugador[event]
  ventana.Close()
  
  return (cambio, contador)

def restaurar_tablero(window, posiciones):
    '''
    Función que restaura las posiciones ocupadas del tablero, en caso de haber
    reanudado una partida anterior.
    '''
    for posicion in posiciones:
        window.Element(posicion).Update(posiciones[posicion], button_color = ('white', 'red'))

def jugar(configuracion, partida):

    '''
    Esta es la función "principal", donde se crea el tablero de juego y se desarrolla la lógica más importante del mismo.
    Recibe la configuración elegida para la partida, y la partida guardada, en caso de que el usuario haya elegido reanudar
    la partida anterior.

    El parámetro "partida" es un diccionario que contiene la información necesaria para reconstruir el estado del tablero
    de la partida anterior. Si es None, significa que el usuario empezó una nueva partida. El parámetro "configuración" es
    otro diccionario que almacena las configuraciones de la partida.

    En caso de que "partida" sea distinto de None, el usuario eligió reanudar la partida anterior, por lo tanto las variables
    se inicializarán con los valores correspondientes del diccionario.

    Si "partida" es None, las variables se inicializarán con los valores correspondientes del diccionario "configuración".
    '''

    if (partida != None):
      for i in partida:
        print(i, partida[i])

    nivel = configuracion['nivel'] if partida == None else partida['nivel']
    FILAS = COLUMNAS = 15 if nivel == 'dificil' else (17 if nivel == 'medio' else 19)
    print('NIVEL', nivel, 'FILAS', FILAS)
    centro = (int(FILAS / 2), int(FILAS / 2))
    abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    palabras_validas = configuracion['palabras validas'] if partida == None else partida['palabras validas']
    contador = configuracion['tiempo'] * 60 if partida == None else partida['contador'] # contador en segundos
    bolsa_de_fichas = {letra : {'cantidad_fichas' : int(configuracion['fichas'][letra]['cantidad_fichas']), 'puntaje_ficha' : int(configuracion['fichas'][letra]['puntaje'])} for letra in abecedario} if partida == None else partida['bolsa de fichas'] 

    print('Fichas totales:', fichas_totales(bolsa_de_fichas))
    if (partida == None):
        letras_jugador = []
        letras_pc = []
        repartir_fichas(bolsa_de_fichas, letras_jugador)
        repartir_fichas(bolsa_de_fichas, letras_pc)
    else:
        letras_jugador = partida['letras jugador']
        letras_pc = partida['letras computadora']
    print('Fichas totales:', fichas_totales(bolsa_de_fichas))

    tablero_juego = [[sg.Button('', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'green')) for j in range(COLUMNAS)] for i in range(FILAS)]

    casillas_especiales = {}
    colocar_posiciones_especiales(tablero_juego, nivel, casillas_especiales, FILAS, COLUMNAS, centro)

    fichas_jugador = [sg.Button(letras_jugador[i], size = (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

    fichas_pc = [sg.Button('?', size= (4, 2), key = i + 8, pad = (0.5, 0.5), button_color = ('white', 'green'), disabled = True) for i in range(7)]

    layout = [[sg.Text('Fichas de la computadora')]] + [fichas_pc] + [[sg.Text(' ')]] + [x for x in tablero_juego] 
    layout += [[sg.Text('Fichas del jugador')]] + [fichas_jugador]
    layout += [[sg.Button('Comenzar', button_color = ('white', 'green')), sg.Button('Posponer'), sg.Button('Pausa'), sg.Button('Terminar')]]

    columna1 = layout

    computadora = Jugador() if partida == None else partida['computadora']
    jugador = Jugador() if partida == None else partida['jugador']

    letra_seleccionada = False              
    orientacion = [True, False] # Si define la orientación, orientacion[0] = True. Si la orientación es vertical, orientacion[1] = False, si es horizontal orientacion[1] = True.
    primer_posicion = ultima_posicion = ()
    posiciones_ocupadas = OrderedDict() if partida == None else partida['posiciones ocupadas']
    primer_jugada = True if partida == None else partida['primer jugada']
    turno_jugador = random.randint(0, 100) % 2 == 0 if partida == None else partida['turno'] # si el número aleatorio es par, comienza el jugador
    posiciones_bloqueadas = [] if partida == None else partida['posiciones bloqueadas']
    fichas_usadas_pc = [] if partida == None else partida['fichas usadas pc']
    comenzar = False
    letra = '' 

    columna2 = [[sg.Text('Tiempo restante'), sg.Text(datetime.timedelta(seconds = contador), key = 'tiempo')],
                [sg.Text('Nivel: ' + nivel)],
                [sg.Text('Palabras válidas: ' + ('adjetivos, sustantivos y verbos' if nivel == 'facil' else ('adjetivos y verbos' if nivel == 'medio' else palabras_validas)))],
                [sg.Text('Puntajes')],
                [sg.Text('Jugador:'), sg.Text(str(jugador.get_puntaje()) + '     ', key = 'puntaje_jugador')],
                [sg.Text('Computadora:'), sg.Text(str(computadora.get_puntaje()) + '      ', key = 'puntaje_computadora')],
                [sg.Text('Turno actual:'), sg.Text('jugador' if turno_jugador else 'computadora', key = 'turno')],
                [sg.Text('Palabra actual:'), sg.Text('                 ', key = 'palabra_actual')],
                [sg.Text('Cambios restantes jugador:'), sg.Text(jugador.get_cambios_restantes(), key = 'cambios_jugador'), sg.Text('Cambios restantes pc:'), sg.Text(computadora.get_cambios_restantes(), key = 'cambios_pc')],
                [sg.Text('Cantidad de fichas en la bolsa:'), sg.Text(fichas_totales(bolsa_de_fichas), key = 'cantidad_fichas')],
                [sg.Button('Confirmar palabra', key = 'confirmar'), sg.Button('Cambiar fichas', key = 'cambiar'), sg.Button('Pasar', key = 'pasar')]]

    layout = [[sg.Column(columna1), sg.Column(columna2)]]  

    window = sg.Window('Tablero', layout).Finalize()

    if (partida != None):
        restaurar_tablero(window, partida['posiciones'])

    posiciones = {} if partida == None else partida['posiciones']
    partida = None

    while True:
      event = window.Read(timeout = 1000)[0] # milisegundos
      if (event == None):
        break
      elif (event == 'Pausa'):
          comenzar = not comenzar
          window.Element('Pausa').Update(button_color = ('white', 'red') if not comenzar else ('white', 'blue'))
      elif (event == 'Posponer'):
          partida = {'jugador' : jugador,
                     'letras jugador' : letras_jugador,
                     'computadora' : computadora, 
                     'letras computadora' : letras_pc,
                     'posiciones ocupadas' : posiciones_ocupadas, 
                     'primer jugada' : primer_jugada,
                     'turno' : turno_jugador, 
                     'posiciones bloqueadas' : posiciones_bloqueadas, 
                     'fichas usadas pc' : fichas_usadas_pc,
                     'nivel' : nivel,
                     'palabras validas' : palabras_validas,
                     'contador' : contador,
                     'bolsa de fichas' : bolsa_de_fichas,
                     'posiciones' : posiciones}
          sg.Popup('Se guardaron los datos de la partida', title = 'Atención')
          break
      elif (event == 'Terminar'):
        imprimir_mensaje_fin(jugador, computadora)
        break
      window.Element('turno').Update('jugador' if turno_jugador else 'computadora')
      if (not turno_jugador and comenzar):
        jugada = jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas, computadora, window, FILAS, COLUMNAS, posiciones, nivel, palabras_validas)
        if (jugada >= 0):
          computadora.actualizar_puntaje(jugada)
          window.Element('puntaje_computadora').Update(computadora.get_puntaje())
          primer_jugada = False
        else:
          computadora.actualizar_cambios_restantes()
        turno_jugador = True
        window.Element('turno').Update('jugador' if turno_jugador else 'computadora')
      if (event == 'Comenzar'):
        comenzar = True
        window.Element('Comenzar').Update(disabled = True, button_color = ('white', 'red'))
      if (event != '__TIMEOUT__' and comenzar):
        if (event == 'cambiar'):
          if (len(posiciones_ocupadas) > 0):
            sg.Popup('Primero debe levantar sus fichas', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
          else:
            print('Originales:', letras_jugador)
            cambio, contador = cambiar_fichas(jugador, letras_jugador, bolsa_de_fichas, contador, window)
            if (cambio):
              jugador.actualizar_cambios_restantes()
              window.Element('cambios_jugador').Update(jugador.get_cambios_restantes())
              letra_seleccionada = False              
              orientacion = [True, False]  
              primer_posicion = ultima_posicion = ()      
              posiciones_ocupadas = OrderedDict()
              turno_jugador = False
              if (jugador.get_cambios_restantes() == 0):
                window.Element('cambiar').Update(disabled = True, button_color = ('white', 'red'))
            print('Cambiadas:', letras_jugador)
        elif (event == 'pasar'):
          if (len(posiciones_ocupadas) > 0):
            sg.Popup('Primero debe levantar sus fichas', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
          else:
            if (letra_seleccionada):
              window.Element(letra).Update(button_color = ('white', 'green'))
              letra_seleccionada = False
            turno_jugador = False
        elif (event == 'confirmar'):
          if (letra_seleccionada):
            window.Element(letra).Update(button_color = ('white', 'green'))
            letra_seleccionada = False
          if (verificar_palabra(letras_jugador, posiciones_ocupadas, posiciones_bloqueadas, centro, primer_jugada, nivel, palabras_validas)):
            puntos_jugada = contar_puntos_jugador(posiciones_ocupadas, casillas_especiales, bolsa_de_fichas, letras_jugador)
            sg.Popup(f'Palabra formada por el jugador: {palabra_formada(letras_jugador, posiciones_ocupadas)}\nPuntos sumadados: {puntos_jugada}', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
            jugador.actualizar_puntaje(puntos_jugada)
            letra_seleccionada = False              
            orientacion = [True, False]  
            primer_posicion = ultima_posicion = ()
            posiciones_bloqueadas += [posicion for posicion in posiciones_ocupadas]
            for posicion in posiciones_ocupadas:
              letra = random.choice(abecedario)
              while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
                letra = random.choice(abecedario)
              letras_jugador[posiciones_ocupadas[posicion]] = letra
              window.Element(posiciones_ocupadas[posicion]).Update(letra, disabled = False, button_color = ('white', 'green'))
              bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
            posiciones_ocupadas = OrderedDict()
            turno_jugador = False
            primer_jugada = False
            window.Element('puntaje_jugador').Update(jugador.get_puntaje())
          else:
            print('palabra incorrecta')
        elif (event in range(7)):
          if (letra_seleccionada):
            window.Element(letra).Update(button_color = ('white', 'green'))
          window.Element(event).Update(button_color = ('white', 'red'))
          letra = event
          letra_seleccionada = True
        else:
          if (letra_seleccionada):
            if (posicion_valida(event, posiciones_ocupadas, orientacion, posiciones_bloqueadas)):
              if (event in posiciones_ocupadas):
                window.Element(posiciones_ocupadas[event]).Update(button_color = ('white', 'green'), disabled = False)
              else:
                ultima_posicion = event
              window.Element(event).Update(letras_jugador[letra], button_color = ('white', 'red'))
              posiciones[event] = letras_jugador[letra]
              posiciones_ocupadas[event] = letra
              window.Element(letra).Update(disabled = True)
              letra_seleccionada = False
              if (len(posiciones_ocupadas) == 1):
                primer_posicion = ultima_posicion = event
          else:
            if (event in (primer_posicion, ultima_posicion)):
              window.Element(event).Update(casillas_especiales[event]['texto'] if event in casillas_especiales else ' ', button_color = casillas_especiales[event]['color'] if event in casillas_especiales else ('white', 'green'), disabled = False)   
              window.Element(posiciones_ocupadas[event]).Update(button_color = ('white', 'green'), disabled = False)
              del posiciones_ocupadas[event]
              del posiciones[event]
              if (len(posiciones_ocupadas) <= 1):
                orientacion = [True, False] 
                if (len(posiciones_ocupadas) == 0):
                  primer_posicion = ()
                  ultima_posicion = ()
              if (event == primer_posicion):
                primer_posicion = (event[0] + 1, event[1]) if not orientacion[1] else (event[0], event[1] + 1)
              else:
                ultima_posicion = (event[0] - 1, event[1]) if not orientacion[1] else (event[0], event[1] - 1)
      if (comenzar):
        window.Element('tiempo').Update(datetime.timedelta(seconds = contador))
        contador -= 1
        window.Element('palabra_actual').Update(palabra_formada(letras_jugador, posiciones_ocupadas))
        window.Element('cantidad_fichas').Update(fichas_totales(bolsa_de_fichas))
        if (contador == 0 or computadora.get_cambios_restantes() == -1):
          imprimir_mensaje_fin(jugador, computadora)
          break

    window.Close()
    return partida, jugador, computadora
