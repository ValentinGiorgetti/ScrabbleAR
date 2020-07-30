import pickle, PySimpleGUI as sg
from datetime import datetime
from componentes.jugador import Jugador
from componentes.ventanas.general import parametros_ventana
from os.path import join

def crear_ventana_tops(tabla):

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

    return sg.Window("Top puntajes", layout, **parametros_ventana)
    

def leer_top():

    with open(join("componentes", "informacion_guardada", "top_puntajes"), "rb") as f:
        top = pickle.load(f)
        
    return top
    
    
def guardar_top(top):

    with open(join("componentes", "informacion_guardada", "top_puntajes"), "wb") as f:
        pickle.dump(top, f)
        
        
def generar_tabla(top):

  tabla = [[i, "", "", "", ""] for i in range(1, 11)]
  for i in range(len(top)):
    tabla[i][1] = top[i][0]
    tabla[i][2] = top[i][1]
    tabla[i][3] = top[i][2]
    tabla[i][4] = top[i][3]
  return tabla
        
        
def resetear(top, tabla, nivel, ventana_tops):

    aux = f'del nivel {nivel}' if nivel != 'general' else 'general'
    ok = sg.Popup('¿Está seguro de que quiere resetear el top ' + aux + '?', custom_text = ('Si', 'No'))
    if ok == 'Si':
        top[nivel] = []
        tabla[nivel] = generar_tabla(top[nivel])
        ventana_tops['top'].Update(values = tabla[nivel])
        ventana_tops['resetear'].Update(disabled = True)
        guardar_top(top)
        
        
def cargar_tabla():

    top = leer_top()
    tabla = {i : generar_tabla(top[i]) for i in ['general', 'fácil', 'medio', 'difícil']}
    return tabla
    
  
def mostrar_top(ultimo_presionado, event, color, top, ventana_tops):

  ventana_tops[ultimo_presionado].Update(button_color = sg.DEFAULT_BUTTON_COLOR)
  ventana_tops[event].Update(button_color = color)
  ventana_tops['top'].Update(values = top)
  ventana_tops['resetear'].Update(disabled = top[0][1] == '')
  
  return event
  

def actualizar_top(jugador, computadora, nivel):
    """
    Función usada para actualizar el top de los 10 mejores puntajes.
    """
    
    fecha = datetime.now().strftime('%d/%m/%Y a las %H:%M')

    top = leer_top()

    jugador = [("Jugador", jugador.puntaje, fecha, nivel.capitalize())] if jugador.puntaje > 0 else []
    computadora = [("Computadora", computadora.puntaje, fecha, nivel.capitalize())] if computadora.puntaje > 0 else []
    
    temp = top['general'] + jugador + computadora
    top['general'] = sorted(temp, key=lambda x: x[1], reverse=True)[:10]
    
    temp = top[nivel] + jugador + computadora
    top[nivel] = sorted(temp, key=lambda x: x[1], reverse=True)[:10]

    guardar_top(top)