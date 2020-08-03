"""
Módulo con las funciones usadas por la ventana del tablero.
"""


import random, PySimpleGUI as sg
from pattern.es import parse, verbs, spelling, lexicon
import datetime
from collections import OrderedDict
from componentes.jugador import Jugador
from os.path import join
from componentes.ventanas.general import *


def crear_ventana_tablero(tablero, parametros, partida_anterior):
    """
    Función usada para crear la ventana del tablero.
    """

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
            sg.Button("Confirmar palabra", key = "confirmar", disabled = True),
            sg.Button("Cambiar fichas", key = "cambiar", disabled = True),
            sg.Button("Pasar", disabled = True),
        ],
    ]

    layout = [[sg.Column(columna1, **parametros_columna), sg.Column(columna2, pad = ((20, 0), (0, 0)), **parametros_columna)]]

    window = sg.Window("Tablero", layout, **parametros_ventana)
    
    parametros['casillas_especiales'] = colocar_posiciones_especiales(window, tablero) # {(i, j) : {'color' : ('white', 'blue'), 'texto' : 'F +2', 'modificador' : 2}}

    if partida_anterior:
        restaurar_tablero(window, tablero["posiciones_ocupadas"])
        
    return window


def colocar_posiciones_especiales(window, tablero):
  """
  Función que coloca todas las casillas especiales en el tablero.
  """
  
  malas_nivel_facil =[(4, 8), (5, 9), (4, 10), (3, 9), (8, 14), (9, 13), (10, 14), (9, 15)]
  multiplicador_nivel_facil = [(0,9),(1,8),(1,10),(2,7),(2,11),(3,6),(3,12),(4,5),(4,13), (9,18),(8,17),(10,17),(7,16),(11,16),(6,15),(12,15),(5,14),(13,14)]
  
  malas_nivel_medio = [(3, 7), (3, 9), (4, 8), (5, 7), (5, 9), (7, 13), (7, 11), (9, 13), (9, 11), (8, 12)]
  multiplicador_nivel_medio = [(0, 8), (1, 7), (1, 9), (2, 6), (2, 10), (3, 5), (3, 11), (8, 16), (7, 15), (9, 15), (6, 14), (10, 14), (5, 13), (11, 13)]
  
  malas_nivel_dificil=[(0,7),(1,6),(1,8),(2,5),(2,9),(3,4),(3,10),(7,14),(6,13),(8,13),(5,12),(9,12),(4,11),(10,11)]
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


def restaurar_tablero(window, posiciones):
    """
    Función que restaura el tablero al estado de la partida anterior.
    """

    for posicion in posiciones:
        window[posicion].Update(posiciones[posicion], button_color = ('white', 'red')) # button_text, button_color


