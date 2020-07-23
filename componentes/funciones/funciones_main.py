import pickle, json, random, PySimpleGUI as sg
from os.path import join
from datetime import datetime
from playsound import playsound as reproducir

def reglas():
    """
    Función que muestra una ventana con información sobre cada nivel: tipo de palabras válidas
    y tamaño del tablero.
    """

    texto1 = (
        "Palabras válidas: cualquier palabra que la librería Pattern considere válida.\nTamaño del tablero: 19 x 19."
    )
    texto2 = "Palabras válidas: adjetivos y verbos.\nTamaño del tablero: 17 x 17."
    texto3 = "Palabras válidas: adjetivos o verbos, se selecciona en forma aleatoria.\nTamaño del tablero: 15 x 15."
    ultimo_presionado = ""
    colores = {'Fácil' : ("white", "green"), 'Medio' : ("white", "orange"), 'Difícil' : ('white', 'red')}

    layout = [
        [sg.Text("Reglas del juego", size=(60, 1), font=("Consolas", 11), justification = 'center')],
        [sg.Text('')],
        [sg.Button("Fácil"), sg.Button("Medio"), sg.Button("Difícil")],
        [sg.Text('')],
        [sg.Multiline("Seleccione un nivel", key="nivel", disabled=True, size = (60, 3))],
        [sg.Text('')],
        [sg.Button("Volver")],
    ]
    window = sg.Window("Reglas", layout, element_justification = 'center', auto_size_text=True, auto_size_buttons=True)

    while True:
        event = window.Read()[0]
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        if event in (None, "Volver"):
            break
        if ultimo_presionado != "":
            window.Element(ultimo_presionado).Update(button_color=sg.DEFAULT_BUTTON_COLOR)
        window.Element(event).Update(button_color=colores[event])
        ultimo_presionado = event
        window.Element("nivel").Update(texto1 if event == "Fácil" else (texto2 if event == "Medio" else texto3))
    window.Close()
    
def generar_tabla(top):
  tabla = [[i, "", "", ""] for i in range(1, 11)]
  for i in range(len(top)):
    tabla[i][1] = top[i][0]
    tabla[i][2] = top[i][1]
    tabla[i][3] = top[i][2]
  return tabla

def top_puntajes():
    """
    Función que muestra una ventana con el top 10 de los mejores puntajes.
    Abre un archivo binario que contiene una lista de tuplas ('Computadora / Jugador', Objeto jugador) ordenada
    por puntaje en forma descendente. Lo que hace es mostrar esa información en la ventana.
    """

    with open(join("componentes", "informacion_guardada", "top_puntajes"), "rb") as f:
        top = pickle.load(f)
    print('en top', top)
        
    param = {"headings" : ['Posición', 'Usuario', 'Puntaje', 'Fecha'], "justification" : 'center'}
    tabla = {i : generar_tabla(top[i]) for i in ['general', 'fácil', 'medio', 'difícil']}

    layout = [
        [sg.Text("Top 10 de los mejores puntajes", size = (40,1), justification = 'center')],
        [sg.Text('')],
        [sg.Button('Top general', key = 'general'), sg.Button('Top nivel fácil', key = 'fácil'), sg.Button('Top nivel medio', key = 'medio'), sg.Button('Top nivel difícil', key = 'difícil')],
        [sg.Text('')],
        [sg.Table(tabla['general'], **param, key = 'tabla', hide_vertical_scroll = True)],
        [sg.Text('')],
        [sg.Button("Volver")],
    ]

    window = sg.Window("Top puntajes", layout, element_justification = 'center', auto_size_text=True, auto_size_buttons=True)
    
    while True:
      event, values = window.Read()
      reproducir(join("componentes", "sonidos", "boton.mp3"))
      if event in (None, 'Volver'):
        break
      window['tabla'].Update(values = tabla[event], visible = True)
    window.Close()
    

