"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo que contiene las funciones utilizadas por la ventana principal.
"""


import pickle, PySimpleGUI as sg
from os.path import isfile, join
from componentes.ventanas.configuracion.main import main as configuracion
from componentes.ventanas.configuracion.funciones import establecer_palabras_validas
from componentes.ventanas.tablero.main import main as jugar
from componentes.ventanas.general import parametros_ventana, parametros_popup, cartel
from componentes.ventanas.top_puntajes.funciones import actualizar_top


def crear_ventana_main(partida_guardada):
    """
    Función que crea la ventana principal.
    
    En caso de que no se encuentre la imagen utilizada, se informará en pantalla.

    Parámetros:
        - partida_guardada (dict): diccionario con la información de la partida guardada.

    Retorna:
        - (sg.Window): ventana principal.
    """

    parametros = {"size": (25, 1), "font": ("None", 11)}
    ruta_imagen = join("componentes", "imagenes", "logo.png")
    
    if isfile(ruta_imagen):
        imagen = [sg.Image(join("componentes", "imagenes", "logo.png"))]
    else:
        imagen = []
        sg.Popup("No se encontró la imagen del menú principal\n", **cartel)
        
    layout = [
        [sg.Text("")],
        imagen,
        [sg.Text("")],
        [sg.Button("Configuración", key="configuracion", **parametros)],
        [sg.Button("Reglas del juego", key="reglas", **parametros)],
        [sg.Button("Top de puntajes", key="top_puntajes", **parametros)],
        [sg.Button("Reanudar partida", key="reanudar", disabled=not partida_guardada, **parametros)],
        [sg.Button("Nueva partida", key="jugar", **parametros)],
        [sg.Button("Salir", **parametros)],
        [sg.Text("")]
    ]

    return sg.Window(" ScrabbleAR", layout, **parametros_ventana)


def leer_partida_guardada():
    """
    Función que retorna la partida guardada.

    Retorna:
        - (dict): diccionario con la información de la partida guardada.
    """

    try:
        with open(join("componentes", "informacion_guardada", "partida_guardada"), "rb") as f:
            partida = pickle.load(f)
    except FileNotFoundError:
        sg.Popup("No se encontró el archivo con la última partida guardada\n", **cartel)
        partida = None
        guardar_partida(None)

    return partida


def guardar_partida(partida_guardada):
    """
    Función usada para guardar los datos de la partida.
    
    En caso de que la partida haya terminado se guardará None. Si la partida fue pospuesta, se
    guardará un diccionario con la información de la partida.

    Parámetros:
        - partida_guardada (dict): diccionario con la información de la partida a guardar.
    """

    with open(join("componentes", "informacion_guardada", "partida_guardada"), "wb") as f:
        pickle.dump(partida_guardada, f)


def comenzar_juego(configuracion_seleccionada, partida_guardada, ventana_principal):
    """
    Función usada para iniciar una nueva partida. 
    
    En caso de que exista una partida guardada se pedirá una confirmación al usuario, ya
    que si inicia una nueva se borrará la anterior.
    
    Retorna None en caso de que la partida haya terminado o un diccionario con la información
    de la partida en caso de que haya sido pospuesta.

    Parámetros:
        - configuracion_seleccionada (dict): diccionario con la configuración seleccionada.
        - partida_guardada (dict): diccionario con la información de la partida guardada.
        - ventana_principal (sg.Window): ventana principal.

    Retorna:
        - (dict): diccionario con información de la partida.
    """

    opcion = " Continuar "
    if partida_guardada:
        opcion = sg.Popup(
            "Se encontró una partida guardada, si inicia una nueva no podrá continuar con la anterior\n",
            custom_text=(" Continuar ", " Cancelar "),
            title=" Atención"
        )
    if opcion == " Continuar ":
        ventana_principal.Hide()
        partida_guardada, jugador, computadora = jugar(configuracion_seleccionada, None)
        fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada, ventana_principal)

    return partida_guardada


def reanudar_juego(configuracion_seleccionada, partida_guardada, ventana_principal):
    """
    Función usada para reaundar una partida, en caso de que exista una partida guardada.
    
    Retorna None en caso de que la partida haya terminado o un diccionario con la información
    del tablero en caso de que la partida haya sido pospuesta.

    Parámetros:
        - configuracion_seleccionada (dict): diccionario con la configuración seleccionada.
        - partida_guardada (dict): diccionario con la información de la partida guardada.
        - ventana_principal (sg.Window): ventana principal.

    Retorna:
        - (dict): diccionario con la partida jugada.
    """
    
    partida_guardada, jugador, computadora = jugar(configuracion_seleccionada, partida_guardada)
    fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada, ventana_principal)

    return partida_guardada


def fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada, ventana_principal):
    """
    Función ejecutada al posponer o terminar una partida.
    
    Si la partida terminó se actualiza el top de puntajes y se elige aleatoriamente el 
    tipo de palabra válida para la próxima partida, en caso de que el nivel sea difícil.
    Si la partida fue pospuesta se guardará la información del tablero, si la partida
    terminó se guardará None.

    Parámetros:
        - jugador (Jugador): instancia de Jugador que representa al usuario.
        - computadora (Jugador): instancia de Jugador que representa a la computadora.
        - configuracion_seleccionada (dict): diccionario con la configuración seleccionada.
        - partida_guardada (dict): diccionario con la información del tablero de la partida.
        - ventana_principal (sg.Window): ventana principal.
    """

    if not partida_guardada:
        actualizar_top(jugador, computadora, configuracion_seleccionada["nivel_seleccionado"])
        establecer_palabras_validas(configuracion_seleccionada)
    ventana_principal["reanudar"].Update(disabled=not partida_guardada)
    guardar_partida(partida_guardada)
