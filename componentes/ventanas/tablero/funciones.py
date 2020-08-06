"""
Módulo con las funciones usadas por la ventana del tablero.
"""


import random, datetime, PySimpleGUI as sg
from collections import OrderedDict
from componentes.jugador import Jugador
from componentes.ventanas.general import *
from componentes.ventanas.tablero.logica.funciones import (
    fichas_totales,
    repartir_fichas,
    actualizar_tiempo,
    actualizar_tabla,
    reproducir_sonido_palabra,
)


def crear_ventana_tablero(tablero, parametros, partida_anterior):
    """
    Función usada para crear la ventana del tablero.

    Parámetros:
        - tablero (dict): diccionario que contiene información del tablero.
        - parametros (dict): diccionario que contiene párametros usados para controlar la lógica del juego.
        - partida_anterior (dict): diccionario que contiene información de la partida anterior.

    Retorna:
        - window (sg.Window): ventana del tablero.
    """

    tablero_juego = [
        [
            sg.Button("", size=(3, 1), key=(i, j), pad=(0.5, 0.5), button_color=("white", "green"),)
            for j in range(tablero["tamanio"])
        ]
        for i in range(tablero["tamanio"])
    ]

    fichas_jugador = [
        sg.Button(tablero["jugador"].fichas[i], size=(3, 1), key=i, pad=(0.5, 0.5), button_color=("white", "green"),)
        for i in range(7)
    ]

    fichas_pc = [
        sg.Button("?", size=(3, 1), key=i + 8, pad=(0.5, 0.5), button_color=("white", "green")) for i in range(7)
    ]

    layout_columna1 = (
        [[sg.Text("Fichas de la computadora")]] + [fichas_pc] + [[sg.Text(" ")]] + [x for x in tablero_juego]
    )
    layout_columna1 += [[sg.Text("")]] + [[sg.Text("Fichas del jugador")]] + [fichas_jugador] + [[sg.Text("")]]
    layout_columna1 += [
        [
            sg.Button("Iniciar",),
            sg.Button("Posponer"),
            sg.Button("Pausa", disabled=True),
            sg.Button("Palabras ingresadas", key="palabras_ingresadas", disabled=True),
            sg.Button("Terminar", visible=False),
            sg.Button("Salir"),
        ]
    ]

    columna1 = layout_columna1

    titulo = {"font": ("Consolas", 12), "background_color": "#1d3557", "size": (40, 1)}
    fuente = ("Helvetica", 11)
    nivel = tablero["nivel"]

    columna2 = [
        [sg.Text("Tiempo restante", **titulo)],
        [sg.Text(datetime.timedelta(seconds=tablero["contador"]), key="tiempo", font=fuente)],
        [sg.Text("Nivel", **titulo)],
        [sg.Text(nivel.capitalize(), font=fuente)],
        [sg.Text("Palabras válidas", **titulo)],
        [sg.Text(tablero["palabras_validas"], font=fuente)],
        [sg.Text("Cantidad de fichas en la bolsa", **titulo)],
        [sg.Text(len(fichas_totales(tablero["bolsa_de_fichas"])), font=fuente, key="cantidad_fichas")],
        [sg.Text("Turno", **titulo)],
        [sg.Text("                       ", key="turno", font=fuente)],
        [sg.Text("")],
        [
            sg.Table(
                actualizar_tabla(tablero["jugador"], tablero["computadora"]),
                ["", "Puntaje", "Cambios restantes"],
                key="tabla",
                justification="center",
                num_rows=2,
                hide_vertical_scroll=True,
            )
        ],
        [sg.Text("")],
        [sg.Multiline(parametros["historial"], size=(37, 10), key="historial", disabled=True, autoscroll=True)],
        [sg.Text("")],
        [
            sg.Button("Confirmar palabra", key="confirmar", disabled=True),
            sg.Button("Cambiar fichas", key="cambiar", disabled=True),
            sg.Button("Pasar", disabled=True),
        ],
    ]

    layout = [
        [sg.Column(columna1, **parametros_columna), sg.Column(columna2, pad=((20, 0), (0, 0)), **parametros_columna)]
    ]

    window = sg.Window("  Tablero", layout, **parametros_ventana)

    window["turno"].Update(tablero["turno"])

    parametros["casillas_especiales"] = colocar_posiciones_especiales(
        window, tablero
    )  # {(i, j) : {'color' : ('white', 'blue'), 'texto' : 'F +2', 'modificador' : 2}}

    if partida_anterior:
        restaurar_tablero(window, tablero["posiciones_ocupadas"])

    return window


