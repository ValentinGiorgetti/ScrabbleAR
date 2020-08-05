"""
Módulo principal de la ventana de configuración.
"""

from componentes.ventanas.configuracion.funciones import *
from componentes.ventanas.general import leer_evento


def main():
    """
    Función que muestra una ventana donde el usuario puede modificar diferentes parámetros de la partida.
    
    El usuario puede configurar el nivel y tiempo de la partida, asi como también el puntaje y cantidad de 
    fichas de cada letra para todos los niveles. 

    Siempre se muestra la última configuración seleccionada, la cuál inicialmente coincide con la configuración 
    por defecto. El usuario tiene la posibilidad de reestablecer las configuraciones a valores por defecto. 
    
    Retorna:
        - (dict): contiene la configuración seleccionada para la ventana principal.
    """

    configuracion_seleccionada = leer_ultima_configuracion()
    ultimo_presionado = configuracion_seleccionada['nivel'].capitalize()

    configuracion_predeterminada = leer_configuracion_predeterminada()
    
    colores = {'Fácil' : ("white", "green"), 'Medio' : ("white", "orange"), 'Difícil' : ('white', 'red')}
    
    window = crear_ventana_configuracion(colores, ultimo_presionado, informacion_letras(configuracion_seleccionada["fichas"]), configuracion_seleccionada)

    while True:
        event, values, tiempo = leer_evento(window)
        if event in (None, "Aceptar"):
            break
        elif event == "restablecer":
            ultimo_presionado, configuracion_seleccionada = restablecer_configuracion(window, configuracion_predeterminada, ultimo_presionado, colores)
        elif event == "confirmar_tiempo":
            confirmar_tiempo(values["tiempo"], configuracion_seleccionada, window)
        elif event == "confirmar_letra":
            confirmar_letra(values, configuracion_seleccionada, window)
        elif event == "confirmar_nick":	
            confirmar_nick(values, configuracion_seleccionada, window)
        elif event in ("Fácil", "Medio", "Difícil"):
            ultimo_presionado = seleccionar_dificultad(configuracion_seleccionada, ultimo_presionado, event, colores[event], window)

    window.Close()

    establecer_palabras_validas(configuracion_seleccionada)

    guardar_ultima_configuracion(configuracion_seleccionada)

    return configuracion_seleccionada