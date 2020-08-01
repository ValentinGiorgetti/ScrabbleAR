"""
Módulo principal de la ventana del tablero de juego.
"""

from componentes.ventanas.tablero.funciones import *
from componentes.ventanas.general import leer_evento


def main(configuracion, partida_anterior = None):
    """
    Función donde se crea el tablero de juego. Recibe la configuración elegida para la partida, y la partida guardada, 
    en caso de que el usuario haya elegido reanudar la partida anterior.

    El parámetro "partida_anterior" es un diccionario que contiene la información necesaria para reconstruir el estado del tablero
    de la partida anterior. Si es None, significa que el usuario empezó una nueva partida. El parámetro "configuración" es
    otro diccionario que almacena las configuraciones de la partida.

    En caso de que "partida_anterior" sea distinto de None, el usuario eligió reanudar la partida anterior, por lo tanto las variables
    se inicializarán con los valores correspondientes del diccionario.

    Si "partida_anterior" es None, las variables se inicializarán con los valores correspondientes del diccionario "configuración".
    
    "parametros" es un diccionario que almacena variables para controlar la lógica del juego:
    
    parametros = {
                   "letra_seleccionada" : booleano que indica si el jugador seleccionó una letra de su atril,
                   "orientacion" : string que indica la orientación elegida para ubicar las fichas en el tablero ('horizontal' o 'vertical'),
                   "primer_posicion" : tupla que indica la posición de la primer ficha que el usuario ubicó en el tablero,
                   "ultima_posicion" : tupla que indica la posición de la última ficha que el usuario ubicó en el tablero,
                   "jugada" : diccionario ordenado (OrderedDict) que almacena la jugada del jugador. Las claves son las posiciones del tablero
                              ocupadas en la jugada (tuplas) y el valor es la letra ubicada en la casilla correspondiente,
                   "letra" : entero que indica la posición de la letra seleccionada en el atril del jugador,
                   "historial" : string que indica lo ocurrido durante la partida (palabras formadas, puntos, etc.),
                   "fichas_totales" : string que contiene todas las fichas de la bolsa ('AAABBBCC...')
                   "fin_juego" : booleano usado para controlar el fin de la partida
                 }
                 
    "tablero" es un diccionario que contine información para actualizar diferentes widgets de la ventana:
    
    tablero = {
                "posiciones_ocupadas" : diccionario que almacena todas las casillas ocupadas del tablero. Las claves son las posiciones (tupla)
                                        y el valor es la letra ubicada en la casilla,
                "palabras_usadas" : lista que contiene las palabras usadas durante el juego,
                "jugador" : referencia al jugador (instancia de la clase Jugador),
                "computadora" : referencia a la computadora (instancia de la clase Jugador),
                "turno" : string que indica el turno ('computadora' o 'jugador'),
                "contador" : almacena la cantidad máxima de segundos de la partida,
                "bolsa_de_fichas" : diccionario que almacena información sobre las fichas. Las claves son las letras y el valor es otro diccionario
                                    que almacena el puntaje y cantidad de fichas de la letra,
                "primer_jugada" : booleano que indica si se realizó alguna jugada o no,
                "nivel" : string que indica el nivel de la partida ('fácil', 'medio' o 'difícil'),
                "tamanio" : entero que indica la cantidad de filas y columnas del tablero,
                "centro" : tupla que indica la posición de la casilla central del tablero,
                "palabras_validas" : string que indica las palabras válidas para el nivel
              }
    """
    
    tablero, parametros = inicializar_parametros(configuracion, partida_anterior)
    
    window = crear_ventana_tablero(tablero, parametros, partida_anterior)
    
    comenzar = partida_guardada = None

    while True:
        event, values, tiempo = leer_evento(window, 1000)
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
            parametros['fin_juego'], tablero['contador'] = actualizar_tiempo(window, tablero['contador'], tiempo)
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
            if parametros['fin_juego']:
              finalizar_partida(window, tablero)
              comenzar = False
            actualizar_tablero(window, parametros, tablero)

    window.Close()
    return partida_guardada, tablero['jugador'], tablero['computadora']