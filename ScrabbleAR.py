from componentes.ventanas.funciones_main import *
from componentes.ventanas.configuracion.funciones import leer_ultima_configuracion
from componentes.ventanas.reglas.main import main as reglas
from componentes.ventanas.top_puntajes.main import main as top_puntajes
import PySimpleGUI as sg
from os.path import join
from playsound import playsound as reproducir

def main():
    """
    Función principal que muestra una ventana_principal con opciones para acceder al menú, reanundar una partida o iniciar una partida nueva.

    La opción de reanudar una partida sólo estará habilitada en caso de que exista una partida guardada. En caso de que exista una 
    partida guardada y el usuario quiera iniciar una nueva, se mostrará una ventana_principal para confirmar la opción, ya que si se inicia una
    nueva partida, la partida guardada se elimina.

    La configuración de la partida será la última seleccionada.

    Una vez que la partida termina, se actualiza el top de puntajes y se guarda la información de la partida. En caso de que el usuario
    no haya pospuesto la partida, se guardará None en el archivo "partida_guardada", lo cuál indica que no hay partida guardada.
    
    (falta implementar manejo de excepciones para el caso en que se haya borrado algún archivo)
    """
    
    partida_guardada = leer_partida_guardada()
    
    configuracion_seleccionada = leer_ultima_configuracion()

    ventana_principal = crear_ventana_main(partida_guardada)

    while True:
        event = ventana_principal.Read()[0]
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        if event in (None, "Salir"):
            break
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
            partida_guardada = reanudar_juego(configuracion_seleccionada, partida_guardada)
        ventana_principal.UnHide()
        ventana_principal["reanudar"].Update(disabled= not partida_guardada)

    ventana_principal.Close()

if __name__ == '__main__':
    main()
