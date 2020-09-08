"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo que contiene parámetros usados para la creación de ventanas y una función para leer eventos.
"""


import time
from os.path import isfile, join
from playsound import playsound as reproducir


titulos = {"font" : ("Consolas", 12), 
           "background_color" : "#1d3557", 
           "justification" : "center"}
           
parametros_ventana = {"element_justification" : "center", 
                      "auto_size_text" : True, 
                      "auto_size_buttons" : True, 
                      "finalize" : True, 
                      "use_default_focus" : False, 
                      "text_justification" : "center"}

parametros_columna = {"justification" : "left", 
                      "element_justification" : "center"}

parametros_popup = {"title" : " Atención", 
                    "non_blocking" : True, 
                    "auto_close_duration" : 8, 
                    "auto_close" : True,
                    "custom_text" : (" Aceptar ", None)}
                    
cartel = {"title" : " Atención", "custom_text" : (" Aceptar ", None)}

colores = {"Fácil" : ("white", "green"), 
           "Medio" : ("white", "orange"), 
           "Difícil" : ("white", "red"),
           "General" : ("white", "blue")}
                    
                    
def leer_evento(window, tiempo = None, key = ""):
    """
    Función usada para leer un evento. 
    
    Reproduce un sonido en caso de haber leído un evento. En caso de 
    que no se encuentre el archivo de sonido no se reproducirá.
    
    Retorna el evento, valores y el tiempo transcurrido hasta que
    se leyó el evento.

    Parámetros:
        - window (sg.Window): ventana sobre la cuál se lee el evento.
        - tiempo (int): máximo tiempo a esperar.
        - key: evento a retornar si se llega al timeout.
        
    Retorna:
        - el evento leído.
        - (dict): los valores de los widgets de la ventana.
        - (int): tiempo transcurrido hasta que se leyó un evento.
    """
    
    inicio = time.time()
    
    event, values = window.Read(timeout = tiempo, timeout_key = key)

    ruta_sonido = join("componentes", "sonidos", "boton.mp3")
    
    if (event != key and isfile(ruta_sonido)):
        reproducir(ruta_sonido)
        
    return event, values, round(time.time() - inicio)
