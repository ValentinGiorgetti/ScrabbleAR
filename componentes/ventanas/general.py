"""
Módulo que contiene variables usadas por las ventanas y una función para
leer eventos.
"""

from os.path import join
from playsound import playsound as reproducir
import time

titulos = {'font' : ("Consolas", 11), 
           'background_color' : '#1d3557', 
           'size' : (55, 1), 
           'justification' : 'center'}
           
parametros_ventana = {'element_justification' : 'center', 
                      'auto_size_text' : True, 
                      'auto_size_buttons' : True, 
                      'finalize' : True, 
                      'use_default_focus' : False, 
                      'text_justification' : 'center', 
                      'disable_close' : True}

parametros_columna = {'justification' : 'left', 
                      'element_justification' : 'center'}

parametros_popup = {"title" : "Atención", 
                    "non_blocking" : True, 
                    "auto_close_duration" : 5, 
                    "auto_close" : True}
                    
def leer_evento(window, tiempo = None, key = ''):
    """
    Función usada para leer un evento. 
    
    Retorna el evento, valores y el tiempo transcurrido.
    """
    
    inicio = time.time()
    event, values = window.Read(timeout = tiempo, timeout_key = key)  
    if (event != key):
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        
    return event, values, round(time.time() - inicio)