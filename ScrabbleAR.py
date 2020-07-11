from componentes.funciones.funciones_main import *
from componentes.tablero import jugar
from componentes.jugador import Jugador
import random, pickle, json, PySimpleGUI as sg
from os.path import join

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
        [sg.Text("ScrabbleAR")],
        [sg.Button("Imagen scrabble", disabled=True)],
        [sg.Button("Configuración", key=configuracion), sg.Button("Ver reglas del juego", key=reglas), sg.Button("Ver top de puntajes", key=top_puntajes)],
        [sg.Button("Reanudar partida", size=(7, 2), key="reanudar", disabled=partida == None,), sg.Button("Iniciar nueva partida", size=(11, 2), key=jugar)],
        [sg.Button("Salir")]
    ]
    ventana = sg.Window("ScrabbleAR", layout)

    layout_confirmar = [
        [sg.Text("Hay una partida guardada, si inicia una nueva no podrá continuar con la anterior")],
        [sg.Button("Cancelar"), sg.Button("Continuar")],
    ]
    window_confirmar = sg.Window("Partida nueva", layout_confirmar)

    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json")) as f:
        configuracion_seleccionada = json.load(f)

    with open(join("componentes", "informacion_guardada", "top_puntajes"), "rb") as f:
        top = pickle.load(f)

    ok = True

    while True:
        event = ventana.Read()[0]
        if event in (None, "Salir"):
            break
        ventana.Hide()
        if event == configuracion:
            temp = configuracion()
            if temp != {}:
                configuracion_seleccionada = temp
        elif event in (reglas, top_puntajes):
            event()
        elif event == jugar:
            if partida != None:
                window_confirmar.UnHide()
                opcion = window_confirmar.Read()[0]
                window_confirmar.Hide()
                ventana.UnHide()
                ok = opcion == "Continuar"
            if ok:
                ventana.Hide()
                partida, jugador, computadora = jugar(configuracion_seleccionada, None)
                actualizar_top(top, jugador, computadora)
                if configuracion_seleccionada["nivel"] == "dificil":
                    configuracion_seleccionada["palabra valida"] = random.choice(["adjetivos", "verbos"])
        elif event == "reanudar":
            partida, jugador, computadora = jugar(configuracion_seleccionada, partida)
            actualizar_top(top, jugador, computadora)
            if configuracion_seleccionada["nivel"] == "dificil":
                configuracion_seleccionada["palabra valida"] = random.choice(["adjetivos", "verbos"])
        ventana.UnHide()
        with open(join("componentes", "informacion_guardada", "partida_guardada"), "wb") as f:
            pickle.dump(partida, f)
        ventana.Element("reanudar").Update(disabled=partida == None)

    ventana.Close()

if __name__ == '__main__':
    main()
