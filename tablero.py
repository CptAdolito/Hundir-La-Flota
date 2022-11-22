#Unas cuantas constantes para dibujar el tablero
FILA_SEPARACION = "╠═══╣├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤"
FILA_SEPARACION_PRIMERA = "╔═══╗┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐"
FILA_SEPARACION_ULTIMA =  "╚═══╝└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘"
FILA_PRIMERA = "     ╔════╦════╦════╦════╦════╦════╦════╦════╦════╦════╦════╦════╦════╦════╦════╦════╗"
FILA_TERCERA = "     ╚════╩════╩════╩════╩════╩════╩════╩════╩════╩════╩════╩════╩════╩════╩════╩════╝"
TABLERO_AYUDA = [[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""]]

#Esta función maneja el tablero
def generarTablero(barcosJugador1, barcosJugador2, tocadosJ1, tocadosJ2, turno):
    #Primero calcula el estado del tablero del jugador 1
    tableroJ1 = calcularEstadoTablero(barcosJugador1, tocadosJ1, 1 if turno == 1 else 0)
    #Si se introducen datos del jugador 2 también calcula el estado del tablero del jugador 2
    #En el caso de la colocación de barcos no se introducen para que así sólo salga por pantalla un tablero y sea más cómodo
    if barcosJugador2 != []:
        imprimirJugadores(turno)
        tableroJ2 = calcularEstadoTablero(barcosJugador2, tocadosJ2, 1 if turno == 2 else 0)
    else: 
        tableroJ2 = TABLERO_AYUDA
    #Imprimimos el tablero según el turno, a la izquierda el jugador al que le toque jugar
    if turno == 1:
        imprimirTablero(tableroJ1, tableroJ2)
    else: 
        imprimirTablero(tableroJ2, tableroJ1)

#Esta función recibe la lista de barcos y de casillas tocadas y genera un tablero con los estados de cada casilla
def calcularEstadoTablero(lista_barcos, lista_tocados, turno):
    #Creamos listas para casillas de barcos tocados y hundidos
    barcosHundidos = list()
    barcosTocados = list()

    #Para cada casilla de barco la agrego a "hundidos", pero si no ha sido tocado añado el barco completo a "tocados"
    for i in range(len(lista_barcos)):
        for j in range(len(lista_barcos[i])):
            barcosHundidos += [lista_barcos[i][j]]
            if lista_barcos[i][j] not in lista_tocados:
                for k in range(len(lista_barcos[i])):
                    barcosTocados += [lista_barcos[i][k]]
    estadoCoordenadas = list()
    #Para cada casilla tocada
    for i in range(len(lista_tocados)):
        #Si está tocado coloco una "T", si está hundido pero no tocado una "H" y si no es ningún caso una "A"
        if lista_tocados[i] in barcosTocados:
            estadoCoordenadas += ["T"]
        elif lista_tocados[i] in barcosHundidos:
            estadoCoordenadas += ["H"]
        else:
            estadoCoordenadas += ["A"]
    
    #Más variables de ayuda para construir el tablero
    tablero = [["     ","║ 01 ║"," 02 ║"," 03 ║"," 04 ║"," 05 ║"," 06 ║"," 07 ║"," 08 ║"," 09 ║"," 10 ║"," 11 ║"," 12 ║"," 13 ║"," 14 ║"," 15 ║"," 16 ║"]]
    columnas = ["║ A ║","║ B ║","║ C ║","║ D ║","║ E ║","║ F ║","║ G ║","║ H ║","║ I ║","║ J ║","║ K ║","║ L ║","║ M ║","║ N ║","║ O ║","║ P ║",""]

    #Finalmente, contruimos el tablero por filas 
    for i in range(0, 17):
        tablero.append([columnas[i], "│"])
        if i > 0:
            for j in range(1,17):
                #Si esta coordenada ha sido tocada miramos en su estado y añadimos el símbolo que necesitemos
                if [i,j] in lista_tocados:
                    ubicacionCoordenada = lista_tocados.index([i,j])
                    if estadoCoordenadas[ubicacionCoordenada] == "T":
                        tablero[i].append(" ░░ │")
                    elif estadoCoordenadas[ubicacionCoordenada] == "H":
                        tablero[i].append(" ██ │")
                    else:
                        tablero[i].append(" ~~ │")
                #Si es tu propio tablero y no han tocado un barco lo pintamos con casillas distintas
                elif turno == 1:
                    if any([i,j] in k for k in lista_barcos):
                        tablero[i].append(" ¤¤ │")
                    else:
                        tablero[i].append("    │")
                else:
                    tablero[i].append("    │")
    return tablero

#Esta función imprime el tablero
#Si no se introduce un segundo tablero utilizamos el tablero vacío
def imprimirTablero(tablero1, tablero2=TABLERO_AYUDA):
    for i in range(len(tablero1) * 2):
        #Usamos las constantes auxiliares para decorar y las intercalamos con el tablero que hemos calculado 
        #Primero imprime las filas con los números de las coordenadas
        if i == 0:
            fila1 = FILA_PRIMERA
            fila2 = FILA_PRIMERA if tablero2 != TABLERO_AYUDA else str()
        elif i == 1:
            fila1 = "".join(str(j) for j in tablero1[0])
            fila2 = "".join(str(j) for j in tablero2[0])
        elif i == 2:
            fila1 = FILA_TERCERA
            fila2 = FILA_TERCERA if tablero2 != TABLERO_AYUDA else str()
        else:
            #Después alterna filas pares e impares para imprimir el contenido del tablero y su decoración
            if i % 2 == 0:
                fila1 = "".join(str(j) for j in tablero1[int(i/2) - 1])
                fila2 = "".join(str(j) for j in tablero2[int(i/2) - 1])
            else:
                if i == 3:
                    fila1 = FILA_SEPARACION_PRIMERA
                    fila2 = FILA_SEPARACION_PRIMERA if tablero2 != TABLERO_AYUDA else str()
                elif i == 35:
                    fila1 = FILA_SEPARACION_ULTIMA
                    fila2 = FILA_SEPARACION_ULTIMA if tablero2 != TABLERO_AYUDA else str()
                else:
                    fila1 = FILA_SEPARACION
                    fila2 = FILA_SEPARACION if tablero2 != TABLERO_AYUDA else str()
        fila = fila1 + "    " + fila2
        print(fila)

#Estas dos funciones imprimen el banner de los jugadores, uno solo si hay un solo tablero o los dos una vez empieza la partida
def imprimirJugador(jugador):
    print("                                    * ╔═══════════╗ *")
    print("                                    * ║ JUGADOR", jugador, "║ *")
    print("                                    * ╚═══════════╝ *")

def imprimirJugadores(turno):
    stringJ1 = "                                    * ║ JUGADOR 1 ║ *                                     "
    stringJ2 = "                                    * ║ JUGADOR 2 ║ *                                     "
    string = stringJ1 + stringJ2 if turno == 1 else stringJ2 + stringJ1
    print("                                    * ╔═══════════╗ *                                                                         * ╔═══════════╗ *")
    print(string)
    print("                                    * ╚═══════════╝ *                                                                         * ╚═══════════╝ *")