"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo principal de la ventana del tablero de juego.
"""


from componentes.ventanas.general import leer_evento
from componentes.ventanas.tablero.cambio_fichas.main import main as cambiar_fichas
from componentes.ventanas.tablero.logica.logica_computadora import jugar_computadora
from componentes.ventanas.tablero.logica.funciones import actualizar_tiempo, fichas_totales
from componentes.ventanas.tablero.logica.logica_jugador import seleccionar_ficha, colocar_ficha, confirmar_palabra
from componentes.ventanas.tablero.funciones import (
    inicializar_parametros, crear_ventana_tablero, 
    iniciar_partida, pausar, ventana_palabras_ingresadas, 
    posponer, finalizar_partida, pasar, confirmar_salir
)


def main(configuracion, partida_anterior):
    """
    Función donde se muestra el tablero de juego y se leen los diferentes eventos.

    Parámetros:
        - configuracion (dict): diccionario que contiene la configuración de la partida.
        - partida_anterior (dict): diccionario que contiene información de la partida anterior.

    Retorna:
        - partida_guardada (dict): diccionario con la partida jugada.
        - tablero["jugador"] (Jugador): instancia de la clase Jugador que representa al usuario.
        - tablero["computadora"] (Jugador): instancia de la clase Jugador que representa a la computadora.
    """

    tablero, parametros = inicializar_parametros(configuracion, partida_anterior)

    window = crear_ventana_tablero(tablero, parametros, partida_anterior)

    comenzar = partida_guardada = partida_finalizada = None

    while True:
        event, values, tiempo = leer_evento(window, 1000)
        if event == "Salir" and confirmar_salir(parametros["fin_juego"]):
            break
        elif event == "Iniciar":
            comenzar = iniciar_partida(window, parametros, partida_anterior)
        elif event == "Pausa":
            comenzar = pausar(window, comenzar)
        elif event == "palabras_ingresadas":
            ventana_palabras_ingresadas(window, tablero, parametros, comenzar)
        elif event == "Posponer":
            salir, partida_guardada = posponer(tablero, parametros["jugada"])
            if salir:
                break
        elif event == "Terminar":
            comenzar = finalizar_partida(window, tablero, parametros)
        elif comenzar:
            parametros["fin_juego"], tablero["contador"] = actualizar_tiempo(window, tablero["contador"], tiempo)
            if tablero["turno"] == "Computadora":
                jugar_computadora(window, parametros, tablero)
            elif tablero["turno"] == "Jugador":
                if event == "cambiar":
                    cambiar_fichas(window, tablero, parametros)
                elif event == "Pasar":
                    pasar(window, parametros, tablero)
                elif event == "confirmar":
                    confirmar_palabra(window, parametros, tablero)
                elif event in range(7):
                    seleccionar_ficha(window, parametros, event, tablero["jugador"].color)
                elif event:
                    colocar_ficha(window, parametros, tablero, event)
            if parametros["fin_juego"]:
                comenzar = finalizar_partida(window, tablero, parametros)
            window["cantidad_fichas"].Update(len(fichas_totales(tablero["bolsa_de_fichas"])))

    window.Close()

    return partida_guardada, tablero["jugador"], tablero["computadora"]