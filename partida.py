import juego
import colocacionBarcos
import tablero

#Esta función se encarga de manejar un turno en la partida
def jugar(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno):
    entradaCorrecta = False
    salir = False
    #Esperamos a que se introduzca una entrada correcta
    while not entradaCorrecta:
        #Imprimimos el tablero en su estado actual para el jugador actual
        juego.limpiar_pantalla()
        tablero.generarTablero(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)
        print("Turno del jugador", turno)
        entrada = input("Mi capitán, ¿dónde deberíamos disparar?\nO escriba SALIR para regresar al menú o PAUSA para pausar: ")
        entradaCorrecta, coordenadas = colocacionBarcos.conseguirCoordenada(entrada)
    if coordenadas == "salir":
        salir = True
        ganador = False
    if coordenadas != "pausa":
        #Una vez tenemos la coordenada seleccionada la introducimos en los tocados
        if turno == 1 and salir == False:
            tocadosJ2.append(coordenadas)
            #Compruebo si el jugador 1 ha ganado ya
            ganador = 1 if checkearSiHayGanador(barcosJ2, tocadosJ2) else 0   
        elif salir == False: 
            tocadosJ1.append(coordenadas)
            #Compruebo si el jugador 2 ha ganado ya
            ganador = 2 if checkearSiHayGanador(barcosJ1, tocadosJ1) else 0
        return tocadosJ1, tocadosJ2, ganador, salir
    else:
        return tocadosJ1, tocadosJ2, 3, False


#Esta fución comrueba si hay un ganador
def checkearSiHayGanador(barcos, tocados):
    ganador = False
    counter = 0
    #Para cada barco del contrario, si has tocado una cordenada suma 1 al contador
    #Si el contador suma todas las posiciones de barcos hay ganador
    for j in range(len(barcos)):
        for k in range(len(barcos[j])):
            if barcos[j][k] in tocados:
                counter += 1
    barcos_total = sum(len(row) for row in barcos)
    if barcos_total == counter:
        ganador = True
    return ganador

