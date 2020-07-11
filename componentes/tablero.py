import random, PySimpleGUI as sg
from componentes.jugador import Jugador
from componentes.funciones.funciones_tablero import *
from random import randint
from collections import OrderedDict
import sys, datetime


def jugar(configuracion, partida):

    """
    Esta es la función "principal", donde se crea el tablero de juego y se desarrolla la lógica más importante del mismo.
    Recibe la configuración elegida para la partida, y la partida guardada, en caso de que el usuario haya elegido reanudar
    la partida anterior.

    El parámetro "partida" es un diccionario que contiene la información necesaria para reconstruir el estado del tablero
    de la partida anterior. Si es None, significa que el usuario empezó una nueva partida. El parámetro "configuración" es
    otro diccionario que almacena las configuraciones de la partida.

    En caso de que "partida" sea distinto de None, el usuario eligió reanudar la partida anterior, por lo tanto las variables
    se inicializarán con los valores correspondientes del diccionario.

    Si "partida" es None, las variables se inicializarán con los valores correspondientes del diccionario "configuración".
    """
    # print(configuracion)
    # print(partida)

    nivel = configuracion["nivel"] if partida == None else partida["nivel"]
    FILAS = COLUMNAS = 15 if nivel == "dificil" else (17 if nivel == "medio" else 19)
    # print('NIVEL', nivel, 'FILAS', FILAS)
    centro = (int(FILAS / 2), int(FILAS / 2))
    palabra_valida = (
        configuracion["palabra valida"]
        if partida == None
        else partida["palabra valida"]
    )
    contador = (
        configuracion["tiempo"] * 60 if partida == None else partida["contador"]
    )  # contador en segundos
    bolsa_de_fichas = (
        configuracion["fichas"] if partida == None else partida["bolsa de fichas"]
    )
    # bolsa_de_fichas = {letra : {'cantidad_fichas' : 1, 'puntaje_ficha' : 1}}

    # print('Fichas totales:', fichas_totales(bolsa_de_fichas))
    if partida == None:
        letras_jugador = []  # Letras del atril
        letras_pc = []
        repartir_fichas(bolsa_de_fichas, letras_jugador)
        repartir_fichas(bolsa_de_fichas, letras_pc)
    else:
        letras_jugador = partida["letras jugador"]
        letras_pc = partida["letras computadora"]
    # print('Fichas totales:', fichas_totales(bolsa_de_fichas))

    fichas = "".join(
        [letra * bolsa_de_fichas[letra]["cantidad_fichas"] for letra in bolsa_de_fichas]
    )

    tablero_juego = [
        [
            sg.Button(
                "",
                size=(3, 1),
                key=(i, j),
                pad=(0.5, 0.5),
                button_color=("white", "green"),
            )
            for j in range(COLUMNAS)
        ]
        for i in range(FILAS)
    ]

    casillas_especiales = (
        {}
    )  # {(i, j) : {'color' : ('white', 'blue'), 'texto' : 'F +2', 'modificador' : 2}}
    colocar_posiciones_especiales(
        tablero_juego, nivel, casillas_especiales, FILAS, COLUMNAS, centro
    )

    fichas_jugador = [
        sg.Button(
            letras_jugador[i],
            size=(3, 1),
            key=i,
            pad=(0.5, 0.5),
            button_color=("white", "green"),
        )
        for i in range(7)
    ]

    fichas_pc = [
        sg.Button(
            "?",
            size=(3, 1),
            key=i + 8,
            pad=(0.5, 0.5),
            button_color=("white", "green"),
            disabled=True,
        )
        for i in range(7)
    ]

    layout = (
        [[sg.Text("Fichas de la computadora")]]
        + [fichas_pc]
        + [[sg.Text(" ")]]
        + [x for x in tablero_juego]
    )
    layout += [[sg.Text("Fichas del jugador")]] + [fichas_jugador]
    layout += [
        [
            sg.Button("Iniciar", button_color=None),
            sg.Button("Posponer"),
            sg.Button("Pausa", disabled=True, button_color=("white", "blue")),
            sg.Button("Terminar"),
        ]
    ]

    columna1 = layout

    computadora = Jugador() if partida == None else partida["computadora"]
    jugador = Jugador() if partida == None else partida["jugador"]

    letra_seleccionada = False
    orientacion = [
        True,
        False,
    ]  # Si define la orientación, orientacion[0] = True. Si la orientación es vertical, orientacion[1] = False, si es horizontal orientacion[1] = True.
    primer_posicion = ultima_posicion = ()
    posiciones_ocupadas = (
        OrderedDict() if partida == None else partida["posiciones ocupadas"]
    )  # {(i, j) : posicion del atril de la ficha colocada} se resetea por cada jugada
    primer_jugada = True if partida == None else partida["primer jugada"]
    turno_jugador = (
        random.randint(0, 100) % 2 == 0 if partida == None else partida["turno"]
    )  # si el número aleatorio es par, comienza el jugador
    posiciones_bloqueadas = (
        [] if partida == None else partida["posiciones bloqueadas"]
    )  # [posicion1, posicion2]
    fichas_usadas_pc = (
        [] if partida == None else partida["fichas usadas pc"]
    )  # [posicion_atril, ..]
    comenzar = False
    letra = ""

    columna2 = [
        [
            sg.Text("Tiempo restante"),
            sg.Text(datetime.timedelta(seconds=contador), key="tiempo"),
        ],
        [sg.Text("Nivel: " + nivel)],
        [
            sg.Text(
                "Palabras válidas: "
                + (
                    "adjetivos, sustantivos y verbos"
                    if nivel == "facil"
                    else ("adjetivos y verbos" if nivel == "medio" else palabra_valida)
                )
            )
        ],
        [sg.Text("Puntajes")],
        [
            sg.Text("Jugador:"),
            sg.Text(str(jugador.get_puntaje()) + "     ", key="puntaje_jugador"),
        ],
        [
            sg.Text("Computadora:"),
            sg.Text(
                str(computadora.get_puntaje()) + "      ", key="puntaje_computadora"
            ),
        ],
        [
            sg.Text("Turno actual:"),
            sg.Text("jugador" if turno_jugador else "computadora", key="turno"),
        ],
        [
            sg.Text("Palabra actual:"),
            sg.Text("                 ", key="palabra_actual"),
        ],
        [
            sg.Text("Cambios restantes jugador:"),
            sg.Text(jugador.get_cambios_restantes(), key="cambios_jugador"),
            sg.Text("Cambios restantes pc:"),
            sg.Text(computadora.get_cambios_restantes(), key="cambios_pc"),
        ],
        [
            sg.Text("Cantidad de fichas en la bolsa:"),
            sg.Text(fichas_totales(bolsa_de_fichas), key="cantidad_fichas"),
        ],
        [sg.Text("")],
        [
            sg.Button("Confirmar palabra", key="confirmar"),
            sg.Button("Cambiar fichas", key="cambiar"),
            sg.Button("Pasar", key="pasar"),
        ],
    ]

    layout = [[sg.Column(columna1), sg.Column(columna2)]]

    window = sg.Window("Tablero", layout).Finalize()

    if partida != None:
        restaurar_tablero(window, partida["posiciones"])

    posiciones = (
        {} if partida == None else partida["posiciones"]
    )  # {(i, j) : letra}  posiciones ocupadas del tablero
    partida = None

    while True:
        event = window.Read(timeout=1000)[0]  # milisegundos
        if event == None:
            break
        elif event == "Iniciar":
            comenzar = True
            window.Element("Iniciar").Update(
                disabled=True, button_color=("white", "red")
            )
            window.Element("Pausa").Update(disabled=False)
        elif event == "Pausa":
            comenzar = not comenzar
            window.Element("Pausa").Update(
                button_color=("white", "red") if (not comenzar) else ("white", "blue")
            )
        elif event == "Posponer":
            partida = {
                "jugador": jugador,
                "letras jugador": letras_jugador,
                "computadora": computadora,
                "letras computadora": letras_pc,
                "posiciones ocupadas": posiciones_ocupadas,
                "primer jugada": primer_jugada,
                "turno": turno_jugador,
                "posiciones bloqueadas": posiciones_bloqueadas,
                "fichas usadas pc": fichas_usadas_pc,
                "nivel": nivel,
                "palabra valida": palabra_valida,
                "contador": contador,
                "bolsa de fichas": bolsa_de_fichas,
                "posiciones": posiciones,
            }
            sg.Popup("Se guardaron los datos de la partida", title="Atención")
            break
        elif event == "Terminar":
            imprimir_mensaje_fin(jugador, computadora)
            break
        window.Element("turno").Update("jugador" if turno_jugador else "computadora")
        if not turno_jugador and comenzar:
            jugada, contador = jugar_computadora(
                letras_pc,
                primer_jugada,
                centro,
                casillas_especiales,
                fichas_usadas_pc,
                posiciones_bloqueadas,
                bolsa_de_fichas,
                computadora,
                window,
                FILAS,
                COLUMNAS,
                posiciones,
                nivel,
                palabra_valida,
                contador,
            )
            if jugada >= 0:
                computadora.actualizar_puntaje(jugada)
                window.Element("puntaje_computadora").Update(computadora.get_puntaje())
                primer_jugada = False
            else:
                computadora.actualizar_cambios_restantes()
            turno_jugador = True
            window.Element("turno").Update(
                "jugador" if turno_jugador else "computadora"
            )
        if event != "__TIMEOUT__" and comenzar:
            if event == "cambiar":
                if len(posiciones_ocupadas) > 0:
                    sg.Popup(
                        "Primero debe levantar sus fichas",
                        title="Atención",
                        non_blocking=True,
                        auto_close_duration=5,
                        auto_close=True,
                    )
                else:
                    # print('Originales:', letras_jugador)
                    cambio, contador = cambiar_fichas(
                        jugador, letras_jugador, bolsa_de_fichas, contador, window
                    )
                    if cambio:
                        jugador.actualizar_cambios_restantes()
                        window.Element("cambios_jugador").Update(
                            jugador.get_cambios_restantes()
                        )
                        letra_seleccionada = False
                        orientacion = [True, False]
                        primer_posicion = ultima_posicion = ()
                        posiciones_ocupadas = OrderedDict()
                        turno_jugador = False
                        if jugador.get_cambios_restantes() == 0:
                            window.Element("cambiar").Update(
                                disabled=True, button_color=("white", "red")
                            )
                    # print('Cambiadas:', letras_jugador)
            elif event == "pasar":
                if len(posiciones_ocupadas) > 0:
                    sg.Popup(
                        "Primero debe levantar sus fichas",
                        title="Atención",
                        non_blocking=True,
                        auto_close_duration=5,
                        auto_close=True,
                    )
                else:
                    if letra_seleccionada:
                        window.Element(letra).Update(button_color=("white", "green"))
                        letra_seleccionada = False
                    turno_jugador = False
            elif event == "confirmar":
                if letra_seleccionada:
                    window.Element(letra).Update(button_color=("white", "green"))
                    letra_seleccionada = False
                if verificar_palabra(
                    letras_jugador,
                    posiciones_ocupadas,
                    posiciones_bloqueadas,
                    centro,
                    primer_jugada,
                    nivel,
                    palabra_valida,
                ):
                    puntos_jugada = contar_puntos_jugador(
                        posiciones_ocupadas,
                        casillas_especiales,
                        bolsa_de_fichas,
                        letras_jugador,
                    )
                    sg.Popup(
                        f"Palabra formada por el jugador: {palabra_formada(letras_jugador, posiciones_ocupadas)}\nPuntos sumadados: {puntos_jugada}",
                        title="Atención",
                        non_blocking=True,
                        auto_close_duration=5,
                        auto_close=True,
                    )
                    jugador.actualizar_puntaje(puntos_jugada)
                    letra_seleccionada = False
                    orientacion = [True, False]
                    primer_posicion = ultima_posicion = ()
                    posiciones_bloqueadas += [
                        posicion for posicion in posiciones_ocupadas
                    ]
                    if quedan_fichas(bolsa_de_fichas, len(posiciones_ocupadas)):
                        for posicion in posiciones_ocupadas:
                            letra = random.choice(fichas)
                            while bolsa_de_fichas[letra]["cantidad_fichas"] <= 0:
                                letra = random.choice(fichas)
                            letras_jugador[posiciones_ocupadas[posicion]] = letra
                            window.Element(posiciones_ocupadas[posicion]).Update(
                                letra, disabled=False, button_color=("white", "green")
                            )
                            bolsa_de_fichas[letra]["cantidad_fichas"] -= 1
                        posiciones_ocupadas = OrderedDict()
                        turno_jugador = False
                        primer_jugada = False
                    else:
                        for i in range(4):
                            jugador.actualizar_cambios_restantes()
                    window.Element("puntaje_jugador").Update(jugador.get_puntaje())
                # else:
                # print('palabra incorrecta')
            elif event in range(7):
                if letra_seleccionada:
                    window.Element(letra).Update(button_color=("white", "green"))
                window.Element(event).Update(button_color=("white", "red"))
                letra = event
                letra_seleccionada = True
            else:
                if letra_seleccionada:
                    if posicion_valida(
                        event, posiciones_ocupadas, orientacion, posiciones_bloqueadas
                    ):
                        if event in posiciones_ocupadas:
                            window.Element(posiciones_ocupadas[event]).Update(
                                button_color=("white", "green"), disabled=False
                            )
                        else:
                            ultima_posicion = event
                        window.Element(event).Update(
                            letras_jugador[letra], button_color=("white", "red")
                        )
                        posiciones[event] = letras_jugador[letra]
                        posiciones_ocupadas[event] = letra
                        window.Element(letra).Update(disabled=True)
                        letra_seleccionada = False
                        if len(posiciones_ocupadas) == 1:
                            primer_posicion = ultima_posicion = event
                else:
                    if event in (primer_posicion, ultima_posicion):
                        window.Element(event).Update(
                            casillas_especiales[event]["texto"]
                            if event in casillas_especiales
                            else " ",
                            button_color=casillas_especiales[event]["color"]
                            if event in casillas_especiales
                            else ("white", "green"),
                            disabled=False,
                        )
                        window.Element(posiciones_ocupadas[event]).Update(
                            button_color=("white", "green"), disabled=False
                        )
                        del posiciones_ocupadas[event]
                        del posiciones[event]
                        if len(posiciones_ocupadas) <= 1:
                            orientacion = [True, False]
                            if len(posiciones_ocupadas) == 0:
                                primer_posicion = ()
                                ultima_posicion = ()
                        if event == primer_posicion:
                            primer_posicion = (
                                (event[0] + 1, event[1])
                                if not orientacion[1]
                                else (event[0], event[1] + 1)
                            )
                        else:
                            ultima_posicion = (
                                (event[0] - 1, event[1])
                                if not orientacion[1]
                                else (event[0], event[1] - 1)
                            )
        if comenzar:
            if (
                contador == 0
                or computadora.get_cambios_restantes() < 0
                or jugador.get_cambios_restantes() < 0
            ):
                imprimir_mensaje_fin(jugador, computadora)
                break
            window.Element("tiempo").Update(datetime.timedelta(seconds=contador))
            contador -= 1
            window.Element("palabra_actual").Update(
                palabra_formada(letras_jugador, posiciones_ocupadas)
            )
            window.Element("cantidad_fichas").Update(fichas_totales(bolsa_de_fichas))
            fichas = "".join(
                [
                    letra * bolsa_de_fichas[letra]["cantidad_fichas"]
                    for letra in bolsa_de_fichas
                ]
            )

    window.Close()
    return partida, jugador, computadora
