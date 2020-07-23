from functools import reduce
import random, PySimpleGUI as sg
from pattern.es import parse, verbs, spelling, lexicon
import time, datetime
from itertools import permutations

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

  return reduce(lambda anterior, posicion: anterior + letras[posicion], posiciones_ocupadas.values(), '')


def es_palabra(nivel, palabra_validas, palabra):
  '''
  Función que retorna true en caso de que la palabra sea válida para el nivel correspondiente
  '''

  palabra = palabra.lower()
  if (nivel == 'fácil'):
    return (palabra in verbs or (palabra in spelling and palabra in lexicon))
  elif (nivel == 'medio'):
    return (parse(palabra).split('/')[1] != 'NN' and (palabra in verbs or (palabra in spelling and palabra in lexicon))) 
  elif (nivel == 'difícil'):
    tipo = 'JJ' if palabras_validas == 'adjetivos' else 'VB'
    return (parse(palabra).split('/')[1] == tipo and (palabra in verbs or (palabra in spelling and palabra in lexicon))) 
      

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
    # str = ''
    # for clave in posiciones_ocupadas:
    #   str += letras[posiciones_ocupadas[clave]]
    if (es_palabra(nivel, palabras_validas, palabra_formada(letras, posiciones_ocupadas))):
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
  
  posiciones[posicion] = letra
  posiciones_bloqueadas += [posicion]
  temp = bolsa_de_fichas[letra]['puntaje']
  if (posicion in casillas_especiales):
    if (casillas_especiales[posicion]['modificador'] < 10):
      puntos_jugada[0] += temp + casillas_especiales[posicion]['modificador']
    elif (casillas_especiales[posicion]['modificador'] < 20):
      puntos_jugada[0] += temp * (casillas_especiales[posicion]['modificador'] % 10)
    else:
      puntos_jugada[0] += temp
      multiplicador[0] += (casillas_especiales[posicion]['modificador'] % 10)   
  else:
    puntos_jugada[0] += temp


def jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas, computadora, window, FILAS, COLUMNAS, posiciones, nivel, palabras_validas, contador):
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
  
  orientacion = random.choice(('v', 'h'))
  print(orientacion)
  fichas = "".join([letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas])
  print('letras pc:', letras_pc)
  puntos_jugada = [0]
  multiplicador = [0]
  ubicacion_mas_larga = []
  print('primer jugada', primer_jugada)
  if (primer_jugada):
    i = centro[0]
    j = centro[1]
    ubicacion_mas_larga = [(i, j + x) if orientacion == 'h' else (i + x, j) for x in range(7)]
  else:
    encontre = False
    cant = 0
    while (not encontre):
      i = random.randint(0, FILAS - 1)
      j = random.randint(0, COLUMNAS - 3)
      cant += 1
      temp = []
      for x in range(7):
        posicion = (i, j + x) if orientacion == 'h' else (i + x, j)
        if (not posicion in posiciones_bloqueadas and (posicion[0] < FILAS and posicion[1] < COLUMNAS)):
          temp += [posicion]
        else:
          break
      if (len(temp) >= 2 and len(temp) > len(ubicacion_mas_larga)):
        ubicacion_mas_larga = temp
      if cant > 100 or len(ubicacion_mas_larga) == 7:
        encontre = True
  permutaciones = set("".join(permutacion) for permutacion in permutations(letras_pc))
  encontrada = ""
  print('ubi', ubicacion_mas_larga)
  for permutacion in permutaciones:
    for x in range(len(ubicacion_mas_larga) - 1, 1, -1):
      palabra = permutacion[: x + 1]
      if es_palabra(nivel, palabras_validas, palabra) and len(palabra) > len(encontrada):
        encontrada = palabra
        print(encontrada)
  palabra = encontrada
  encontre = len(palabra) >= 2
  if (encontre):
    posiciones_usadas = []
    print(palabra, es_palabra(nivel, palabras_validas, palabra))
    for letra, posicion in zip(palabra, ubicacion_mas_larga):
      sumar_casilla(window, bolsa_de_fichas, casillas_especiales, posicion, letra, puntos_jugada, multiplicador, posiciones_bloqueadas, posiciones) 
      posiciones_usadas += [posicion]
    fichas_usadas_pc.clear()
    quedan = quedan_fichas(bolsa_de_fichas, len(palabra))
    for letra, posicion in zip(palabra, posiciones_usadas):
      x = random.randint(8, 14)
      while (x in fichas_usadas_pc):
        x = random.randint(8, 14)
      window.Element(x).Update(button_color = ('white', 'red'))
      window.Element(posicion).Update(letra, button_color = ('white', 'red'))
      window.Read(timeout = 1000)
      contador -= 1
      window.Element('tiempo').Update(datetime.timedelta(seconds = contador))
      fichas_usadas_pc += [x]
      letras_pc.remove(letra)
      if (quedan):
        letra_nueva = random.choice(fichas)
        while (bolsa_de_fichas[letra_nueva]['cantidad_fichas'] <= 0):
          letra_nueva = random.choice(fichas)
        letras_pc += [letra_nueva]
        bolsa_de_fichas[letra_nueva]['cantidad_fichas'] -= 1
    if (quedan):
      for i in range(8, 15):
        window.Element(i).Update(button_color = ('white', 'green'), disabled = True)
    else:
      print('1')
      for i in range(4):
        computadora.actualizar_cambios_restantes()
    puntos_jugada = 0 if puntos_jugada[0] < 0 else (puntos_jugada[0] if multiplicador[0] == 0 else puntos_jugada[0] * multiplicador[0])
    sg.Popup(f'Palabra formada por la computadora: {palabra}\nPuntos sumadados: {puntos_jugada}', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
    return puntos_jugada, contador, False
  else:
    if (quedan_fichas(bolsa_de_fichas)):
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
        window.Element('cambios_pc').Update(computadora.get_cambios_restantes())
        return 0, contador, primer_jugada   
      else:
        return -1, contador, primer_jugada
    else:
      print('2')
      return -1, contador, primer_jugada

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
        tablero_juego[i][j] = sg.Button('F x2', size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'blue'))      
        casillas_especiales[(i, j)] = {'color' : ('white', 'blue'), 'texto' : 'F x2', 'modificador' : 12}                              
      elif(i + j == FILAS - 1):
        tablero_juego[i][j] = sg.Button('F x3', size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'blue'))
        casillas_especiales[(i, j)] = {'color': ('white', 'blue'), 'texto' : 'F x3', 'modificador' : 13}
      elif (nivel == 'fácil'):
        if ((posicion in malas_nivel_facil) or (posicion_invertida in malas_nivel_facil)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif ((posicion in multiplicador_nivel_facil) or (posicion_invertida in multiplicador_nivel_facil)):
          tablero_juego[i][j] = sg.Button('P x3' if posicion in multiplicador_nivel_facil else 'P x2', size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)]={'color': ('white', 'purple'), 'texto' : 'P x3' if posicion in multiplicador_nivel_facil else 'P x2', 'modificador' : 23 if posicion in multiplicador_nivel_facil else 22}
      elif (nivel == 'medio'):
        if ((posicion in malas_nivel_medio) or (posicion_invertida in malas_nivel_medio)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (posicion in multiplicador_nivel_medio or posicion_invertida in multiplicador_nivel_medio):
          tablero_juego[i][j] = sg.Button('P x3' if posicion_invertida in multiplicador_nivel_medio else 'P x2', size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3' if posicion in multiplicador_nivel_facil else 'P x2', 'modificador' : 23 if posicion_invertida in multiplicador_nivel_medio else 22}
      elif (nivel == 'difícil'):
        if ((posicion in malas_nivel_dificil) or (posicion_invertida in malas_nivel_dificil)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (posicion in multiplicador_nivel_dificil or posicion_invertida in multiplicador_nivel_dificil):
          tablero_juego[i][j] = sg.Button('P x3' if posicion in multiplicador_nivel_dificil else 'P x2', size = (3, 1), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3' if posicion in multiplicador_nivel_facil else 'P x2', 'modificador' : 23 if posicion in multiplicador_nivel_dificil else 22}
          
  tablero_juego[centro[0]][centro[1]] = sg.Button('Inicio', size = (3, 1), key = (centro[0], centro[1]), pad = (0.5, 0.5), button_color = ('black', 'yellow'))
  casillas_especiales[(centro[0], centro[1])] = {'color' : ('black', 'yellow'), 'texto' : 'Inicio', 'modificador' : 1}   


def repartir_fichas(bolsa_de_fichas, letras):
  '''
  Función que reparte 7 fichas de la bolsa en forma aleatoria.
  Los jugadores reciben más vocales que consonantes para que 
  tengan mayor posibilidad de formar palabras.
  '''
  
  fichas = "".join([letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas])
  for i in range(7):
    letra = random.choice(fichas)
    while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):         
      letra = random.choice(fichas)
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
    temp = bolsa_de_fichas[letras_jugador[posiciones_ocupadas[posicion]]]['puntaje']
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


def finalizar_partida(jugador, letras_jugador, computadora, letras_pc, bolsa_de_fichas, window):
  '''
  Función que muestra el mensaje de fin de la partida, detallando los puntos
  de la computadora y del jugador.
  '''
  
  
  for letra_jugador, letra_pc in zip(letras_jugador, letras_pc):
      jugador.actualizar_puntaje(- bolsa_de_fichas[letra_jugador]['puntaje'])
      computadora.actualizar_puntaje(- bolsa_de_fichas[letra_pc]['puntaje'])
  if jugador.get_puntaje() < 0:
    jugador.set_puntaje(0)
  if computadora.get_puntaje() < 0:
    computadora.set_puntaje(0)
    
  window['puntaje_jugador'].Update(jugador.get_puntaje())
  window['puntaje_computadora'].Update(computadora.get_puntaje())

  for i, letra in zip(range(8, 15), letras_pc):
      window.Element(i).Update(letra, disabled = False)

  hay_cambios = computadora.get_cambios_restantes() >= 0 and jugador.get_cambios_restantes() >= 0
  if (not hay_cambios):
    aux = 'El jugador' if jugador.get_cambios_restantes() < 0 else 'La computadora'
  mensaje = '¡Fin de la partida!\n' + (f'{aux} no puede formar ninguna palabra y no dispone de más cambios \n' if not hay_cambios else '\n')
  if (jugador.get_puntaje() > computadora.get_puntaje()):
    mensaje += f'Ganó el jugador con {jugador.get_puntaje()} puntos'
  elif (jugador.get_puntaje() < computadora.get_puntaje()):
    mensaje += f'Ganó la computadora con {computadora.get_puntaje()} puntos'
  else: 
    mensaje += 'Hubo un empate'
  sg.Popup(mensaje, title = 'Atención')

  for key in ('Iniciar', 'Posponer', 'Pausa', 'Terminar', 'confirmar', 'cambiar', 'pasar'):
    window.Element(key).Update(disabled = True)
  window.Element('Salir').Update(visible = True)


def cambiar_fichas(jugador, letras_jugador, bolsa_de_fichas, contador, window):
  '''
  Esta función muestra una ventana para que el jugador pueda cambiar algunas o todas sus fichas.
  En caso de haber hecho algún cambio, actualiza las fichas del atril.
  '''

  layout_cambiar_fichas = [[sg.Button('Cambiar todas', key = 'todas'), sg.Button('Cambiar algunas', key = 'algunas')],
                           [sg.Text('')],
                           [sg.Text('Seleccione las fichas que quiere intercambiar')],
                           [sg.Button(letras_jugador[i], size= (3, 1), key = i, pad = (0.5, 0.5), disabled = True, button_color = ('white', 'green')) for i in range(7)],
                           [sg.Text('')],
                           [sg.Button('Aceptar', disabled = True), sg.Button('Salir')]]
  ventana = sg.Window('Cambiar fichas', layout_cambiar_fichas)

  fichas = "".join([letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas])

  seleccionadas = {}

  cambio = algunas = False

  while True:
    event = ventana.Read(timeout = 1000)[0]
    contador -= 1
    window.Element('tiempo').Update(datetime.timedelta(seconds = contador))
    if (contador == 0):
      break
    if (event == '__TIMEOUT__'):
      continue
    if (event in ('Salir', None)):
      break
    if (event == 'todas'):
      if (quedan_fichas(bolsa_de_fichas)):
        for letra in letras_jugador:
          bolsa_de_fichas[letra]['cantidad_fichas'] += 1
        letras_jugador.clear()
        repartir_fichas(bolsa_de_fichas, letras_jugador)
        for i in range (7):
          window.Element(i).Update(letras_jugador[i], button_color = ('white', 'green'))
        sg.Popup('Se cambiaron todas las fichas del jugador', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
        cambio = True
        break
      else:
        sg.Popup('No quedan suficientes fichas en la bolsa', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
    elif (event == 'algunas'):
      if (not algunas):
        ventana.Element('todas').Update(disabled = True)
        ventana.Element('Aceptar').Update(disabled = False) 
        for i in range(7):
          ventana.Element(i).Update(disabled = False)
        algunas = True
      else:
        ventana.Element('todas').Update(disabled = False)
        ventana.Element('Aceptar').Update(disabled = True) 
        for i in range(7):
          ventana.Element(i).Update(disabled = True)
        algunas = False
    elif (event == 'Aceptar'):
      if (len(seleccionadas) == 0):
        sg.Popup('Debe seleccionar alguna letra', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
      else:
        if (quedan_fichas(bolsa_de_fichas, len(seleccionadas))):
          for i in seleccionadas:
            bolsa_de_fichas[seleccionadas[i]]['cantidad_fichas'] += 1
            letra = random.choice(fichas)
            while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
              letra = random.choice(fichas)
            bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
            window.Element(i).Update(letra, button_color = ('white', 'green'))
            letras_jugador[i] = letra
          sg.Popup('Se cambiaron algunas fichas del jugador', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
          cambio = True
          break
        else:
          sg.Popup('No quedan suficientes fichas en la bolsa', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
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
