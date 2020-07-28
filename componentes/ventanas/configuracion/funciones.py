import json, random, PySimpleGUI as sg
from componentes.ventanas.parametros import titulos, parametros_columna, parametros_ventana, parametros_popup
from os.path import join

def crear_ventana_configuracion(colores, ultimo_presionado, tabla, configuracion_seleccionada):

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
    
    columna_configuracion = sg.Column(layout_configuracion, **parametros_columna)
    
    layout_configuracion_actual = [[sg.Text("Configuración actual", **titulos)],
        [sg.Text("")],
        [sg.Text("Nivel:", ), sg.Text(str(configuracion_seleccionada["nivel"] + '    '), key="nivel_seleccionado"),],
        [
            sg.Text("Tiempo:", ),
            sg.Text(str(configuracion_seleccionada["tiempo"]) + " minutos", key="tiempo_seleccionado", ),
        ],
        [sg.Text("")],
        [sg.Table(tabla, ['Letra', "Puntaje", "Cantidad fichas"], justification = 'center', key = "letras_modificadas")],
        [sg.Text("")],
        [sg.Button("Aceptar")]]
        
    columna_configuracion_actual = sg.Column(layout_configuracion_actual, **parametros_columna)
    
    window = sg.Window("Configuración", [[columna_configuracion, columna_configuracion_actual]], **parametros_ventana)
    
    window[ultimo_presionado].update(button_color = colores[configuracion_seleccionada['nivel'].capitalize()])
    
    return window
    
    
def leer_ultima_configuracion():

    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json"), encoding = 'UTF-8') as f:
        configuracion_seleccionada = json.load(f)
    
    return configuracion_seleccionada
    
    
def guardar_ultima_configuracion(configuracion):
    
    with open(join("componentes", "informacion_guardada", "ultima_configuracion.json"), 'w', encoding = 'UTF-8') as f:
        json.dump(configuracion, f, indent=2)
        
    
def leer_configuracion_predeterminada():

    with open(join("componentes", "informacion_guardada", "configuracion_predeterminada.json"), encoding = 'UTF-8') as f:
        configuracion_predeterminada = json.load(f)
    
    return configuracion_predeterminada 


def restablecer_configuracion(window, configuracion_predeterminada, ultimo_presionado, colores):

    configuracion_seleccionada = configuracion_predeterminada.copy()
    window["tiempo_seleccionado"].Update(str(configuracion_seleccionada["tiempo"]) + " minutos")
    window["letras_modificadas"].Update(informacion_letras(configuracion_seleccionada["fichas"]))
    window["nivel_seleccionado"].Update(configuracion_seleccionada["nivel"])
    window[ultimo_presionado].Update(button_color = sg.DEFAULT_BUTTON_COLOR)
    nivel = configuracion_seleccionada['nivel'].capitalize()
    window[nivel].Update(button_color = colores[nivel])
    return nivel, configuracion_seleccionada    
    
    
def confirmar_tiempo(tiempo, configuracion_seleccionada, ventana_configuracion):

    if tiempo == " ":
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
            
            
def informacion_letras(letras):
    """
    Función que es usada para actualizar un widget de la ventana el cuál muestra la información de las 
    fichas, de acuerdo a la configuración actual.
    """
    
    return [[letra, letras[letra]['puntaje'], letras[letra]['cantidad_fichas']] for letra in letras]
            
            
def confirmar_letra(values, configuracion_seleccionada, window):

    letra = values["letra"].upper()
    puntaje = values["puntaje"]
    cantidad_fichas = values["fichas"]
    if len(letra) > 1 or not letra.isalpha():
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
            window["letras_modificadas"].Update(informacion_letras(configuracion_seleccionada["fichas"]))
            
            
def seleccionar_dificultad(configuracion_seleccionada, ultimo_presionado, event, color, window):

    window[event].Update(button_color = color)
    if not ultimo_presionado in ("", event):
      window[ultimo_presionado].Update(button_color=sg.DEFAULT_BUTTON_COLOR)
    configuracion_seleccionada["nivel"] = event.lower()
    window["nivel_seleccionado"].Update(configuracion_seleccionada["nivel"])
    return event
    
    
    
def establecer_palabras_validas(configuracion_seleccionada):

    if configuracion_seleccionada["nivel"] == "difícil":
        configuracion_seleccionada["palabras_validas"] = random.choice(["adjetivos", "verbos"])
    else:
        configuracion_seleccionada["palabras_validas"] = "-"