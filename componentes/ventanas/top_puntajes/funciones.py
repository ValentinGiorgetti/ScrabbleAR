"""
Módulo que contiene las funciones usadas por la ventana de top de puntajes.
"""


import pickle, PySimpleGUI as sg
from datetime import datetime
from componentes.jugador import Jugador
from componentes.ventanas.general import parametros_ventana, colores
from os.path import join


def crear_ventana_tops(tabla):
    """
    Función usada para crear la ventana del top de puntajes.

    Parámetros:
        - tabla (list): lista con el top de puntajes.

    Retorna:
        - (sg.Window): ventana del top de puntajes.
    """

    tamanio = (13, 1)

    layout = [
        [sg.Text("Top 10 de los mejores puntajes", size = (58,1), justification = 'center', background_color = '#1d3557')],
        [sg.Text('')],
        [sg.Button('General', key = 'general', button_color = ('white', 'blue'), size = tamanio), sg.Button('Nivel fácil', key = 'fácil', size = tamanio), sg.Button('Nivel medio', key = 'medio', size = tamanio), sg.Button('Nivel difícil', key = 'difícil', size = tamanio)],
        [sg.Text('')],
        [sg.Table(tabla, headings = ['Posición', 'Usuario', 'Puntaje', 'Fecha', 'Nivel'], justification = 'center', key = 'top', hide_vertical_scroll = True)],
        [sg.Text('')],
        [sg.Button('Resetear', key = 'resetear', disabled = tabla[0][1] == '', size = tamanio), sg.Button("Volver")],
    ]

    return sg.Window("  Top puntajes", layout, **parametros_ventana)
    

def leer_top():
    """
    Función que retorna el top de puntajes.

    Abre un archivo binario que contiene un diccionario con el top de cada nivel, en caso de que
    no exista se crea uno nuevo con los tops vacíos.

    -Retorna:
        - top (dict): un diccionario que contiene el top de puntajes de cada nivel.
    """
    
    try:
        with open(join("componentes", "informacion_guardada", "top_puntajes"), "rb") as f:
            top = pickle.load(f)
    except FileNotFoundError:
        sg.Popup('No se encontró el archivo con el top de puntajes, se reseteó el top de los niveles.', title = 'Atención')
        top = {i : [] for i in ['general', 'fácil', 'medio', 'difícil']}
        guardar_top(top)
            
    return top
    
    
def guardar_top(top):
    """
    Función usada para guardar el top de puntajes en un archivo binario.

    Parámetros:
        - top (dict): diccionario que contiene el top de puntajes de cada nivel.
    """

    with open(join("componentes", "informacion_guardada", "top_puntajes"), "wb") as f:
        pickle.dump(top, f)
        
        
def generar_tabla(top):
    """
    Función que genera la tabla para mostrar el top de puntajes del nivel correspondiente.
    
    Primero genera una tabla vacía y luego la completa con los valores del top.

    Parámetros:
        - top (list): lista con el top de puntajes de un nivel.

    Retorna:
        - tabla (list): lista con el top de puntajes para ser mostrados en un widget de tipo 'sg.Table'.
    """

    tabla = [[i, "", "", "", ""] for i in range(1, 11)]
    for i in range(len(top)):
      tabla[i] = [i + 1] + top[i]
      
    return tabla
    
    
def cargar_tabla():
    """
    Función que genera las 4 tablas del top.

    Retorna:
        - tabla (dict): diccionario que contiene el top de puntajes de cada nivel.
    """

    top = leer_top()
    tabla = {i : generar_tabla(top[i]) for i in ['general', 'fácil', 'medio', 'difícil']}
    
    return tabla
        
        
def resetear(top, tabla, nivel, ventana_tops):
    """
    Función usada para resetear el top de un nivel.
    
    Muestra un mensaje para que el usuario confirme la operación, luego actualiza
    el top y los widgets de la ventana.

    Parámetros:
        - top (dict): diccionario que contiene el top de puntajes por nivel.
        - tabla (dict): diccionario que contiene una tabla del top de puntajes por nivel.
        - nivel (str): el nivel de dificultad actual ('general', 'fácil', 'medio', 'difícil').
        - ventanta_tops (sg.Window): ventanta del top de puntajes.
    """

    aux = f'del nivel {nivel}' if nivel != 'general' else 'general'
    ok = sg.Popup('¿Está seguro de que quiere resetear el top ' + aux + '?', custom_text = ('Si', 'No'))
    if ok == 'Si':
        top[nivel] = []
        tabla[nivel] = generar_tabla(top[nivel])
        ventana_tops['top'].Update(values = tabla[nivel])
        ventana_tops['resetear'].Update(disabled = True)
        guardar_top(top)
    
  
def mostrar_top(ultimo_presionado, event, top, ventana_tops):
    """
    Función usada para mostrar el top de puntajes de un nivel determinado.

    Parámetros:
        - ultimo_presionado (str): el anterior nivel seleccionado.
        - event (str): el nuevo nivel seleccionado.
        - top (list): una lista con el top de puntajes para ser mostrados en un widget de tipo "sg.Table".
        - ventanta_tops (sg.Window): ventana del top de puntajes.

    Retorna:
        - event (str): nivel seleccionado.
    """
    colores['General'] = ('white', 'blue')

    ventana_tops[ultimo_presionado].Update(button_color = sg.DEFAULT_BUTTON_COLOR)
    ventana_tops[event].Update(button_color = colores[event.capitalize()])
    ventana_tops['top'].Update(values = top)
    ventana_tops['resetear'].Update(disabled = not top[0][1])

    return event
  

def actualizar_top(jugador, computadora, nivel):
    """
    Función usada para actualizar el top de los 10 mejores puntajes.

    Parámetros:
        - jugador (Jugador): objeto que representa al jugador.
        - computadora (Jugador): objeto que representa a la computadora.
        - nivel (str): nivel de dificultad.
    """
    
    fecha = datetime.now().strftime('%d/%m/%Y a las %H:%M')

    top = leer_top()

    jugador = [[jugador.nick, jugador.puntaje, fecha, nivel.capitalize()]] if jugador.puntaje > 0 else []
    computadora = [[computadora.nick, computadora.puntaje, fecha, nivel.capitalize()]] if computadora.puntaje > 0 else []
    
    temp = top['general'] + jugador + computadora
    top['general'] = sorted(temp, key=lambda x: x[1], reverse=True)[:10]
    
    temp = top[nivel] + jugador + computadora
    top[nivel] = sorted(temp, key=lambda x: x[1], reverse=True)[:10]

    guardar_top(top)