def ventana_palabras_ingresadas(window, tablero, parametros):
    """
    Función que muestra una ventana con información sobre las palabras formadas
    durante la partida.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - tablero (dict): diccionario que contiene información del tablero.
        - parametros (dict): diccionario que contiene párametros usados para controlar la lógica del juego.
    """

    palabras_ingresadas = tablero["palabras_ingresadas"]

    if not palabras_ingresadas:
        sg.Popup("No se ingresó ninguna palabra\n", **parametros_popup)
        return

    layout = [
        [sg.Text("Palabras ingresadas durante la partida")],
        [sg.Text("")],
        [
            sg.Table(
                sorted(palabras_ingresadas, key=lambda x: x[2], reverse=True),
                ["Palabra", "Clasifiación", "Puntos", "Usuario"],
                justification="center",
            )
        ],
        [sg.Button("Volver")],
    ]
    ventana = sg.Window("  Palabras ingresadas", layout, **parametros_ventana)

    partida_finalizada = parametros["fin_juego"]

    while True:
        event, values, tiempo = leer_evento(ventana, 1000)
        if not partida_finalizada:
            parametros["fin_juego"], tablero["contador"] = actualizar_tiempo(window, tablero["contador"], tiempo)
            if parametros["fin_juego"]:
                break
        if event in ("Volver", None):
            break

    ventana.Close()


def colocar_posiciones_especiales(window, tablero):
    """
    Función que coloca todas las casillas especiales en el tablero.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - tablero (dict): diccionario que contiene información del tablero.

    Retorna:
        - casillas_especiales (dict): diccionario que contiene las casillas especiales.
    """

    malas_nivel_facil =[(4, 8), (5, 9), (4, 10), (3, 9), (8, 14), (9, 13), (10, 14), (9, 15)]
    multiplicador_nivel_facil = [(0,9),(1,8),(1,10),(2,7),(2,11),(3,6),(3,12),(4,5),(4,13), (9,18),(8,17),(10,17),(7,16),(11,16),(6,15),(12,15),(5,14),(13,14)]

    malas_nivel_medio = [(3, 7), (3, 9), (4, 8), (5, 7), (5, 9), (7, 13), (7, 11), (9, 13), (9, 11), (8, 12)]
    multiplicador_nivel_medio = [(0, 8), (1, 7), (1, 9), (2, 6), (2, 10), (3, 5), (3, 11), (8, 16), (7, 15), (9, 15), (6, 14), (10, 14), (5, 13), (11, 13)]

    malas_nivel_dificil=[(0,7),(1,6),(1,8),(2,5),(2,9),(3,4),(3,10),(7,14),(6,13),(8,13),(5,12),(9,12),(4,11),(10,11)]
    multiplicador_nivel_dificil = [(2,7),(3,6),(3,8),(7,12),(6,11),(8,11)]

    mala_actual = -1

    nivel = tablero["nivel"]

    casillas_especiales = {}
    negro = ("white", "black")
    ficha_x2 = lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra, puntaje_ficha * 2)
    ficha_x3 = lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra, puntaje_ficha * 3)
    resto = {-1 : lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra, puntaje_ficha - 1),
             -2 : lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra, puntaje_ficha - 2),
             -3 : lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra, puntaje_ficha - 3)}
    multiplicador_x2 = lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra + 2, puntaje_ficha)
    multiplicador_x3 = lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra + 3, puntaje_ficha)
    
    ficha_x2 = {"parametros_boton" : {"text" : "F x2", "button_color" : ("white", "blue")}, "modificador" : ficha_x2}
    ficha_x3 = {"parametros_boton" : {"text" : "F x3", "button_color" : ("white", "blue")}, "modificador" : ficha_x3}
    multiplicador_x2 = {"parametros_boton" : {"text" : "P x2", "button_color" : ("white", "purple")}, "modificador" : multiplicador_x2}
    multiplicador_x3 = {"parametros_boton" : {"text" : "P x3", "button_color" : ("white", "purple")}, "modificador" : multiplicador_x3}

    for i in range(tablero["tamanio"]):
        for j in range(tablero["tamanio"]):
            pos = (i, j)
            pos_invertida = (j, i)
            if j == i:
                casillas_especiales[pos] = ficha_x2
            elif i + j == tablero["tamanio"] - 1:
                casillas_especiales[pos] = ficha_x3
            elif nivel == "fácil":
                if (pos in malas_nivel_facil) or (pos_invertida in malas_nivel_facil):
                    casillas_especiales[pos] = {"parametros_boton" : {"text" : "F " + str(mala_actual), "button_color" : negro}, "modificador" : resto[mala_actual]} 
                    mala_actual = mala_actual -1 if mala_actual > -3 else -1
                elif (pos in multiplicador_nivel_facil) or (pos_invertida in multiplicador_nivel_facil):
                    if pos in multiplicador_nivel_facil:
                        casillas_especiales[pos] = multiplicador_x3 
                    else:
                        casillas_especiales[pos] = multiplicador_x2 
            elif nivel == "medio":
                if (pos in malas_nivel_medio) or (pos_invertida in malas_nivel_medio):
                    casillas_especiales[pos] = {"parametros_boton" : {"text" : "F " + str(mala_actual), "button_color" : negro}, "modificador" : resto[mala_actual]} 
                    mala_actual = mala_actual -1 if mala_actual > -3 else -1
                elif pos in multiplicador_nivel_medio or pos_invertida in multiplicador_nivel_medio:
                    if pos in multiplicador_nivel_medio:
                        casillas_especiales[pos] = multiplicador_x3 
                    else:
                        casillas_especiales[pos] = multiplicador_x2
            elif nivel == "difícil":
                if (pos in malas_nivel_dificil) or (pos_invertida in malas_nivel_dificil):
                    casillas_especiales[pos] = {"parametros_boton" : {"text" : "F " + str(mala_actual), "button_color" : negro}, "modificador" : resto[mala_actual]} 
                    mala_actual = mala_actual -1 if mala_actual > -3 else -1
                elif pos in multiplicador_nivel_dificil or pos_invertida in multiplicador_nivel_dificil:
                    if pos in multiplicador_nivel_dificil:
                        casillas_especiales[pos] = multiplicador_x3 
                    else:
                        casillas_especiales[pos] = multiplicador_x2
            if pos in casillas_especiales:
                window[pos].Update(**casillas_especiales[pos]["parametros_boton"])

    sumador = lambda multiplicador_palabra, puntaje_ficha: (multiplicador_palabra, puntaje_ficha + 1)
    centro = tablero["centro"]
    casillas_especiales[centro] = {"parametros_boton" : {"text" : "Inicio", "button_color" : ("black", "yellow")}, "modificador" : sumador}
    window[centro].Update(**casillas_especiales[centro]["parametros_boton"])

    return casillas_especiales


