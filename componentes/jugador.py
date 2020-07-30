class Jugador:
    """
    Clase Jugador con métodos para obtener y actualizar el puntaje
    y los cambios restantes del mismo.
    """

    def __init__(self, nombre, color_ficha):
        self._puntaje = 0
        self._cambios_restantes = 3
        self._fichas = []
        self._nombre = nombre
        self._color = color_ficha

    @property
    def puntaje(self):
        return self._puntaje

    @puntaje.setter
    def puntaje(self, puntaje):
        self._puntaje = puntaje
        if self._puntaje < 0:
            self._puntaje = 0
        
    @property
    def cambios_restantes(self):
        return self._cambios_restantes
    
    @cambios_restantes.setter
    def cambios_restantes(self, cambios):
        self._cambios_restantes = cambios
        
    @property
    def fichas(self):
        return self._fichas
        
    @fichas.setter
    def fichas(self, fichas):
        self._fichas = fichas
        
    @property
    def nombre(self):
        return self._nombre
        
    @property
    def color(self):
        return self._color
        
    def informacion(self):
        return [self._nombre, self._puntaje, self._cambios_restantes]