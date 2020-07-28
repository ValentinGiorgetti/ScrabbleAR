from componentes.ventanas.configuracion.main import main as configuracion
from componentes.ventanas.tablero.main import main as jugar
from componentes.ventanas.parametros import parametros_ventana
from componentes.ventanas.top_puntajes.funciones import actualizar_top
from os.path import join
import random
import pickle
import PySimpleGUI as sg

def crear_ventana_main(partida_guardada):

    layout = [
        [sg.Text("")],
        [sg.Image(join('componentes', 'imagenes', 'logo.png'))],
        [sg.Text("")],
        [sg.Button("Configuración", size = (25, 1), key= 'configuracion')],
        [sg.Button("Reglas del juego", size = (25, 1), key= 'reglas')],
        [sg.Button("Top de puntajes", size = (25, 1), key='top_puntajes')],
        [sg.Button("Reanudar partida", size = (25, 1), key="reanudar", disabled= not partida_guardada)],
        [sg.Button("Nueva partida", size = (25, 1), key='jugar')],
        [sg.Button("Salir", size = (25, 1))],
        [sg.Text("")],
    ]
    return sg.Window("ScrabbleAR", layout, **parametros_ventana)
    
    
def leer_partida_guardada():

    with open(join("componentes", "informacion_guardada", "partida_guardada"), "rb") as f:
        partida = pickle.load(f)
        
    return partida
    
    
def fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada):

    if not partida_guardada:
      actualizar_top(jugador, computadora, configuracion_seleccionada["nivel"])
    if configuracion_seleccionada["nivel"] == "difícil":
      configuracion_seleccionada["palabras_validas"] = random.choice(["adjetivos", "verbos"])
    guardar_partida(partida_guardada)
    
    
def cargar_configuracion():

    configuracion_temporal = configuracion()
    if configuracion_temporal:
        configuracion_seleccionada = configuracion_temporal
        
    return configuracion_seleccionada
    
    
def comenzar_juego(configuracion_seleccionada, partida_guardada, ventana_principal):

    opcion = 'Continuar'
    if partida_guardada:
        opcion = sg.Popup('Se encontró una partida guardada, si inicia una nueva no podrá continuar con la anterior', custom_text = ('Continuar', 'Cancelar')) 
    if opcion == "Continuar":
        ventana_principal.Hide()
        partida_guardada, jugador, computadora = jugar(configuracion_seleccionada, None)
        fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada)
    return partida_guardada
    
    
def reanudar_juego(configuracion_seleccionada, partida_guardada):

    partida_guardada, jugador, computadora = jugar(configuracion_seleccionada, partida_guardada)
    fin_partida(jugador, computadora, configuracion_seleccionada, partida_guardada)
    return partida_guardada
    
    
def guardar_partida(partida_guardada):

    with open(join("componentes", "informacion_guardada", "partida_guardada"), "wb") as f:
        pickle.dump(partida_guardada, f)
