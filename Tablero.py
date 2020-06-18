import random, PySimpleGUI as sg
from random import randint
from pattern.es import parse, verbs, spelling, lexicon
from collections import OrderedDict
from itertools import permutations
import sys

def posicion_valida(event, posiciones_ocupadas, orientacion, posiciones_bloqueadas):
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
  sg.Popup('Solo se pueden agregar letras en forma horizontal' if orientacion[1] else 'Solo se pueden agregar letras en forma vertical')
  return False

def palabra_formada(letras, posiciones_ocupadas):
  str = ''
  for clave in posiciones_ocupadas:
    str += letras[posiciones_ocupadas[clave]]
  return str

def es_palabra(str):
  str = str.lower()
  return (str in verbs or (str in spelling and str in lexicon))

def verificar_palabra(letras, posiciones_ocupadas, posiciones_bloqueadas, centro, primer_jugada):
  if (primer_jugada and not centro in posiciones_ocupadas):
    sg.Popup('La casilla de inicio de juego no está ocupada')
    return False
  if (len(posiciones_ocupadas) < 2):
    sg.Popup('Palabra inválida')
    return False
  else:
    str = ''
    for clave in posiciones_ocupadas:
      str += letras[posiciones_ocupadas[clave]]
    if (es_palabra(str)):
      #analisis = parse(str).split('/')
      #print(analisis)
      #for tipo_palabra in palabras_validas:
      #  if (analisis[1] in palabras_validas[tipo_palabra]):
      #    sg.Popup(f'Palabra formada: {str}')
      #    for posicion in posiciones_ocupadas:
      #      posiciones_bloqueadas += [posicion]
      #    return True
      sg.Popup(f'Palabra formada por el jugador: {str}')
      return True
    else:
      sg.Popup('Palabra inválida')
      return False

def sumar_casilla(casillas_especiales, posicion, letra, puntos_jugada, multiplicador, posiciones_bloqueadas):
  window.Element(posicion).Update(letra, button_color = ('white', 'red'))
  puntos_jugada[0] += bolsa_de_fichas[letra]['puntaje_ficha']
  posiciones_bloqueadas += [posicion]
  if (posicion in casillas_especiales):
    if (casillas_especiales[posicion]['modificador'] < 10):
      puntos_jugada[0] += casillas_especiales[posicion]['modificador']
    else:
      multiplicador[0] += (casillas_especiales[posicion]['modificador'] % 10)

def jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas):
  orientacion = random.randint(0, 100) % 2 == 0   # Si es par la orientacion es horizontal
  abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  print(letras_pc)
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
      if (es_palabra(palabra)):
        encontre = True
        break
  encontre = encontre and len(palabra) > 1
  if (encontre):
    print(palabra, es_palabra(palabra))
    if (primer_jugada):
      for letra in palabra:
        sumar_casilla(casillas_especiales, (i, j), letra, puntos_jugada, multiplicador, posiciones_bloqueadas) 
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
        sumar_casilla(casillas_especiales, (i, j), letra, puntos_jugada, multiplicador, posiciones_bloqueadas) 
        j += 1 if orientacion else 0
        i += 1 if not orientacion else 0
    fichas_usadas_pc.clear()
    for letra in palabra:
      x = random.randint(8, 14)
      while (x in fichas_usadas_pc):
        x = random.randint(8, 14)
      window.Element(x).Update(button_color = ('white', 'red'), disabled = True)
      fichas_usadas_pc += [x]
      letras_pc.remove(letra)
      letra_nueva = random.choice(abecedario)
      while (bolsa_de_fichas[letra_nueva]['cantidad_fichas'] <= 0):
        letra_nueva = random.choice(abecedario)
      letras_pc += [letra_nueva]
      bolsa_de_fichas[letra_nueva]['cantidad_fichas'] -= 1
    print(puntos_jugada[0], '*', multiplicador[0])
    for i in range(8, 15):
      window.Element(i).Update(button_color = ('white', 'green'), disabled = False)
    sg.Popup(f'Palabra formada por la computadora: {palabra}')
    print('nuevas letras', letras_pc)
    if (puntos_jugada[0] < 0):
      return 0
    else:
      return puntos_jugada[0] if multiplicador[0] == 0 else puntos_jugada[0] * multiplicador[0]
  else:
    letras_pc.clear()
    for letra in fichas_usadas_pc:
      bolsa_de_fichas[letra]['cantidad_fichas'] += 1
    fichas_usadas_pc.clear()
    for i in range(8, 15):
      window.Element(i).Update(button_color = ('white', 'green'), disabled = False)
    repartir_fichas(bolsa_de_fichas, letras_pc)
    sg.Popup('Se repartieron nuevas fichas a la computadora')
    print('nuevas letras', letras_pc)
    return 0

