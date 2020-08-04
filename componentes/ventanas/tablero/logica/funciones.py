"""
Módulo que contiene funciones usadas por el jugador y la computadora.
"""


import random, datetime
from os.path import join
from collections import OrderedDict
from playsound import playsound as reproducir
from pattern.es import parse, verbs, spelling, lexicon


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
    Función que retorna un string con todas las fichas de la bolsa.
    """
    
    return "".join([letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas])
    
    
def repartir_fichas(bolsa_de_fichas, letras):
  """
  Función que reparte 7 fichas de la bolsa en forma aleatoria.
  """
  
  letras.clear()
  for i in range(7):
    letra = letra_random(bolsa_de_fichas)
    letras += [letra]


def actualizar_tabla(window, jugador, computadora):
    """
    Función que actualiza la tabla que muestra el puntaje y los cambios restantes
    de los jugadores.
    """

    tabla = sorted([jugador.informacion(), computadora.informacion()], key = lambda x : x[1], reverse = True)
    window["tabla"].Update(tabla)


def actualizar_tiempo(window, contador, tiempo):
    """
    Función usada para actualizar el contador de la partida.
    """

    temp = round(contador - tiempo)
    contador = 0 if temp <= 0 else temp
    window['tiempo'].Update(datetime.timedelta(seconds = contador), text_color='red' if temp < 60 else 'white')
    window.Refresh()
    
    return contador == 0, contador


def reiniciar_parametros(parametros):
    """
    Función usada para reiniciar algunos parámetros de la partida.
    """

    parametros["letra_seleccionada"] = False
    parametros["orientacion"] = parametros["primer_posicion"] = parametros["ultima_posicion"] = ''
    parametros["jugada"] = OrderedDict()    


def reproducir_sonido_palabra(es_correcta):	
    """
    Función que reproduce un sonido para el caso de que la palabra sea correcta o incorrecta.
    """
    
    reproducir(join("componentes", "sonidos", "palabra_correcta.mp3" if es_correcta else "palabra_incorrecta.mp3"))


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


def letra_random(bolsa_de_fichas):
    """
    Función que devuelve una ficha aleatoria de la bolsa.
    """

    fichas = fichas_totales(bolsa_de_fichas)
    letra = random.choice(fichas)
    bolsa_de_fichas[letra]['cantidad_fichas'] -= 1
    
    return letra


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