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
      analisis = parse(str).split('/')
      print(analisis)
      for tipo_palabra in palabras_validas:
        if (analisis[1] in palabras_validas[tipo_palabra]):
          sg.Popup(f'Palabra formada: {str}')
          for posicion in posiciones_ocupadas:
            posiciones_bloqueadas += [posicion]
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
      palabra = temp[0:x + 1]
      if (es_palabra(palabra)):
        encontre = True
        break
  encontre = encontre and len(palabra) > 1
  if (encontre):
    print(palabra, es_palabra(palabra))
    if (primer_jugada):
      for letra in palabra:
        sumar_casilla(casillas_especiales, (i,j), letra, puntos_jugada, multiplicador, posiciones_bloqueadas) 
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
        sumar_casilla(casillas_especiales, (i,j), letra, puntos_jugada, multiplicador, posiciones_bloqueadas) 
        j += 1 if orientacion else 0
        i += 1 if not orientacion else 0
    for letra in palabra:
      x = random.randint(8, 14)
      while (x in fichas_usadas_pc):
        x = random.randint(8, 14)
      window.Element(x).Update(button_color = ('white', 'red'), disabled = True)
      fichas_usadas_pc += [x]
      letras_pc.remove(letra)
    print(puntos_jugada[0], '*', multiplicador[0])
    if (puntos_jugada[0] < 0):
      return 0
    else:
      return puntos_jugada[0] if multiplicador[0] == 0 else puntos_jugada[0] * multiplicador[0]
  else:
    abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    letras_pc.clear()
    fichas_usadas_pc.clear()
    for i in range(8, 15):
      window.Element(i).Update(button_color = ('white', 'green'), disabled = False)
    for i in range(7):
      letra = random.choice(abecedario)
      while (bolsa_de_fichas[letra] == 0):
        letra = random.choice(abecedario)
      letras_pc += [letra]
      bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
    print('nuevas letras', letras_pc)
    return 0

def colocar_fichas_especiales(nivel, casillas_especiales, FILAS, COLUMNAS):
  malas_NivelFacil =[(1,7),(1,11),(2,8),(2,10),(3,9),
                   (17,7),(11,17),(8,16),(10,16),(9,15)]

  malas_NivelMedio=[(3,7),(3,9),(4,8),(5,7),(5,9),
                    (7,13),(7,11),(9,13),(9,11),(8,12)]

  pal_NivelMedio=[(0,8),(1,7),(1,9),(2,6),(2,10),(3,5),(3,11),
                  (8,16),(7,15),(9,15),(6,14),(10,14),(5,13),(11,13)

  ]

  malas_NivelDificil=[(0,5),(0,9),(1,6),(1,8),(2,7),(3,6),(3,8),(4,7),
                      (14,5),(14,9),(13,6),(13,8),(12,7),(11,6),(11,8),(10,7)]

  mala_actual = -1

  for i in range(FILAS):
    for j in range(COLUMNAS):
      tupla=(i,j)
      tuplain=(j,i)
      if(tupla!=centro):
        if(j==i):
          tablero_juego[i][j] = sg.Button('F +2', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'blue'))
          casillas_especiales[(i,j)] = {'color' : ('white', 'blue'), 'modificador' : 2}
        else:
          if(i + j==FILAS - 1):
            tablero_juego[i][j]=sg.Button('F +3', size=(4, 2), key=(i, j), pad=(0.5, 0.5),button_color=('white', 'blue'))
            casillas_especiales[(i, j)]={'color': ('white', 'blue'), 'modificador' : 3}
        if ((nivel == 1) and ((tupla in malas_NivelFacil)or(tuplain in malas_NivelFacil))):
          tablero_juego[i][j]=sg.Button('F ' + str(mala_actual), size=(4, 2), key=(i, j), pad=(0.5, 0.5), button_color=('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1
        elif (nivel == 2):
          if((tupla in malas_NivelMedio) or (tuplain in malas_NivelMedio)):
            tablero_juego[i][j]=sg.Button('F ' + str(mala_actual), size=(4, 2), key=(i, j), pad=(0.5, 0.5), button_color=('white', 'black'))
            casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'modificador' : mala_actual}
            mala_actual = mala_actual - 1 if mala_actual > -3 else -1
          if(tupla in pal_NivelMedio):
            tablero_juego[i][j]=sg.Button('P x3', size=(4, 2), key=(i, j), pad=(0.5, 0.5),button_color=('white', 'purple'))
            casillas_especiales[(i, j)]={'color': ('white', 'black'), 'modificador' : 13}
          if(tuplain in pal_NivelMedio):
            tablero_juego[i][j]=sg.Button('P x2', size=(4, 2), key=(i, j), pad=(0.5, 0.5),button_color=('white', 'purple'))
            casillas_especiales[(i, j)]={'color': ('white', 'black'), 'modificador' : 12}
        elif (nivel== 3) and ((tupla in malas_NivelDificil) or (tuplain in malas_NivelDificil)):
          tablero_juego[i][j]=sg.Button('F ' + str(mala_actual), size=(4, 2), key=(i, j), pad=(0.5, 0.5), button_color=('white', 'black'))
          casillas_especiales[(i, j)] = {'color' : ('white', 'black'), 'modificador' : mala_actual}
          mala_actual = mala_actual - 1 if mala_actual > -3 else -1

def agregar_posiciones_bloqueadas(posiciones_ocupadas, posiciones_bloqueadas):
  for posicion in posiciones_ocupadas:
    posiciones_bloqueadas += [posicion]

def repartir_fichas(bolsa_de_fichas, letras_jugador, letras_pc):
  abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  for i in range(7):
    letra = random.choice(abecedario)
    letras_jugador += [letra]
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
    letra = random.choice(abecedario)
    letras_pc += [letra]
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1

FILAS = COLUMNAS = 17
nivel = 2

centro = (int(FILAS / 2), int(FILAS / 2))

abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

bolsa_de_fichas = {}

for letra in abecedario:
  bolsa_de_fichas[letra] = {'cantidad_fichas' : 10, 'puntaje_ficha' : 1}

letras_jugador = []
letras_pc = []

repartir_fichas(bolsa_de_fichas, letras_jugador, letras_pc)

tablero_juego = [[sg.Button('', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'green')) for j in range(COLUMNAS)] for i in range(FILAS)]

