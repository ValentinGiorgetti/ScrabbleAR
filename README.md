# ScrabbleAR - Seminario de Lenguajes (Python)

### Trabajo realizado por: Garea Antonella (17614/5), Garofalo Pedro (17136/5) y Giorgetti Valentín (17133/2).

### Número del grupo: 31.

#### Consideraciones a tener en cuenta

*~* Versión de Python usada: 3.6.8

*~* Versión de PySimpleGUI usada: 4.26.0

*~* Versión de Pattern usada: 3.6

*~* Versión de PlaySound usada: 1.2.2. Necesita los siguientes paquetes para funcionar:
- En Ubuntu: "libcairo2-dev", "libgirepository1.0-dev" y "gir1.2-gtk-3.0".
Instalar con el comando: "sudo apt install libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0".
- En Arch Linux: "python-gobject".
Instalar con el comando: "sudo pacman -S python-gobject".

*~* La imagen utilizada en el menú principal es propia. Los sonidos utilizados fueron buscados en la web "freesound.org" (Creative Commons Licensed).

*~* Para usar el programa se debe ejecutar el archivo "ScrabbleAR.py".

#### Introducción

El trabajo final de la materia “Seminario de Lenguajes” consiste en implementar el conocido juego “Scrabble” usando el lenguaje de programación Python, aplicando los conocimientos adquiridos durante la cursada de la materia.  

La versión implementada del juego tiene algunas diferencias respecto al original. El nombre elegido para la versión desarrollada es “ScrabbleAR”. Se juega contra la computadora y el jugador puede modificar varios parámetros de la partida.

Las palabras con las que se juegan son sustantivos, adjetivos y verbos. Para el análisis sintáctico de las palabras usadas en el juego se utilizó la librería Pattern, y para el diseño de la interfaz gráfica se usó PySimpleGUI. También se añadieron sonidos haciendo uso de la librería PlaySound.

El objetivo del juego es intentar ganar más puntos que la computadora, formando palabras sobre un tablero, tratando de aprovechar las casillas especiales ubicadas en el mismo.

#### Reglas del juego

Para comenzar la partida se deberá presionar el botón “Iniciar”. Esta acción hará que se elija en forma aleatoria, entre el jugador y la computadora, quien tendrá el primer turno.

Cada partida cuenta con una bolsa de fichas, en la cual se almacena una cierta cantidad de fichas de cada letra. 

Al comenzar la partida se reparten en forma aleatoria 7 (siete) fichas a cada participante. En todo momento, tanto el jugador como la computadora, deben disponer de esta cantidad de fichas en su atril que poseen para almacenarlas. Las fichas de la computadora no son visibles al jugador, de caso contrario, le otorgaría ventaja al mismo.

Las palabras colocadas en el tablero no deben cruzarse con otras palabras, sólo pueden situarse de izquierda a derecha (orientación horizontal) o de arriba hacia abajo (orientación vertical). Los tipos de palabras admitidas dependen del nivel seleccionado.

El jugador debe formar una palabra usando 2 (dos) o más fichas. En la primera jugada, una de ellas deberá estar situada en la casilla rotulada “Inicio”, la cual se encuentra en el centro del tablero. 

Una vez ingresada la palabra en el tablero, el jugador debe presionar el botón “Confirmar palabra” para verificar si la palabra es válida. En caso de que la palabra formada no sea válida, se le informará al jugador y el mismo podrá intentarlo nuevamente la cantidad de veces que desee. Si la palabra ingresada es válida, se informará en pantalla la palabra formada y los puntos obtenidos. Además, se repartirán aleatoriamente nuevas fichas al jugador, para reponer las utilizadas en la jugada, y luego se pasará el turno a la computadora.

Si el turno es de la computadora, tratará de formar una palabra válida con las fichas que dispone. En caso de no poder formar una palabra válida, se informará en pantalla, devolverá sus fichas a la bolsa y se le repartirán 7 (siete) nuevas en forma aleatoria. Luego se pasará el turno al jugador. Si la palabra ingresada es válida, se informará en pantalla la palabra formada y los puntos obtenidos. Luego, se repartirán aleatoriamente nuevas fichas a la computadora, para reponer las utilizadas en la jugada, y finalmente se pasará el turno al jugador.

En cualquier momento de la partida, el jugador puede presionar el botón “Cambiar fichas” para cambiar algunas o todas sus fichas, devolviéndolas a la bolsa y reemplazandolas por la misma cantidad. Si el jugador realizó algún cambio, se pasará el turno a la computadora. Tanto el jugador como la computadora pueden realizar un máximo de 3 (tres) cambios durante la partida.

#### Niveles del juego

• Nivel fácil: las palabras válidas son sustantivos, adjetivos y verbos. El tamaño del tablero es 19 x 19, tiene muchas casillas con premios y muy pocas con descuentos.

• Nivel medio: las palabras permitidas en este nivel son adjetivos y verbos. El tamaño del tablero es 17 x 17 y tiene más casillas con descuentos.

• Nivel difícil: en este nivel, el tipo de palabra permitida se selecciona aleatoriamente entre adjetivos y verbos. Es decir, durante la partida sólo se podrán formar adjetivos o verbos, dependiendo del resultado de la elección aleatoria para la misma. El tamaño del tablero es 15 x 15, hay algunas casillas con premios y muchas con descuentos.

#### Casillas especiales

• La casilla de inicio suma 1 punto a la palabra formada.

• Las casillas azules rotuladas "F x3" y "F x2" multiplican por 3 o por 2 respectivamente, el puntaje de la ficha colocada en esa posición.

• Las casillas negras rotuladas "F -3", "F -2" y "F -1" restan 3, 2 o 1 punto respectivamente, a la ficha colocada en esa posición.

• Las casillas violetas rotuladas "P x3" y "P x2" multiplican por 2 o por 3 respectivamente, el puntaje de la palabra formada. Los multiplicadores pueden acumularse, es decir, si la palabra ocupa una casilla "P x3" y una "P x2", se multiplicará por 5 el puntaje de la palabra formada.

En todo momento estará visible el puntaje del jugador y de la computadora. Para calcular el puntaje de una jugada se suma el puntaje de cada letra. Si la palabra está ubicada en una casilla especial, se aplicará el modificador correspondiente. El puntaje mínimo de una jugada es 0 (cero).  

#### Fin de la partida

La partida finaliza cuando ocurre alguna de las siguientes situaciones:

• El jugador presiona el botón “Terminar”.

• La computadora no puede formar ninguna palabra y no dispone de cambios suficientes para recibir nuevas fichas.

• No hay suficientes fichas en la bolsa para repartir a los jugadores.

• Se acaba el tiempo límite de la partida.

Una vez finalizada la partida, se revelan las fichas del atril de la computadora y al puntaje final de cada jugador se le resta el puntaje de las fichas que quedaron en sus atriles.

#### Algunas imágenes del juego

Menú principal

![](https://i.imgur.com/9a8o7Lf.png)

Ventana de configuración

![](https://i.imgur.com/rv9MwUL.png)

Ventana de reglas 

![](https://i.imgur.com/lE8jbf5.png)

Ventana del top de puntajes

![](https://i.imgur.com/PDdmMUa.png)

Ventana de juego

![](https://i.imgur.com/cmUni9G.png)