def restaurar_tablero(window, posiciones):
    """
    Función que restaura el tablero al estado de la partida anterior.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - posiciones (dict): diccionario que contiene las posiciones a restaurar.
    """

    for posicion in posiciones:
        window[posicion].Update(**posiciones[posicion])


def inicializar_parametros(configuracion, partida_anterior):
    """
    Función que inicializa los parámetros de la partida.

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
                              ocupadas en la jugada (tuplas) y el valor es la posición del atril de la letra ubicada en la casilla correspondiente,
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
                "palabras_validas" : string que indica las palabras válidas para el nivel,
                "palabras_ingresadas" : lista con las palabras ingresadas durante la partida
            }

    Parámetros:
        - configuracion (dict): diccionario que contiene la configuración de la partida.
        - partida_anterior (dict): diccionario que contiene información de la partida anterior.

    Retorna:
        - tablero (dict): diccionario con la información del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
    """

    nivel = configuracion["nivel_seleccionado"]
    configuracion = configuracion[nivel]

    if not partida_anterior:
        tablero = {
            "posiciones_ocupadas": {},
            "palabras_usadas": [],
            "jugador": Jugador(configuracion["nick"], ("white", "red")),
            "computadora": Jugador("Computadora", ("white", "orange")),
            "turno": random.choice(("Computadora", "Jugador")),
            "contador": configuracion["tiempo"] * 60,
            "bolsa_de_fichas": configuracion["fichas"],
            "primer_jugada": True,
            "nivel": nivel,
            "tamanio": 15 if nivel == "difícil" else (17 if nivel == "medio" else 19),
            "centro": (7, 7) if nivel == "difícil" else ((8, 8) if nivel == "medio" else (9, 9)),
            "palabras_validas": configuracion["palabras_validas"],
            "palabras_ingresadas": [],
        }
        repartir_fichas(tablero["bolsa_de_fichas"], tablero["jugador"].fichas)
        repartir_fichas(tablero["bolsa_de_fichas"], tablero["computadora"].fichas)
    else:
        tablero = partida_anterior

    parametros = {
        "letra_seleccionada": False,
        "orientacion": "",
        "primer_posicion": "",
        "ultima_posicion": "",
        "jugada": OrderedDict(),
        "letra": "",
        "historial": "                  Historial de la partida",
        "fin_juego": False,
    }

    return tablero, parametros


