import random, PySimpleGUI as sg
from random import randint
from pattern.es import parse, verbs, spelling, lexicon
from collections import OrderedDict
from itertools import permutations

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

def jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas):
  orientacion = random.randint(0, 100) % 2 == 0   # Si es par la orientacion es horizontal
  print(letras_pc)
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
      if (orientacion):
        for letra in palabra:
          window.Element((i, j)).Update(letra, button_color = ('white', 'red'))
          posiciones_bloqueadas += [(i,j)]
          j += 1
      else:
        for letra in palabra:
          window.Element((i, j)).Update(letra, button_color = ('white', 'red'))
          posiciones_bloqueadas += [(i,j)]
          i += 1
    else:
      posicion_valida = False
      while (not posicion_valida):
        posicion_valida = True
        if (orientacion):
          i = random.randint(0, FILAS - 1)
          j = random.randint(0, COLUMNAS - 9)
        else:
          i = random.randint(0, FILAS - 9)
          j = random.randint(0, COLUMNAS - 1)
        for x in range(len(palabra)):
          if (orientacion):
            if ((i, j + x) in posiciones_bloqueadas):
              posicion_valida = False
              break
          else:
            if ((i + x, j) in posiciones_bloqueadas):
              posicion_valida = False
              break
      if (orientacion):
        for letra in palabra:
          window.Element((i, j)).Update(letra, button_color = ('white', 'red'))
          posiciones_bloqueadas += [(i,j)]
          j += 1
      else:
        for letra in palabra:
          window.Element((i, j)).Update(letra, button_color = ('white', 'red'))
          posiciones_bloqueadas += [(i,j)]
          i += 1  
    for letra in palabra:
      x = random.randint(8, 14)
      while (x in fichas_usadas_pc):
        x = random.randint(8, 14)
      window.Element(x).Update(button_color = ('white', 'red'), disabled = True)
      fichas_usadas_pc += [x]
      letras_pc.remove(letra)
    return True
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
      bolsa_de_fichas[letra] -= 1
    print('nuevas letras', letras_pc)
    return False

def colocar_fichas_especiales(nivel, casillas_especiales, FILAS, COLUMNAS):
  malas_NivelFacil =[(1,7),(1,11),(2,8),(2,10),(3,9),
                   (7,1),(11,1),(8,2),(10,2),(9,3),
                   (17,7),(11,17),(8,16),(10,16),(9,15),
                   (7,17),(17,11),(16,18),(16,10),(15,9)]

  malas_NivelMedio=[(2,7),(2,9),(3,8),(4,7),(4,9),
                    (7,2),(9,4),(8,3),(7,4),(9,2),
                    (7,14),(7,12),(9,14),(9,12),(8,13),
                    (14,7),(12,7),(14,9),(12,9),(13,8)]

  malas_NivelDificil=[(0,5),(0,9),(1,6),(1,8),(2,7),(3,6),(3,8),(4,7),
                      (5,0),(9,0),(6,1),(8,1),(7,2),(6,3),(8,3),(7,4),
                      (14,5),(14,9),(13,6),(13,8),(12,7),(11,6),(11,8),(10,7),
                      (5,14),(9,14),(6,13),(8,13),(7,12),(6,11),(8,11),(7,10)]

  for i in range(FILAS):
    for j in range(COLUMNAS):
      tupla=(i,j)
      if(tupla!=centro):
        if(j==i or i+j==FILAS-1):
          tablero_juego[i][j] = sg.Button('Buena', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'blue'))
          casillas_especiales[tupla] = {'color' : ('white', 'blue'), 'texto' : 'Buena'}
        if (nivel == 1) and (tupla in malas_NivelFacil):
          tablero_juego[i][j]=sg.Button('Mala', size=(4, 2), key=(i, j), pad=(0.5, 0.5), button_color=('white', 'black'))
          casillas_especiales[tupla] = {'color' : ('white', 'black'), 'texto' : 'Mala'}
        elif (nivel == 2) and (tupla in malas_NivelMedio):
          tablero_juego[i][j]=sg.Button('Mala', size=(4, 2), key=(i, j), pad=(0.5, 0.5), button_color=('white', 'black'))
          casillas_especiales[tupla]={'color': ('white', 'black'), 'texto': 'Mala'}
        elif (nivel== 3) and (tupla in malas_NivelDificil):
          tablero_juego[i][j]=sg.Button('Mala', size=(4, 2), key=(i, j), pad=(0.5, 0.5), button_color=('white', 'black'))
          casillas_especiales[tupla]={'color': ('white', 'black'), 'texto': 'Mala'}

def agregar_posiciones_bloqueadas(posiciones_ocupadas, posiciones_bloqueadas):
  for posicion in posiciones_ocupadas:
    posiciones_bloqueadas += [posicion]

