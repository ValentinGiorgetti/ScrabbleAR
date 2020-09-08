"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo principal de la ventana de configuración.
"""


from componentes.ventanas.general import leer_evento
from componentes.ventanas.configuracion.funciones import (
    leer_ultima_configuracion, crear_ventana_configuracion, restablecer_configuracion, 
    confirmar_tiempo, confirmar_letra, confirmar_nick, 
    seleccionar_dificultad, seleccionar_dificultad, guardar_ultima_configuracion
)


def main():
    """
    Función que muestra una ventana donde el usuario puede modificar diferentes parámetros de la partida.
    
    El usuario puede configurar el nivel y tiempo de la partida, asi como también el puntaje y cantidad de 
    fichas de cada letra para todos los niveles. 

    Siempre se muestra la última configuración seleccionada, la cuál inicialmente coincide con la configuración 
    por defecto. El usuario tiene la posibilidad de reestablecer las configuraciones a valores por defecto. 
    
    Retorna:
        - configuracion_seleccionada (dict): diccionario que contiene la configuración seleccionada.
    """

    configuracion_seleccionada = leer_ultima_configuracion()

    ultimo_presionado = configuracion_seleccionada["nivel_seleccionado"].capitalize()

    window = crear_ventana_configuracion(ultimo_presionado, configuracion_seleccionada)

    while True:
        event, values, tiempo = leer_evento(window)
        if event in (None, " Aceptar "):
            break
        elif event == "restablecer":
            restablecer_configuracion(window, ultimo_presionado, configuracion_seleccionada)
        elif event == "confirmar_tiempo":
            confirmar_tiempo(values["tiempo"], configuracion_seleccionada, window)
        elif event == "confirmar_letra":
            confirmar_letra(values, configuracion_seleccionada, window)
        elif event == "confirmar_nick":
            confirmar_nick(values, configuracion_seleccionada, window)
        elif event in ("Fácil", "Medio", "Difícil"):
            ultimo_presionado = seleccionar_dificultad(configuracion_seleccionada, ultimo_presionado, event, window)

    window.Close()

    guardar_ultima_configuracion(configuracion_seleccionada)

    return configuracion_seleccionada