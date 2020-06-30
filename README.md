# ScrabbleAR
ScrabbleAR - Seminario de Lenguajes (Python)

Consideraciones a tener en cuenta:

~ Versión de PySimpleGUI usada: 3.39.0

~ Versión de Pattern usada: 2.6

~ Versión de Python usada: 3.6.8

~ Para usar el programa se debe ejecutar el archivo "ScrabbleAR.py".

~ El usuario puede configurar distintos parámetros de la partida, tales como el nivel, tiempo límite, el puntaje y la cantidad de fichas de cada letra. Existe una configuración por defecto para que el usuario pueda iniciar una partida rápidamente. La última configuración elegida será guardada. 

~ El usuario tiene la posibilidad de posponer una partida, la cuál será guardada para poder continuarla en otra ocasión. En caso de que el usuario inicie una nueva partida, si había una partida guardada, esta será eliminada.

~ Para comenzar la partida, el usuario debe presionar el boton comenzar. En ese momento empezará a correr el contador. Puede pausar o posponer la partida en cualquier momento del juego.

~ Casillas especiales: 
  
  - Las casillas rotuladas "F +3" y "F +2" suman 3 o 2 puntos respectivamente, a la ficha colocada en esa posición.
  - Las casillas rotuladas "F -3", "F -2" y "F -1" restan 3, 2 o 1 punto respectivamente, a la ficha colocada en esa posición.
  - Las casillas rotuladas "P x3" y "P x2" multiplican por 2 o por 3 respectivamente, el puntaje de la palabra formada.
  - Los multiplicadores pueden acumularse, es decir, si la palabra ocupa una casilla "P x3" y una "P x2", se multiplicará por 5 el puntaje de la palabra formada.

~ El juego termina cuando el jugador presiona el botón de terminar, cuando la computadora no puede formar ninguna palabra y no tiene cambios disponibles, o cuando ya no se pueden repartir nuevas fichas ya que la bolsa de fichas no dispone de una cantidad suficiente.

~ En esta primer fecha nos centramos más en las funcionalidades del programa. Los aspectos estéticos los dejamos para más adelante, cuando tengamos bien todas las funcionalidades. La interfaz seguirá siendo similar, se cambiarán los colores / tamaños de diferentes widgets, fuentes de letras, se añadirán imágenes, etcétera.