def repartir_fichas(bolsa_de_fichas, letras_jugador, letras_pc):
  abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  for i in range(7):
    letra = random.choice(abecedario)
    letras_jugador += [letra]
    bolsa_de_fichas[letra] -= 1
    letra = random.choice(abecedario)
    letras_pc += [letra]
    bolsa_de_fichas[letra] -= 1

FILAS = COLUMNAS = 15

centro = (int(FILAS / 2), int(FILAS / 2))

casillas_buenas = 3
casillas_malas = 5

palabras_validas = {'adjetivos' : ("AO", "JJ","AQ","DI","DT"), 
                    'sustantivos': ("NC", "NN", "NCS","NCP", "NNS","NP", "NNP","W"), 
                    'verbos': ("VAG", "VBG", "VAI","VAN", "MD", "VAS" , "VMG" , "VMI", "VB", "VMM" ,"VMN" , "VMP", "VBN","VMS","VSG",  "VSI","VSN", "VSP","VSS")}

bolsa_de_fichas = {'A' : 10, 'B' : 10, 'C' : 10, 'D' : 10, 'E' : 10, 'F' : 10, 'G' : 10, 'H' : 10, 'I' : 10, 'J' : 10, 'K' : 10, 'L' : 10, 'M' : 10, 'N' : 10, 'O' : 10, 'P' : 10, 'Q' : 10, 'R' : 10, 'S' : 10, 'T' : 10, 'U' : 10, 'V' : 10, 'W' : 10, 'X' : 10, 'Y' : 10, 'Z' : 10}

letras_jugador = []
letras_pc = []

repartir_fichas(bolsa_de_fichas, letras_jugador, letras_pc)

print(bolsa_de_fichas)

tablero_juego = [[sg.Button('', size = (4, 2), key = (i, j), pad = (0.5, 0.5), button_color = ('white', 'green')) for j in range(COLUMNAS)] for i in range(FILAS)]

tablero_juego[centro[0]][centro[1]] = sg.Button('Inicio', size = (4, 2), key = (centro[0], centro[1]), pad = (0.5, 0.5), button_color = ('white', 'yellow'))

casillas_especiales = {centro : {'color' : ('white', 'yellow'), 'texto' : 'Inicio'}}

colocar_fichas_especiales(3, casillas_especiales, FILAS, COLUMNAS)

fichas_jugador = [sg.Button(letras_jugador[i], size= (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

fichas_pc = [sg.Button('?', size= (4, 2), key = i + 8, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(7)]

layout = [[sg.Text('Fichas de la computadora')]] + [fichas_pc] + [[sg.Text(' ')]] + [x for x in tablero_juego] 
layout += [[sg.Text('Fichas del jugador')]] + [fichas_jugador]
layout += [[sg.Button('Posponer'), sg.Button('Pausa'), sg.Button('Terminar')]]

columna1 = layout

columna2 = [[sg.Text('Tiempo restante'), sg.Text(' ', key = 'tiempo')],
            [sg.Text('Puntajes')],
            [sg.Text('Jugador'), sg.Text(' ', key = 'puntaje_jugador')],
            [sg.Text('Computadora'), sg.Text(' ', key = 'puntaje_computadora')],
            [sg.Text('Turno actual'), sg.Text('                  ', key = 'turno')],
            [sg.Text('Palabra actual'), sg.Text('                 ', key = 'palabra_actual')],
            [sg.Button('Confirmar palabra', key = 'confirmar'), sg.Button('Cambiar fichas', key = 'cambiar'), sg.Button('Pasar', key = 'pasar')],
            [sg.Text('Cambios restantes'), sg.Text(' ', key = 'cambios')]]

layout = [[sg.Column(columna1), sg.Column(columna2)]]  

window = sg.Window('Tablero', layout)

abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') # 

layout_cambiar_fichas = [[sg.Button('Cambiar todas', key = 'todas'), sg.Button('Cambiar algunas', key = 'algunas')],
                         [sg.Text('Seleccione las fichas que quiere intercambiar', key = 'texto1', visible = False)],
                         [sg.Text('Fichas en la bolsa', key = 'texto2', visible = False)],
                         [sg.Button(abecedario[i] + ' x' + str(bolsa_de_fichas[abecedario[i]]), size= (4, 2), key = abecedario[i], pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(14)],
                         [sg.Button(abecedario[i] + ' x' + str(bolsa_de_fichas[abecedario[i]]), size= (4, 2), key = i, pad = (0.5, 0.5), button_color = ('white', 'green')) for i in range(14,26)]]

ventana_cambiar_fichas = sg.Window('Cambiar fichas', layout_cambiar_fichas)

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

# print('palabritas', es_palabra('su'), es_palabra('las'))

while True:
  event, values = window.Read()
  if (not turno_jugador):
    if (jugar_computadora(letras_pc, primer_jugada, centro, casillas_especiales, fichas_usadas_pc, posiciones_bloqueadas, bolsa_de_fichas)):
      primer_jugada = False
    turno_jugador = True
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