def inicializar_parametros(configuracion, partida_anterior):
  """
  Función que inicializa los parámetros de la partida.
  """

  if not partida_anterior:
    tablero = {
      "posiciones_ocupadas" : {},
      "palabras_usadas" : [],
      "jugador" : Jugador(configuracion["nick"], ('white', 'blue')),
      "computadora" : Jugador("Computadora", ('white', 'red')),
      "turno" : random.choice(('Computadora', 'Jugador')),
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


def iniciar_partida(window, parametros, partida_anterior):
    """
    Función que inicia la partida.
    """

    parametros['historial'] += '\n\n - El jugador ' + ('reanudó' if partida_anterior else 'inició') + ' la partida.'
    window['historial'].Update(parametros['historial'])
    for i in ("Pausa", "confirmar", "cambiar", "Pasar"):
        window[i].Update(disabled = False)
    window["Iniciar"].Update(disabled = True)
    
    return True
    
    
def pausar(window, comenzar):
    """
    Función usada para pausar la partida.
    """
    
    window["Pausa"].Update(button_color = ("white", "red") if comenzar else sg.DEFAULT_BUTTON_COLOR)
    for i in ("confirmar", "cambiar", "Pasar"):
        window[i].Update(disabled = comenzar)
   
    return not comenzar
   
   
def posponer(tablero, jugada):
    """
    Función usada para posponer la partida.
    """

    if (not jugada):
        sg.Popup("Se guardaron los datos de la partida", title = "Atención")
        return True, tablero
    else:
      sg.Popup("Primero debe levantar sus fichas", title = "Atención")
      return False, None


def pasar(window, parametros, tablero):
    """
    Función usada para pasar el turno a la computadora
    """

    if parametros['jugada']:
        sg.Popup("Primero debe levantar sus fichas")
    else:
        if parametros['letra_seleccionada']:
            window[parametros['letra']].Update(button_color = ("white", "green"))
            parametros['letra_seleccionada'] = False
        tablero['turno'] = 'Computadora'
        window['turno'].Update('Computadora')


def repartir_fichas(bolsa_de_fichas, letras):
  """
  Función que reparte 7 fichas de la bolsa en forma aleatoria.
  """
  
  letras.clear()
  fichas = actualizar_fichas_totales(bolsa_de_fichas)
  for i in range(7):
    letra = random.choice(fichas)
    while (bolsa_de_fichas[letra]['cantidad_fichas'] <= 0):
      letra = random.choice(fichas)
    letras += [letra]
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
    fichas = actualizar_fichas_totales(bolsa_de_fichas)


def seleccionar_ficha(window, parametros, event):
    """
    Función usada para que el usuario seleccione una ficha.
    """

    if parametros['letra_seleccionada']:
        window[parametros['letra']].Update(button_color = ("white", "green"))
    window[event].Update(button_color = ("white", "red"))
    parametros['letra'] = event
    parametros['letra_seleccionada'] = True
    
    
def actualizar_tiempo(window, contador, tiempo):
    """
    Función usada para actualizar el contador de la partida.
    """

    temp = round(contador - tiempo)
    contador = 0 if temp <= 0 else temp
    window['tiempo'].Update(datetime.timedelta(seconds = contador), text_color='red' if temp < 60 else 'white')
    window.Refresh()
    
    return contador == 0, contador


def es_palabra(nivel, palabras_validas, palabra):
  """
  Función que verifica que la palabra sea válida correspondiente al nivel de la partida.
  """

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
    
    
def fichas_totales(bolsa_de_fichas):
  """
  Función que retorna la cantidad total de fichas que quedan en la bolsa.
  """

  total = 0
  for letra in bolsa_de_fichas:
    total += bolsa_de_fichas[letra]['cantidad_fichas'] 
  return total  


def reproducir_sonido_palabra(es_correcta):	
    """
    Función que reproduce un sonido para el caso de que la palabra sea correcta o incorrecta.
    """
    
    reproducir(join("componentes", "sonidos", "palabra_correcta.mp3" if es_correcta else "palabra_incorrecta.mp3"))


def reiniciar_parametros(parametros):
    """
    Función usada para reiniciar algunos parámetros de la partida.
    """

    parametros["letra_seleccionada"] = False
    parametros["orientacion"] = parametros["primer_posicion"] = parametros["ultima_posicion"] = ''
    parametros["jugada"] = OrderedDict()


def quedan_fichas(bolsa_de_fichas, cantidad_fichas = 7):
    """
    Función que verifica si hay suficientes fichas en la bolsa para repartir.
    """

    contador = 0
    for letra in bolsa_de_fichas:
        contador += bolsa_de_fichas[letra]['cantidad_fichas']
        if (contador >= cantidad_fichas):
            return True
    return False
    
        
def actualizar_fichas_totales(bolsa_de_fichas):
    """
    Función que retorna un string con todas las fichas de la bolsa.
    """
    
    return "".join([letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas])


def actualizar_tabla(window, jugador, computadora):

    tabla = sorted([jugador.informacion(), computadora.informacion()], key = lambda x : x[1], reverse = True)
    window["tabla"].Update(tabla)


def finalizar_jugada(window, parametros, tablero, palabra, puntos_jugada, jugador, texto):
    """
    Función que brinda información sobre la palabra formada y suma el puntaje de la jugada.
    """

    tipo = parse(palabra.lower(), chunks = False).split('/')[1] 
    tipo_palabra = 'sustantivo' if tipo.find('NN') != -1 else ('verbo' if tipo.find('VB') != -1 else 'adjetivo')
    parametros['historial'] += f'\n\n - {texto} formó la palabara "{palabra}" ({tipo_palabra}) y sumó {puntos_jugada} puntos.'
    window['historial'].Update(parametros['historial'])
    jugador.puntaje += puntos_jugada
    tablero['primer_jugada'] = False
    actualizar_tabla(window, tablero['jugador'], tablero['computadora'])


def sumar_casilla(casillas_especiales, posicion, letra, puntos_jugada, multiplicador, tablero):
  """
  Función que actualiza la cantidad de puntos de la jugada, obtenidos al pasar por una casilla, 
  sumando el puntaje de la ficha. Si la casilla es especial, también se suma el modificador 
  correspondiente o se acumula el multiplicador de la palabra.
  """
  
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
  

def contar_jugada(window, palabra, posiciones_tablero, tablero, casillas_especiales):
    """
    Función para contar los puntos obtenidos al formar una palabra.
    """

    posiciones_ocupadas = []
    multiplicador = puntos_jugada = 0
    for letra, posicion in zip(palabra, posiciones_tablero):
        multiplicador, puntos_jugada = sumar_casilla(casillas_especiales, posicion, letra, puntos_jugada, multiplicador, tablero) 
        posiciones_ocupadas += [posicion]
    puntos_jugada = 0 if puntos_jugada < 0 else (puntos_jugada if multiplicador == 0 else puntos_jugada * multiplicador)
    
    return posiciones_ocupadas, puntos_jugada


def finalizar_partida(window, tablero):
  """
  Función que muestra el mensaje de fin de la partida.
  
  Se informa el ganador o si hubo un empate.
  """
  
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
      
  for key in ('Iniciar', 'Posponer', 'Pausa', 'Terminar', 'confirmar', 'cambiar', 'Pasar'):
    window[key].Update(button_color = sg.DEFAULT_BUTTON_COLOR, disabled = True)

  aux = 'el jugador' if jugador.nick != 'Jugador' else "jugador.nick"
  mensaje = ''
  if (jugador.puntaje > computadora.puntaje):
    mensaje = f'Ganó {aux} con {jugador.puntaje} puntos'
  elif (jugador.puntaje < computadora.puntaje):
    mensaje = f'Ganó la computadora con {computadora.puntaje} puntos'
  else: 
    mensaje = 'Hubo un empate'
  sg.Popup(mensaje, title = 'Fin de la partida')
  
  window['Salir'].Update(visible = True)

  return False