def colocar_posiciones_especiales(nivel, casillas_especiales, FILAS, COLUMNAS, centro):
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
      elif (nivel == 1):
        if ((posicion in malas_nivel_facil) or (posicion_invertida in malas_nivel_facil)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif ((posicion in multiplicador_nivel_facil) or (posicion_invertida in multiplicador_nivel_facil)):
          tablero_juego[i][j] = sg.Button('P x3' if posicion in multiplicador_nivel_facil else 'P x2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)]={'color': ('white', 'purple'), 'texto' : 'P x3', 'modificador' : 13 if posicion in multiplicador_nivel_facil else 12}
      elif (nivel == 2):
        if ((posicion in malas_nivel_medio) or (posicion_invertida in malas_nivel_medio)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (posicion in multiplicador_nivel_medio or posicion_invertida in multiplicador_nivel_medio):
          tablero_juego[i][j] = sg.Button('P x3' if posicion_invertida in multiplicador_nivel_medio else 'P x2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3', 'modificador' : 13 if posicion_invertida in multiplicador_nivel_medio else 12}
      elif (nivel == 3):
        if ((posicion in malas_nivel_dificil) or (posicion_invertida in malas_nivel_dificil)):
          tablero_juego[i][j] = sg.Button('F ' + str(mala_actual), size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'texto' : 'F ' + str(mala_actual), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (posicion in multiplicador_nivel_dificil or posicion_invertida in multiplicador_nivel_dificil):
          tablero_juego[i][j] = sg.Button('P x3' if posicion in multiplicador_nivel_dificil else 'P x2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'purple'))
          casillas_especiales[(i, j)] = {'color': ('white', 'purple'), 'texto' : 'P x3', 'modificador' : 13 if posicion in multiplicador_nivel_dificil else 12}
          
  tablero_juego[centro[0]][centro[1]] = sg.Button('Inicio', size = (4, 2), key = (centro[0], centro[1]), pad = (0.5, 0.5), button_color = ('white', 'yellow'))
  casillas_especiales[(centro[0], centro[1])] = {'color' : ('white', 'yellow'), 'texto' : 'Inicio', 'modificador' : 1}        

def agregar_posiciones_bloqueadas(posiciones_ocupadas, posiciones_bloqueadas):
  for posicion in posiciones_ocupadas:
    posiciones_bloqueadas += [posicion]

def repartir_fichas(bolsa_de_fichas, letras):
  abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  for i in range(7):
    letra = random.choice(abecedario)
    while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
      letra = random.choice(abecedario)
    letras += [letra]
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1

def contar_puntos_jugador(posiciones_ocupadas, casillas_especiales, bolsa_de_fichas, letras_jugador):
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
  total = 0
  for letra in bolsa_de_fichas:
    total += bolsa_de_fichas[letra]['cantidad_fichas']  
  return total  

def imprimir_mensaje_fin(puntos_jugador, puntos_pc):
  mensaje = '¡Fin de la partida!\n'
  if (puntos_jugador > puntos_pc):
    mensaje += f'Ganó el jugador con {puntos_jugador}'
  if (puntos_jugador < puntos_pc):
    mensaje += f'Ganó la computadora con {puntos_pc}'
  if (puntos_jugador == puntos_pc):
    mensaje += 'Hubo un empate'
  sg.Popup(mensaje)

nivel = 3
FILAS = COLUMNAS = 15

centro = (int(FILAS / 2), int(FILAS / 2))

abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

bolsa_de_fichas = {}

for letra in abecedario:
  bolsa_de_fichas[letra] = {'cantidad_fichas' : 10, 'puntaje_ficha' : 1}

letras_jugador = []
letras_pc = []

print('Fichas totales:', fichas_totales(bolsa_de_fichas))
repartir_fichas(bolsa_de_fichas, letras_jugador)
repartir_fichas(bolsa_de_fichas, letras_pc)
print('Fichas totales:', fichas_totales(bolsa_de_fichas))

tablero_juego = [[sg.Button('', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'green')) for j in range(COLUMNAS)] for i in range(FILAS)]

casillas_especiales = {}
colocar_posiciones_especiales(nivel, casillas_especiales, FILAS, COLUMNAS, centro)

fichas_jugador = [sg.Button(letras_jugador[i], size = (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

fichas_pc = [sg.Button('?', size= (4, 2), key = i + 8, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

layout = [[sg.Text('Fichas de la computadora')]] + [fichas_pc] + [[sg.Text(' ')]] + [x for x in tablero_juego] 
layout += [[sg.Text('Fichas del jugador')]] + [fichas_jugador]
layout += [[sg.Button('Comenzar', button_color = ('white', 'green')), sg.Button('Posponer'), sg.Button('Pausa'), sg.Button('Terminar')]]

columna1 = layout

columna2 = [[sg.Text('Tiempo restante'), sg.Text('             ', key = 'tiempo')],
            [sg.Text('Puntajes')],
            [sg.Text('Jugador'), sg.Text('0       ', key = 'puntaje_jugador')],
            [sg.Text('Computadora'), sg.Text('0     ', key = 'puntaje_computadora')],
            [sg.Text('Turno actual'), sg.Text('                  ', key = 'turno')],
            [sg.Text('Palabra actual'), sg.Text('                 ', key = 'palabra_actual')],
            [sg.Button('Confirmar palabra', key = 'confirmar'), sg.Button('Cambiar fichas', key = 'cambiar'), sg.Button('Pasar', key = 'pasar')],
            [sg.Text('Cambios restantes'), sg.Text(' ', key = 'cambios')]]

layout = [[sg.Column(columna1), sg.Column(columna2)]]  

window = sg.Window('Tablero', layout)

abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') 

# layout_cambiar_fichas = [[sg.Button('Cambiar todas', key = 'todas'), sg.Button('Cambiar algunas', key = 'algunas')],
#                          [sg.Text('Seleccione las fichas que quiere intercambiar', key = 'texto1', visible = False)],
#                          [sg.Text('Fichas en la bolsa', key = 'texto2', visible = False)],
#                          [sg.Button(abecedario[i] + ' x' + str(bolsa_de_fichas[abecedario[i]]), size= (4, 2), key = abecedario[i], pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(14)],
#                          [sg.Button(abecedario[i] + ' x' + str(bolsa_de_fichas[abecedario[i]]), size= (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(14,26)]]

# ventana_cambiar_fichas = sg.Window('Cambiar fichas', layout_cambiar_fichas)

# ventana_cambiar_fichas.Read()
# ventana_cambiar_fichas.Close()

letra_seleccionada = False              
orientacion = [True, False]   # Si define la orientación, orientacion[0] = True. Si la orientación es vertical, orientacion[1] = False, si es horizontal orientacion[1] = True.
letras = []
abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
primer_posicion = ultima_posicion = ()
posiciones_ocupadas = OrderedDict()
primer_jugada = True
turno_jugador = random.randint(0, 100) % 2 == 0 #   si el número aleatorio es par, comienza el jugador
posiciones_bloqueadas = []
fichas_usadas_pc = []
puntaje_pc = 0
puntaje_jugador = 0
contador_segundos = 12
comenzar = False
    
while True:
  event, values = window.Read(timeout = 1000) # milisegundos
  window.Element('turno').Update('jugador' if turno_jugador else 'computadora')
  if (not turno_jugador and comenzar):
    jugada = jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas)
    if (jugada > 0):
      puntaje_pc += jugada
      window.Element('puntaje_computadora').Update(puntaje_pc)
      primer_jugada = False
    turno_jugador = True
    window.Element('turno').Update('jugador' if turno_jugador else 'computadora')
    print('Fichas totales:', fichas_totales(bolsa_de_fichas))
  if (event == 'Comenzar'):
    comenzar = True
    window.Element('Comenzar').Update(disabled = True, button_color = ('white', 'red'))
  if (event != '__TIMEOUT__' and comenzar):
    if (event in (None, 'Terminar')):
        break
    if (event == 'cambiar'):
      if (len(posiciones_ocupadas) > 0):
        sg.Popup('Primero debe levantar sus fichas')
      else:
        for letra in letras_jugador:
          bolsa_de_fichas[letra]['cantidad_fichas'] += 1
        letra_seleccionada = False              
        orientacion = [True, False]  
        primer_posicion = ultima_posicion = ()      
        posiciones_ocupadas = OrderedDict()
        turno_jugador = False
        letras_jugador = []
        repartir_fichas(bolsa_de_fichas, letras_jugador)
        for i in range (7):
          window.Element(i).Update(letras_jugador[i], disabled = False, button_color = ('white', 'green'))
        sg.Popup('Se repartieron nuevas fichas al jugador')
    if (event == 'pasar'):
      if (len(posiciones_ocupadas) > 0):
        sg.Popup('Primero debe levantar sus fichas')
      else:
        if (letra_seleccionada):
          window.Element(letra).Update(button_color = ('white', 'green'))
          letra_seleccionada = False
        turno_jugador = False
    if (event == 'confirmar'):
      if (letra_seleccionada):
        window.Element(letra).Update(button_color = ('white', 'green'))
        letra_seleccionada = False
      if (verificar_palabra(letras_jugador, posiciones_ocupadas, posiciones_bloqueadas, centro, primer_jugada)):
        puntaje_jugador += contar_puntos_jugador(posiciones_ocupadas, casillas_especiales, bolsa_de_fichas, letras_jugador)
        letra_seleccionada = False              
        orientacion = [True, False]  
        primer_posicion = ultima_posicion = ()
        agregar_posiciones_bloqueadas(posiciones_ocupadas, posiciones_bloqueadas)
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
        window.Element('puntaje_jugador').Update(puntaje_jugador)
      else:
        print('palabra incorrecta')
    if (event in range(7)):
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
          if (len(posiciones_ocupadas) <= 1):
            orientacion[0] = True
            orientacion[1] = False
            if (len(posiciones_ocupadas) == 0):
              primer_posicion = ()
              ultima_posicion = ()
          if (event == primer_posicion):
            primer_posicion = (event[0] + 1, event[1]) if not orientacion[1] else (event[0], event[1] + 1)
          else:
            ultima_posicion = (event[0] - 1, event[1]) if not orientacion[1] else (event[0], event[1] - 1)
      print('Fichas totales:', fichas_totales(bolsa_de_fichas))
  if (comenzar):
    window.Element('tiempo').Update(contador_segundos)
    contador_segundos -= 1
    if (contador_segundos == 0):
      imprimir_mensaje_fin(puntaje_jugador, puntaje_pc)
      break
  window.Element('palabra_actual').Update(palabra_formada(letras_jugador, posiciones_ocupadas))

window.Close()

