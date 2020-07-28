import PySimpleGUI as sg
from playsound import playsound as reproducir
from os.path import join
from componentes.ventanas.configuracion.funciones import *

def main():
    """
    Función que muestra una ventana donde el usuario puede modificar diferentes parámetros de la partida,
    tales como el nivel, el tiempo, el puntaje y cantidad de fichas de cada letra. La configuración 
    consiste en un diccionario donde se van almacenando la configuración seleccionada.

    Siempre muestra la última configuración seleccionada, la cuál inicialmente coincide con la configuración 
    por defecto (la configuración por defecto se obtiene de un archivo json). El usuario tiene la posibilidad 
    de reestablecer las configuraciones a valores por defecto. Finalmente, se guarda la configuración seleccionada 
    en un archivo json y se retorna el diccionario con la configuración seleccionada a la ventana "menú".
    """

    configuracion_seleccionada = leer_ultima_configuracion()
    ultimo_presionado = configuracion_seleccionada['nivel'].capitalize()

    configuracion_predeterminada = leer_configuracion_predeterminada()
    
    colores = {'Fácil' : ("white", "green"), 'Medio' : ("white", "orange"), 'Difícil' : ('white', 'red')}
    
    window = crear_ventana_configuracion(colores, ultimo_presionado, informacion_letras(configuracion_seleccionada["fichas"]), configuracion_seleccionada)

    while True:
        event, values = window.Read()
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        if event in (None, "Aceptar"):
            break
        elif event == "restablecer":
            ultimo_presionado, configuracion_seleccionada = restablecer_configuracion(window, configuracion_predeterminada, ultimo_presionado, colores)
        elif event == "confirmar_tiempo":
            confirmar_tiempo(values["tiempo"], configuracion_seleccionada, window)
        elif event == "confirmar_letra":
            confirmar_letra(values, configuracion_seleccionada, window)
        elif event in ("Fácil", "Medio", "Difícil"):
            ultimo_presionado = seleccionar_dificultad(configuracion_seleccionada, ultimo_presionado, event, colores[event], window)

    window.Close()

    establecer_palabras_validas(configuracion_seleccionada)

    guardar_ultima_configuracion(configuracion_seleccionada)

    return configuracion_seleccionada