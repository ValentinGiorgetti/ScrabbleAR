# ScrabbleAR - Seminario de Lenguajes (Python)

#### Trabajo realizado por: Garea Antonella (17614/5), Garofalo Pedro (17136/5) y Giorgetti Valentín (17133/2).
#### Número del grupo: 31.

##### Consideraciones a tener en cuenta:

*~* Versión de PySimpleGUI usada: 4.26.0

*~* Versión de Pattern usada: 2.6

*~* Versión de Python usada: 3.6.8


*~* El módulo "playsound" necesita los siguientes paquetes para funcionar:
- En Ubuntu: "libcairo2-dev", "libgirepository1.0-dev" y "gir1.2-gtk-3.0".
Instalar con el comando: "sudo apt install libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0".
- En Arch Linux: "python-gobject".
Instalar con el comando: "sudo pacman -S python-gobject".

*~* Para usar el programa se debe ejecutar el archivo "ScrabbleAR.py".

*~* El usuario puede configurar distintos parámetros de la partida, tales como el nivel, tiempo límite, el puntaje y la cantidad de fichas de cada letra. Existe una configuración por defecto para que el usuario pueda iniciar una partida rápidamente. La última configuración elegida será guardada. 

*~* El usuario tiene la posibilidad de posponer una partida, la cuál será guardada para poder continuarla en otra ocasión. En caso de que el usuario inicie una nueva partida, si había una partida guardada, esta será eliminada.

*~* Para comenzar la partida, el usuario debe presionar el botón “Iniciar”. En ese momento empezará a correr el contador. Puede pausar o posponer la partida en cualquier momento del juego.

*~* Casillas especiales: 
  
  - Las casillas rotuladas "F x3" y "F x2" multiplican por 3 o por 2 respectivamente, el puntaje de la ficha colocada en esa posición.
  - Las casillas rotuladas "F -3", "F -2" y "F -1" restan 3, 2 o 1 punto respectivamente, a la ficha colocada en esa posición.
  - Las casillas rotuladas "P x3" y "P x2" multiplican por 2 o por 3 respectivamente, el puntaje de la palabra formada.
  - Los multiplicadores pueden acumularse, es decir, si la palabra ocupa una casilla "P x3" y una "P x2", se multiplicará por 5 el puntaje de la palabra formada.

*~* El juego termina cuando el jugador presiona el botón de terminar, cuando la computadora no puede formar ninguna palabra y no tiene cambios disponibles, cuando ya no se pueden repartir nuevas fichas ya que la bolsa de fichas no dispone de una cantidad suficiente, o cuando se acaba el tiempo límite de la partida.

*~* En esta primer fecha nos centramos más en las funcionalidades del programa. Los aspectos estéticos los dejamos para más adelante, cuando tengamos bien todas las funcionalidades. La interfaz seguirá siendo similar, se cambiarán los colores / tamaños de diferentes widgets, fuentes de letras, se añadirán imágenes, etcétera.

*~* Si la pantalla de la computadora es pequeña, no se podrá visualizar la ventana completa (estamos tratando de solucionar eso).