tablero_juego[centro[0]][centro[1]] = sg.Button('Inicio', size = (4, 2), key = (centro[0], centro[1]), pad = (0.5, 0.5), button_color = ('white', 'yellow'))

casillas_especiales = {centro : {'color' : ('white', 'yellow'), 'modificador' : 1}}

colocar_fichas_especiales(nivel, casillas_especiales, FILAS, COLUMNAS)

fichas_jugador = [sg.Button(letras_jugador[i], size= (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

fichas_pc = [sg.Button('?', size= (4, 2), key = i + 8, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

layout = [[sg.Text('Fichas de la computadora')]] + [fichas_pc] + [[sg.Text(' ')]] + [x for x in tablero_juego] 
layout += [[sg.Text('Fichas del jugador')]] + [fichas_jugador]
layout += [[sg.Button('Posponer'), sg.Button('Pausa'), sg.Button('Terminar')]]

columna1 = layout

columna2 = [[sg.Text('Tiempo restante'), sg.Text(' ', key = 'tiempo')],
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
primer_posicion = ultima_posicion = ()
posiciones_ocupadas = OrderedDict()
primer_jugada = True
turno_jugador = random.randint(0, 100) % 2 == 0 #   si el número aleatorio es par, comienza el jugador
posiciones_bloqueadas = []
fichas_usadas_pc = []
puntaje_pc = 0
puntaje_jugador = 0

while True:
  event, values = window.Read()
  if (not turno_jugador):
    jugada = jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas)
    if (jugada > 0):
      puntaje_pc += jugada
      window.Element('puntaje_computadora').Update(puntaje_pc)
      primer_jugada = False
    turno_jugador = True
    print(puntaje_pc)
  if (event in (None, 'Terminar')):
      break
  if (event == 'cambiar'):
    pass
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
      letra_seleccionada = False              
      orientacion = [True, False]  
      letras = []
      primer_posicion = ultima_posicion = ()
      agregar_posiciones_bloqueadas(posiciones_ocupadas, posiciones_bloqueadas)
      posiciones_ocupadas = OrderedDict()
      turno_jugador = False
      primer_jugada = False
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
        if (event in casillas_especiales):
          if (event == centro and primer_jugada):
              window.Element(event).Update(casillas_especiales[event]['texto'], button_color = casillas_especiales[event]['color'], disabled = False)
          elif (event != centro):
             window.Element(event).Update(casillas_especiales[event]['texto'], button_color = casillas_especiales[event]['color'], disabled = False)      
        else:
          window.Element(event).Update(' ', button_color = ('white', 'green'))
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
  window.Element('turno').Update('jugador' if turno_jugador else 'computadora')
  window.Element('palabra_actual').Update(palabra_formada(letras_jugador, posiciones_ocupadas))
  print(event)

window.Close()