def iniciar_partida(window, parametros, partida_anterior):
    """
    Función que inicia la partida.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - partida_anterior (dict): diccionario que contiene información de la partida anterior.

    Retorna:
        - (bool): siempre devuelve True, se utiliza para indicar que la partida inició.
    """

    parametros["historial"] += "\n\n - El jugador " + ("reanudó" if partida_anterior else "inició") + " la partida."
    window["historial"].Update(parametros["historial"])
    for i in ("Pausa", "confirmar", "cambiar", "Pasar", "palabras_ingresadas"):
        window[i].Update(disabled=False)
    window["Iniciar"].Update(visible=False)
    window["Salir"].Update(visible=False)
    window["Terminar"].Update(visible=True)

    return True


def pausar(window, comenzar):
    """
    Función usada para pausar la partida.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - comenzar (bool): indica si la partida está iniciada o no. 

    Retorna:
        - (bool): devuelve lo opuesto al parámetro comenzar, se utiliza para reanudar o pausar.
    """

    window["Pausa"].Update(button_color=("white", "red") if comenzar else sg.DEFAULT_BUTTON_COLOR)
    for i in ("confirmar", "cambiar", "Pasar"):
        window[i].Update(disabled=comenzar)

    return not comenzar


def posponer(tablero, jugada):
    """
    Función usada para posponer la partida.

    Parámetros:
        - tablero (dict): diccionario con la información del tablero.
        - jugada (OrderedDict): almacena la jugada del jugador.

    Retorna:
        - (bool): indica si se puede posponer la partida o no.
        - (dict): devuelve el tablero.
    """

    if not jugada:
        sg.Popup("Se guardaron los datos de la partida\n", title="  Atención")
        return True, tablero
    else:
        sg.Popup("Primero debe levantar sus fichas\n", title="  Atención")
        return False, None


def pasar(window, parametros, tablero):
    """
    Función usada para pasar el turno a la computadora.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - tablero (dict): diccionario con la información del tablero.
    """

    if parametros["jugada"]:
        sg.Popup("Primero debe levantar sus fichas\n")
    else:
        if parametros["letra_seleccionada"]:
            window[parametros["letra"]].Update(button_color=("white", "green"))
            parametros["letra_seleccionada"] = False
        tablero["turno"] = "Computadora"
        window["turno"].Update("Computadora")


def seleccionar_ficha(window, parametros, event, color):
    """
    Función usada para que el usuario seleccione una ficha.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - event (int): indica la posición de la letra seleccionada en el atril del jugador.
        - color (tuple): tupla que indica el color de las fichas del usuario.
    """

    if parametros["letra_seleccionada"]:
        window[parametros["letra"]].Update(button_color=("white", "green"))
    window[event].Update(button_color=color)
    parametros["letra"] = event
    parametros["letra_seleccionada"] = True


def finalizar_partida(window, tablero, parametros, fichas_pc=None):
    """
    Función que muestra el mensaje de fin de la partida.

    Se informa el ganador o si hubo un empate.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - tablero (dict): diccionario con la información del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.

    Retorna:
        - (bool): siempre devuelve false, indica que la partida terminó.
    """

    if parametros["jugada"]:
        reproducir_sonido_palabra(False)

    jugador = tablero["jugador"]
    computadora = tablero["computadora"]
    bolsa_de_fichas = tablero["bolsa_de_fichas"]

    for usuario in (jugador, computadora):
        for letra in usuario.fichas:
            usuario.puntaje   -= bolsa_de_fichas[letra]["puntaje"]

    actualizar_tabla(jugador, computadora, window)

    fichas_reales_pc = parametros["fichas_reales_pc"] if "fichas_reales_pc" in parametros else computadora.fichas
    for i, letra in zip(range(8, 15), fichas_reales_pc):
        window[i].Update(letra)

    for key in ("Posponer", "Pausa", "confirmar", "cambiar", "Pasar"):
        window[key].Update(button_color=sg.DEFAULT_BUTTON_COLOR, disabled=True)

    aux = "el jugador" if jugador.nick == "Jugador" else jugador.nick
    mensaje = "¡Fin de la partida! "
    if jugador.puntaje > computadora.puntaje:
        mensaje += f"Ganó {aux} con {jugador.puntaje} puntos."
    elif jugador.puntaje < computadora.puntaje:
        mensaje += f"Ganó la computadora con {computadora.puntaje} puntos."
    else:
        mensaje += "Hubo un empate."
    sg.Popup(mensaje + "\n", title="  Fin de la partida")

    historial = parametros["historial"]
    historial += "\n\n - " + mensaje
    window["historial"].Update(historial)
    window["Salir"].Update(visible=True)
    window["Terminar"].Update(visible=False)

    return False