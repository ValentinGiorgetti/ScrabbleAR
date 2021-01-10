"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo principal del programa.
"""


from webbrowser import open
from componentes.ventanas.configuracion.funciones import leer_ultima_configuracion
from componentes.ventanas.reglas.main import main as reglas
from componentes.ventanas.top_puntajes.main import main as top_puntajes
from componentes.ventanas.general import leer_evento
from componentes.ventanas.configuracion.main import main as cargar_configuracion
from componentes.ventanas.funciones_main import crear_ventana_main, comenzar_juego, reanudar_juego, leer_partida_guardada


def main():
    """
    Función que muestra la ventana principal del programa.
    
    Muestra un menú con opciones para acceder a la ventana de configuración, reglas, top de
    puntajes, reanundar o iniciar una partida nueva.
    """

    partida_guardada = leer_partida_guardada()

    configuracion_seleccionada = leer_ultima_configuracion()

    ventana_principal = crear_ventana_main(partida_guardada)

    while True:
        event = leer_evento(ventana_principal)[0]
        if event in (None, "Salir"):
            break
        if event == "github":
           open("github.com/ValentinGiorgetti/ScrabbleAR")
           continue
        ventana_principal.Hide()
        if event == "reglas":
            reglas()
        elif event == "top_puntajes":
            top_puntajes()
        elif event == "configuracion":
            configuracion_seleccionada = cargar_configuracion()
        elif event == "jugar":
            partida_guardada = comenzar_juego(configuracion_seleccionada, partida_guardada, ventana_principal)
        elif event == "reanudar":
            partida_guardada = reanudar_juego(configuracion_seleccionada, partida_guardada, ventana_principal)
        ventana_principal.UnHide()

    ventana_principal.Close()

if __name__ == "__main__":
    main()
