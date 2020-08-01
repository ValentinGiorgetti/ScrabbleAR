"""
Módulo que contiene las funciones utilizadas por la ventana principal.
"""


from componentes.ventanas.configuracion.main import main as configuracion
from componentes.ventanas.tablero.main import main as jugar
from componentes.ventanas.general import parametros_ventana
from componentes.ventanas.top_puntajes.funciones import actualizar_top
from os.path import join
import pickle, random, PySimpleGUI as sg


def crear_ventana_main(partida_guardada):
    """
    Función que crea la ventana principal.
    """
    
    tamanio = (25, 1)
    layout = [
        [sg.Text("")],
        [sg.Image(join('componentes', 'imagenes', 'logo.png'))],
        [sg.Text("")],
        [sg.Button("Configuración", size = tamanio, key= 'configuracion')],
        [sg.Button("Reglas del juego", size = tamanio, key= 'reglas')],
        [sg.Button("Top de puntajes", size = tamanio, key='top_puntajes')],
        [sg.Button("Reanudar partida", size = tamanio, key="reanudar", disabled= not partida_guardada)],
        [sg.Button("Nueva partida", size = tamanio, key='jugar')],
        [sg.Button("Salir", size = tamanio)],
        [sg.Text("")],
    ]
    return sg.Window("ScrabbleAR", layout, **parametros_ventana)
    
    
def leer_partida_guardada():
    """
    Función que retorna la partida guardada.
    """

    try:
        with open(join("componentes", "informacion_guardada", "partida_guardada"), "rb") as f:
            partida = pickle.load(f)
    except FileNotFoundError:
        sg.Popup('No se encontró el archivo con la última partida guardada.', title = 'Atención')
        partida = None
        guardar_partida(None)
        
    return partida
    
    
def guardar_partida(partida_guardada):
    """
    Función usada para guardar los datos de la partida.
    
    En caso de que la partida haya terminado se guardará None. Si la partida fue pospuesta, se
    guardará un diccionario con la información del tablero.
    """
    
    with open(join("componentes", "informacion_guardada", "partida_guardada"), "wb") as f:
        pickle.dump(partida_guardada, f)
    
    
def cargar_configuracion():
    """
    Función usada para que el usuario configure los parámetros de la partida.
    
    Abre la ventana de configuración y retorna un diccionario con la 
    configuracion seleccionada.
    """

    configuracion_temporal = configuracion()
    if configuracion_temporal:
        configuracion_seleccionada = configuracion_temporal
        
    return configuracion_seleccionada
    
    
def comenzar_juego(configuracion_seleccionada, partida_guardada, ventana_principal):
    """
    Función usada para iniciar una nueva partida. 
    
    En caso de que exista una partida guardada se pedirá una confirmación al usuario, ya
    que si inicia una nueva se borrará la anterior.
    
    Retorna None en caso de que la partida haya terminado o un diccionario con la información
    del tablero en caso de que la partida haya sido pospuesta.
    """

    opcion = 'Continuar'
    if partida_guardada:
        opcion = sg.Popup('Se encontró una partida guardada, si inicia una nueva no podrá continuar con la anterior', custom_text = ('Continuar', 'Cancelar')) 
    if opcion == "Continuar":
        ventana_principal.Hide()
        partida_guardada, jugador, computadora = jugar(configuracion_seleccionada, None)
        fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada)
        
    return partida_guardada
    
    
def reanudar_juego(configuracion_seleccionada, partida_guardada):
    """
    Función usada para reaundar una partida, en caso de que exista una partida guardada.
    
    Retorna None en caso de que la partida haya terminado o un diccionario con la información
    del tablero en caso de que la partida haya sido pospuesta.
    """
    partida_guardada, jugador, computadora = jugar(configuracion_seleccionada, partida_guardada)
    fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada)
    
    return partida_guardada
    
    
def fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada):
    """
    Función ejecutada al posponer o terminar una partida.
    
    Si la partida terminó se actualiza el top de puntajes y se elige aleatoriamente el 
    tipo de palabra válida para la próxima partida, en caso de que el nivel sea difícil.
    Si la partida fue pospuesta se guardará la información del tablero, si la partida
    terminó se guardará None.
    """

    if not partida_guardada:
      actualizar_top(jugador, computadora, configuracion_seleccionada["nivel"])
      if configuracion_seleccionada["nivel"] == "difícil":
        configuracion_seleccionada["palabras_validas"] = random.choice(["Adjetivos", "Verbos"])
    guardar_partida(partida_guardada)