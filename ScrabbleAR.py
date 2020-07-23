from componentes.funciones.funciones_main import *
from componentes.tablero import jugar
from componentes.jugador import Jugador
import random, pickle, json, PySimpleGUI as sg
from os.path import join
from playsound import playsound as reproducir 

def main():
    """
    Función principal que muestra una ventana con opciones para acceder al menú, reanundar una partida o iniciar una partida nueva.

    La opción de reanudar una partida sólo estará habilitada en caso de que exista una partida guardada. En caso de que exista una 
    partida guardada y el usuario quiera iniciar una nueva, se mostrará una ventana para confirmar la opción, ya que si se inicia una
    nueva partida, la partida guardada se elimina.

    La configuración de la partida será la última seleccionada.

    Una vez que la partida termina, se actualiza el top de puntajes y se guarda la información de la partida. En caso de que el usuario
    no haya pospuesto la partida, se guardará None en el archivo "partida_guardada", lo cuál indica que no hay partida guardada.
    
    (falta implementar manejo de excepciones para el caso en que se haya borrado algún archivo)
    """

    with open(join("componentes", "informacion_guardada", "partida_guardada"), "rb") as f:
        partida = pickle.load(f)

    layout = [
        [sg.Text("")],
        [sg.Image(join('componentes', 'imagenes', 'logo.png'))],
        [sg.Text("")],
        [sg.Button("Configuración", size = (25, 1), key=configuracion)],
        [sg.Button("Ver reglas del juego", size = (25, 1), key=reglas)],
        [sg.Button("Ver top de puntajes", size = (25, 1), key=top_puntajes)],
        [sg.Button("Reanudar partida", size = (25, 1), key="reanudar", disabled=partida == None,)],
        [sg.Button("Iniciar nueva partida", size = (25, 1), key=jugar)],
        [sg.Button("Salir", size = (25, 1))],
        [sg.Text("")],
    ]
    ventana = sg.Window("ScrabbleAR", layout, element_justification = 'center', auto_size_text=True, auto_size_buttons=True, finalize = True, use_default_focus = False, text_justification = 'center', disable_close = True)

    layout_confirmar = [
        [sg.Text("Hay una partida guardada, si inicia una nueva no podrá continuar con la anterior")],
        [sg.Button("Cancelar"), sg.Button("Continuar")],
    ]
    window_confirmar = sg.Window("Partida nueva", layout_confirmar, element_justification = 'center', auto_size_text=True, auto_size_buttons=True, finalize = True)
    window_confirmar.Hide()

    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json")) as f:
        configuracion_seleccionada = json.load(f)
        
    partida_pospuesta = False
    opcion = 'Continuar'

    while True:
        event = ventana.Read()[0]
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        if event in (None, "Salir"):
            break
        ventana.Hide()
        if event == configuracion:
            configuracion_temporal = configuracion()
            if configuracion_temporal:
                configuracion_seleccionada = configuracion_temporal
        elif event in (reglas, top_puntajes):
            event()
        elif event == jugar:
            if partida:
                window_confirmar.UnHide()
                opcion = window_confirmar.Read()[0]
                window_confirmar.Hide()
                ventana.UnHide()
            if opcion == "Continuar":
                ventana.Hide()
                partida, jugador, computadora, partida_pospuesta = jugar(configuracion_seleccionada, None)
                if not partida_pospuesta:
                  actualizar_top(jugador, computadora, configuracion_seleccionada["nivel"])
                if configuracion_seleccionada["nivel"] == "dificil":
                    configuracion_seleccionada["palabra valida"] = random.choice(["adjetivos", "verbos"])
        elif event == "reanudar":
            partida, jugador, computadora, partida_pospuesta = jugar(configuracion_seleccionada, partida)
            if not partida_pospuesta:
              actualizar_top(jugador, computadora, configuracion_seleccionada["nivel"])
            if configuracion_seleccionada["nivel"] == "dificil":
                configuracion_seleccionada["palabra valida"] = random.choice(["adjetivos", "verbos"])
        ventana.UnHide()
        if partida_pospuesta:
          with open(join("componentes", "informacion_guardada", "partida_guardada"), "wb") as f:
            pickle.dump(partida, f)
        ventana.Element("reanudar").Update(disabled=partida == None)

    ventana.Close()

if __name__ == '__main__':
    main()
