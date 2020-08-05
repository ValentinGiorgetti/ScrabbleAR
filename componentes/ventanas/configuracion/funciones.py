"""
Módulo que contiene las funciones usadas por la ventana de configuración.
"""


import json, random, PySimpleGUI as sg
from componentes.ventanas.general import titulos, parametros_columna, parametros_ventana, parametros_popup
from os.path import join


def crear_ventana_configuracion(colores, ultimo_presionado, tabla, configuracion_seleccionada):
    """
    Función usada para crear la ventana de configuración.

    Parámetros:
        - colores (dict): contiene los colores a utilizar para cada nivel de dificultad.
        - ultimo_presionado (str): último nivel de dificultad presionado (Fácil, Medio, Difícil).
        - tabla (list): contiene la información de las letras.
        - configuracion_seleccionada (dict): contiene la configuración seleccionada.

    Retorna:
        - (sg.Window): la ventana de configuración creada.
    """
    
    layout_configuracion = [
        [sg.Text("Nivel de la partida", **titulos)],
        [sg.Text("")],
        [
            sg.Button("Fácil"),
            sg.Button("Medio"),
            sg.Button("Difícil"),
        ],
        [sg.Text("")],
        [sg.Text("Tiempo de la partida", **titulos)],
        [sg.Text("")],
        [
            sg.Input(" ", size=(4, 2), key="tiempo"),
            sg.Text("minutos"),
            sg.Button("Confirmar", key="confirmar_tiempo"),
        ],
        [sg.Text("")],
        [
            sg.Text(
                "Configuración de las fichas para todos los niveles",
                **titulos
            )
        ],
        [sg.Text("")],
        [
            sg.Text("Letra"),
            sg.Input("", size=(4, 2), key="letra",),
            sg.Text("Puntaje"),
            sg.Input("", size=(4, 2), key="puntaje"),
            sg.Text("Cantidad de fichas"),
            sg.Input("", size=(4, 2), key="fichas"),
            sg.Button("Confirmar", key="confirmar_letra"),
        ],
        [sg.Text("")],
        [sg.Text("Nick del jugador", **titulos)],
        [sg.Text("")],
        [	
            sg.Input("", size = (10, 2), key="nick"),	
            sg.Button("Confirmar", key="confirmar_nick")	
        ],	
        [sg.Text("")],
        [sg.Button("Restablecer configuración", key="restablecer")],
    ]
    
    columna_configuracion = sg.Column(layout_configuracion, **parametros_columna)
    
    layout_configuracion_actual = [[sg.Text("Configuración actual", **titulos)],
        [sg.Text("")],
        [sg.Text("Nivel:", ), sg.Text(str(configuracion_seleccionada["nivel"]), key="nivel_seleccionado"),],
        [
            sg.Text("Tiempo:", ),
            sg.Text(str(configuracion_seleccionada["tiempo"]) + " minutos", key="tiempo_seleccionado", ),
        ],
        [sg.Text("Nick: "), sg.Text(configuracion_seleccionada["nick"], key="nick_seleccionado")],
        [sg.Text("")],
        [sg.Table(tabla, ['Letra', "Puntaje", "Cantidad fichas"], justification = 'center', key = "letras_modificadas")],
        [sg.Text("")],	
        [sg.Button("Aceptar")]	
    ]
        
    columna_configuracion_actual = sg.Column(layout_configuracion_actual, **parametros_columna)
    
    window = sg.Window("Configuración", [[columna_configuracion, columna_configuracion_actual]], **parametros_ventana)
    
    window[ultimo_presionado].update(button_color = colores[configuracion_seleccionada['nivel'].capitalize()])
    
    return window
    
    
def leer_ultima_configuracion():
    """
    Función que lee y retorna la última configuración seleccionada por el usuario.
    
    Abre un archivo json que contiene un diccionario con la configuración. Inicialmente 
    coincide con la configuración por defecto.

    Retorna:
        - (dict): la última configuración, o en caso de no existir, la configuración por defecto.
    """

    try:
        with open(join("componentes", "informacion_guardada", "ultima_configuracion.json"), encoding = 'UTF-8') as f:
            configuracion_seleccionada = json.load(f)
    except FileNotFoundError:
        sg.Popup('No se encontró el archivo con la última configuración seleccionada, se cargó la configuración por defecto.', title = 'Atención')
        configuracion_seleccionada = leer_configuracion_predeterminada()
    
    return configuracion_seleccionada
    
    
