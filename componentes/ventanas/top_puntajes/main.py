"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo principal de la ventana de top de puntajes.
"""


from componentes.ventanas.general import leer_evento
from componentes.ventanas.top_puntajes.funciones import (
    leer_top, cargar_tabla, crear_ventana_tops, 
    resetear, mostrar_top
)


def main():
    """
    Función que muestra la ventana de top de puntajes.
    
    El usuario puede ver el top de todos los niveles y un top general (incluye todos los niveles).
    """
    
    ultimo_presionado = "general"
    
    top = leer_top()
        
    tabla = cargar_tabla()

    window = crear_ventana_tops(tabla["general"])
    
    while True:
      event = leer_evento(window)[0]
      if event in (None, "volver"):
        break
      elif event == "resetear":
        resetear(top, tabla, ultimo_presionado, window)
      else:
        ultimo_presionado = mostrar_top(ultimo_presionado, event, tabla[event], window)

    window.Close()