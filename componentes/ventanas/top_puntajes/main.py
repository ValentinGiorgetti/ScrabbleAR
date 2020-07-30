from componentes.ventanas.top_puntajes.funciones import *
from componentes.ventanas.general import leer_evento

def main():
    """
    Función que muestra una ventana con el top 10 de los mejores puntajes.
    Abre un archivo binario que contiene una lista de tuplas ('Computadora / Jugador', Objeto jugador) ordenada
    por puntaje en forma descendente. Lo que hace es mostrar esa información en la ventana.
    """
    
    colores = {'general' : ('white', 'blue'), 'fácil' : ("white", "green"), 'medio' : ("white", "orange"), 'difícil' : ('white', 'red')}
    
    ultimo_presionado = 'general'
    
    top = leer_top()
        
    tabla = cargar_tabla()

    window = crear_ventana_tops(tabla['general'])
    
    while True:
      event, values = leer_evento(window)
      if event in (None, 'Volver'):
        break
      elif event == 'resetear':
        resetear(top, tabla, ultimo_presionado, window)
      else:
        ultimo_presionado = mostrar_top(ultimo_presionado, event, colores[event], tabla[event], window)
    window.Close()