def informacion_letras(letras):
    """
    Función que es usada para actualizar un widget de la ventana el cuál muestra la información de las 
    fichas, de acuerdo a la configuración actual.
    """
    
    return [[letra, letras[letra]['puntaje'], letras[letra]['cantidad_fichas']] for letra in letras]


def configuracion():
    """
    Función que muestra una ventana donde el usuario puede modificar diferentes parámetros de la partida,
    tales como el nivel, el tiempo, el puntaje y cantidad de fichas de cada letra. La configuración 
    consiste en un diccionario donde se van almacenando la configuración seleccionada.

    Siempre muestra la última configuración seleccionada, la cuál inicialmente coincide con la configuración 
    por defecto (la configuración por defecto se obtiene de un archivo json). El usuario tiene la posibilidad 
    de reestablecer las configuraciones a valores por defecto. Finalmente, se guarda la configuración seleccionada 
    en un archivo json y se retorna el diccionario con la configuración seleccionada a la ventana "menú".
    """

    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json"), encoding = 'UTF-8') as f:
        configuracion_seleccionada = json.load(f)

    with open(join("componentes", "informacion_guardada", "configuracion_predeterminada.json"), encoding = 'UTF-8') as f:
        configuracion_predeterminada = json.load(f)
        
    titulos = {'font' : ("Consolas", 11), 'background_color' : '#1d3557', 'size' : (55, 1), 'justification' : 'center'}
    
    colores = {'Fácil' : ("white", "green"), 'Medio' : ("white", "orange"), 'Difícil' : ('white', 'red')}

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
            sg.Input(" ", size=(4, 2), key="puntaje"),
            sg.Text("Cantidad de fichas"),
            sg.Input(" ", size=(4, 2), key="fichas"),
            sg.Button("Confirmar", key="confirmar_letra"),
        ],
        [sg.Text("")],
        [sg.Button("Restablecer configuración", key="restablecer")],
    ]
    
    parametros_columna = {'justification' : 'left', 'element_justification' : 'center'}
    
    columna_configuracion = sg.Column(layout_configuracion, **parametros_columna)
    
    layout_configuracion_actual = [[sg.Text("Configuración actual", **titulos)],
        [sg.Text("")],
        [sg.Text("Nivel:", ), sg.Text(str(configuracion_seleccionada["nivel"] + '    '), key="nivel_seleccionado"),],
        [
            sg.Text("Tiempo:", ),
            sg.Text(str(configuracion_seleccionada["tiempo"]) + " minutos", key="tiempo_seleccionado", ),
        ],
        [sg.Text("")],
        [sg.Table(informacion_letras(configuracion_seleccionada["fichas"]), ['Letra', "Puntaje", "Cantidad fichas"], justification = 'center', key = "letras_modificadas")],
        [sg.Text("")],
        [sg.Button("Aceptar")]]
        
    columna_configuracion_actual = sg.Column(layout_configuracion_actual, **parametros_columna)
    
    window = sg.Window("Configuración", [[columna_configuracion, columna_configuracion_actual]], element_justification = 'center', auto_size_text=True, auto_size_buttons=True, finalize = True)
    
    window[configuracion_seleccionada['nivel'].capitalize()].update(button_color = colores[configuracion_seleccionada['nivel'].capitalize()])
    
    parametros_popup = {"title" : "Atención", "non_blocking" : True, "auto_close_duration" : 5, "auto_close" : True}
    
    ultimo_presionado = configuracion_seleccionada['nivel'].capitalize()

    while True:
        event, values = window.Read()
        reproducir(join("componentes", "sonidos", "boton.mp3"))
        if event in (None, "Aceptar"):
            break
        if event == "restablecer":
            configuracion_seleccionada = configuracion_predeterminada.copy()
            window.Element("tiempo_seleccionado").Update(str(configuracion_seleccionada["tiempo"]) + " minutos")
            window.Element("letras_modificadas").Update(informacion_letras(configuracion_seleccionada["fichas"]))
            window.Element("nivel_seleccionado").Update(configuracion_seleccionada["nivel"])
        if event == "confirmar_tiempo":
            if values["tiempo"] == " ":
                sg.Popup("El campo está vacío", **parametros_popup)
            else:
                try:
                    tiempo = int(values["tiempo"])
                except (ValueError):
                    sg.Popup("No se ingresó un número válido", **parametros_popup)
                else:
                    if tiempo >= 1:
                      configuracion_seleccionada["tiempo"] = tiempo
                    else:
                      sg.Popup("Ingrese una cantidad de minutos válida", **parametros_popup)
                    window.Element("tiempo_seleccionado").Update(str(configuracion_seleccionada["tiempo"]) + " minutos")
        if event == "confirmar_letra":
            letra = values["letra"].upper()
            puntaje = values["puntaje"]
            cantidad_fichas = values["fichas"]
            if not letra.isalpha():
              sg.Popup("Ingrese una letra válida", **parametros_popup)
            elif (puntaje == " " and cantidad_fichas == " "):
              sg.Popup("Los campos están vacíos", **parametros_popup)
            else:
                try:
                    puntaje = int(puntaje) if puntaje != " " else puntaje
                    cantidad_fichas = int(cantidad_fichas) if cantidad_fichas != " " else cantidad_fichas
                except (ValueError):
                    sg.Popup("Los datos ingresados deben ser válidos", **parametros_popup)
                else:
                    if puntaje != " ":
                      if puntaje >= 1:
                        configuracion_seleccionada["fichas"][letra]["puntaje"] = puntaje
                      else:
                        sg.Popup("El puntaje debe ser mayor o igual a 1", **parametros_popup)
                    if cantidad_fichas != " ":
                      if cantidad_fichas >= 1:
                        configuracion_seleccionada["fichas"][letra]["cantidad_fichas"] = int(cantidad_fichas)
                      else:
                        sg.Popup("La cantidad de fichas debe ser mayor o igual a 1", **parametros_popup)
                    window.Element("letras_modificadas").Update(informacion_letras(configuracion_seleccionada["fichas"]))
        if event in ("Fácil", "Medio", "Difícil"):
            window[event].Update(button_color = colores[event])
            if ultimo_presionado != "":
              window.Element(ultimo_presionado).Update(button_color=sg.DEFAULT_BUTTON_COLOR)
            ultimo_presionado = event
            configuracion_seleccionada["nivel"] = event.lower()
            window.Element("nivel_seleccionado").Update(configuracion_seleccionada["nivel"])

    window.Close()

    if configuracion_seleccionada["nivel"] == "difícil":
        configuracion_seleccionada["palabras validas"] = random.choice(["adjetivos", "verbos"])
    else:
        configuracion_seleccionada["palabras validas"] = "-"

    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json"), "w", encoding = 'UTF-8') as f:
        json.dump(configuracion_seleccionada, f, indent=2)

    return configuracion_seleccionada


def actualizar_top(jugador, computadora, nivel):
    """
    Función usada para actualizar el top de los 10 mejores puntajes.
    """
    
    fecha = datetime.now().strftime('%d / %m / %Y')

    with open(join("componentes", "informacion_guardada", "top_puntajes"), "rb") as f:
        top = pickle.load(f)
        
        print('antes', top)

        jugador = [("Jugador", jugador.get_puntaje(), fecha)] if jugador.get_puntaje() > 0 else []
        computadora = [("Computadora", computadora.get_puntaje(), fecha)] if computadora.get_puntaje() > 0 else []
        
        temp = top['general'] + jugador + computadora
        top['general'] = sorted(temp, key=lambda x: x[1], reverse=True)[:10]
        
        temp = top[nivel] + jugador + computadora
        top[nivel] = sorted(temp, key=lambda x: x[1], reverse=True)[:10]
        
        print('despues', top)
    with open(join("componentes", "informacion_guardada", "top_puntajes"), "wb") as f:
        pickle.dump(top, f)