def guardar_ultima_configuracion(configuracion):
    """
    Función usada para guardar la configuración seleccionada.
    
    Guarda el diccionario con la configuración en formato json.

    Parámetros:
        - configuracion (dict): configuración a guardar.
    """
    
    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json"), 'w', encoding = 'UTF-8') as f:
        json.dump(configuracion, f, indent=2)
        
    
def leer_configuracion_predeterminada():
    """
    Función que lee y retorna la configuración predeterminada.
    
    Abre un archivo json que contiene un diccionario con la configuración predeterminada.

    Retorna:
        - (dict): la configuración por defecto.
    """
    
    ruta = join("componentes", "informacion_guardada", "configuracion_predeterminada.json")
    try:
        with open(ruta, encoding = 'UTF-8') as f:
            configuracion_predeterminada = json.load(f)
    except FileNotFoundError:
        configuracion_predeterminada = {"nivel": "fácil", "palabras_validas": "Adjetivos, sustantivos y verbos", "tiempo": 60}
        configuracion_predeterminada['fichas'] = {i : {"puntaje" : 1, "cantidad_fichas" : 15 if i in 'AEIOU' else 10} for i in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'}
        with open(ruta, 'w') as f:
            json.dump(configuracion_predeterminada, f, indent = 2)
    
    return configuracion_predeterminada 


def restablecer_configuracion(window, configuracion_predeterminada, ultimo_presionado, colores):
    """
    Función usada para restablecer la configuración.
    
    Actualiza la configuracion seleccionada y los widgets de la ventana con la configuración
    predeterminada.

    Parámetros:
        - window (sg.Window): ventana de configuración a actualizar.
        - configuracion_predeterminada (dict): configuración predeterminada.
        - ultimo_presionado (str): último nivel de dificultad presionado (Fácil, Medio, Difícil).
        - colores (dict): contiene los colores a utilizar para cada nivel de dificultad.

    Retorna:
        - (str): el nivel de dificultad nuevo (Fácil, Medio, Difícil).
        - (dict): la nueva configuración seleccionada, que es igual a la predeterminada.
    """

    configuracion_seleccionada = configuracion_predeterminada.copy()
    window["tiempo_seleccionado"].Update(str(configuracion_seleccionada["tiempo"]) + " minutos")
    window["letras_modificadas"].Update(informacion_letras(configuracion_seleccionada["fichas"]))
    window["nivel_seleccionado"].Update(configuracion_seleccionada["nivel"])
    window[ultimo_presionado].Update(button_color = sg.DEFAULT_BUTTON_COLOR)
    nivel = configuracion_seleccionada['nivel'].capitalize()
    window[nivel].Update(button_color = colores[nivel])
    window["nick_seleccionado"].Update(configuracion_seleccionada["nick"])
    return nivel, configuracion_seleccionada    
    
    
def confirmar_tiempo(tiempo, configuracion_seleccionada, ventana_configuracion):
    """
    Función usada para confirmar el tiempo de la partida ingresado por el usuario.
    
    Verifica que el valor ingresado sea válido.

    Parámetros:
        - tiempo (str): contiene el tiempo a verificar.
        - configuracion_seleccionada (dict): contiene la configuración seleccionada.
        - ventana_configuracion (sg.Window): la ventana de configuración.
    """

    if not tiempo:
        sg.Popup("El campo está vacío", **parametros_popup)
    else:
        try:
            tiempo = int(tiempo)
        except (ValueError):
            sg.Popup("No se ingresó un número válido", **parametros_popup)
        else:
            if tiempo >= 1:
              configuracion_seleccionada["tiempo"] = tiempo
            else:
              sg.Popup("Ingrese una cantidad de minutos válida", **parametros_popup)
            ventana_configuracion["tiempo_seleccionado"].Update(str(configuracion_seleccionada["tiempo"]) + " minutos")
            
            
def confirmar_letra(values, configuracion_seleccionada, window):
    """
    Función usada para confirmar la configuración de una letra.
    
    Verifica que los valores ingresados sean válidos. El usuario debe ingresar una letra y
    alguna configuración (puntaje y/o cantidad de fichas de la misma).

    Parámetros:
        - values (dict): contiene los valores de los widgets en el momento del evento.
        - configuracion_seleccionada (dict): contiene la configuración seleccionada.
        - window (sg.Window): la ventana de configuración.
    """

    letra = values["letra"].upper()
    puntaje = values["puntaje"]
    cantidad_fichas = values["fichas"]
    if len(letra) > 1 or not letra.isalpha():
      sg.Popup("Ingrese una letra válida", **parametros_popup)
    elif (not puntaje and not cantidad_fichas):
      sg.Popup("Los campos están vacíos", **parametros_popup)
    else:
        try:
            puntaje = int(puntaje) if puntaje else puntaje
            cantidad_fichas = int(cantidad_fichas) if cantidad_fichas else cantidad_fichas
        except (ValueError):
            sg.Popup("Los datos ingresados deben ser válidos", **parametros_popup)
        else:
            if puntaje:
              if puntaje >= 1:
                configuracion_seleccionada["fichas"][letra]["puntaje"] = puntaje
              else:
                sg.Popup("El puntaje debe ser mayor o igual a 1", **parametros_popup)
            if cantidad_fichas:
              if cantidad_fichas >= 1:
                configuracion_seleccionada["fichas"][letra]["cantidad_fichas"] = int(cantidad_fichas)
              else:
                sg.Popup("La cantidad de fichas debe ser mayor o igual a 1", **parametros_popup)
            window["letras_modificadas"].Update(informacion_letras(configuracion_seleccionada["fichas"]))
            
            
def confirmar_nick(values, configuracion_seleccionada, window):	
    """
    Función usada para confirmar el nick ingresado por el usuario.

    Parámetros:
        - values (dict): contiene los valores de los widgets en el momento del evento.
        - configuracion_seleccionada (dict): contiene la configuración seleccionada.
        - window (sg.Window): la ventana de configuración.
    """
    
    nick = values["nick"]
    if (not nick):
        sg.Popup('Ingrese un nick válido')
    else:
        configuracion_seleccionada["nick"] = nick	
        window["nick_seleccionado"].Update(nick)
            
            
def seleccionar_dificultad(configuracion_seleccionada, ultimo_presionado, event, color, window):
    """
    Función usada para seleccionar el nivel de dificultad de la partida.
    
    Actualiza los widgets de la ventana y la configuración seleccionada.

    Parámetros:
        - configuracion_seleccionada (dict): contiene la configuración seleccionada.
        - ultimo_presionado (str): anterior nivel de dificultad presionado (Fácil, Medio, Difícil).
        - event (str): nuevo nivel de dificultad presionado (Fácil, Medio, Difícil).
        - color (tuple): colores del botón del nivel presionado.
        - window (sg.Window): la ventana de configuración.

    Retorna:
        - (str): nuevo nivel de dificultad (Fácil, Medio, Difícil).
    """

    window[event].Update(button_color = color)
    if not ultimo_presionado in ("", event):
      window[ultimo_presionado].Update(button_color=sg.DEFAULT_BUTTON_COLOR)
    configuracion_seleccionada["nivel"] = event.lower()
    window["nivel_seleccionado"].Update(configuracion_seleccionada["nivel"])
    return event
    
    
def establecer_palabras_validas(configuracion_seleccionada):
    """
    Función usada para establecer las palabras válidas para el nivel seleccionado.

    Parámetros:
        - configuracion_seleccionada (dict): contiene la configuración seleccionada.
    """

    nivel = configuracion_seleccionada["nivel"]
    palabras_validas = {'fácil' : 'Adjetivos, sustantivos y verbos',
                        'medio' : 'Adjetivos y verbos',
                         'difícil' : random.choice(["Adjetivos", "Verbos"])}
    configuracion_seleccionada["palabras_validas"] = palabras_validas[nivel]
    
    
def informacion_letras(letras):
    """
    Función que retorna una lista con la información de las letras.

    Esta función es usada para actualizar la tabla que muestra la información de las fichas.
    La misma es actualizada a partir de la configuración seleccionada.
    
    Retorna una lista con las letras, el puntaje y la cantidad de fichas de las mismas.

    Parámetros:
        - letras (dict): contiene información de las fichas.

    Retorna:
        - (list): contiene la información de las fichas adaptadas para mostrar en un widget tipo 'sg.Table'.
    """
    
    return [[letra, letras[letra]['puntaje'], letras[letra]['cantidad_fichas']] for letra in letras]