"""
Módulo donde se define la clase Jugador.
"""


class Jugador:
    """
    Clase Jugador con métodos para obtener y actualizar el puntaje
    y los cambios restantes del mismo.
    """

    def __init__(self, nick, color_ficha):
        """
        Inicializa el objeto de tipo jugador.
        
        Parámetros:
            - nick (str): nombre del jugador.
            - color_ficha (tuple): color de las fichas del jugador.
        """
        self._puntaje = 0
        self._cambios_restantes = 3
        self._fichas = []
        self._nick = nick
        self._color = color_ficha

    @property
    def puntaje(self):
        """
        Devuelve el puntaje del jugador.
        
        Retorna:
            - (int): puntaje del jugador.
        """
        return self._puntaje

    @puntaje.setter
    def puntaje(self, puntaje):
        """
        Modifica el puntaje del jugador.
        
        Parámetros:
            - puntaje (int): puntaje del jugador.
        """
        self._puntaje = puntaje
        if self._puntaje < 0:
            self._puntaje = 0

    @property
    def cambios_restantes(self):
        """
        Devuelve la cantidad de cambios restantes del jugador.
        
        Retorna:
            - (int): cantidad de cambios restantes.
        """
        return self._cambios_restantes

    @cambios_restantes.setter
    def cambios_restantes(self, cambios):
        """
        Modifica la cantidad de cambios restantes del jugador.
        
        Parámetros:
            - cambios (int): cantidad de cambios restantes.
        """
        self._cambios_restantes = cambios

    @property
    def fichas(self):
        """
        Devuelve las fichas del jugador.
        
        Retorna:
            - (list): fichas del jugador.
        """
        return self._fichas

    @fichas.setter
    def fichas(self, fichas):
        """
        Modifica las fichas del jugador.
        
        Parámetros:
            - fichas (list): fichas del jugador.
        """
        self._fichas = fichas

    @property
    def nick(self):
        """
        Devuelve el nombre del jugador.
        
        Retorna:
            - (str): nombre del jugador.
        """
        return self._nick

    @property
    def color(self):
        """
        Devuelve el color de ficha del jugador.
        
        Retorna:
            - (tuple): color de ficha del jugador (fondo y letra).
        """
        return self._color

    def informacion(self):
        """
        Devuelve una lista con el nombre, el puntaje y la cantidad de cambios restantes del jugador.
        
        Retorna:
            - (list): lista con la información del jugador.
        """
        return [self._nick, self._puntaje, self._cambios_restantes]