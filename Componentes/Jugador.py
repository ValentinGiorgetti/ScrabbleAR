class Jugador:
  '''
  Clase Jugador con métodos para obtener y actualizar el puntaje
  y los cambios restantes del mismo.
  '''
  def __init__(self):
    self._puntaje = 0
    self._cambios_restantes = 3

  def get_puntaje(self):
    return self._puntaje

  def actualizar_puntaje(self, puntos):
    self._puntaje += puntos

  def get_cambios_restantes(self):
    return self._cambios_restantes

  def actualizar_cambios_restantes(self):
    self._cambios_restantes -= 1
