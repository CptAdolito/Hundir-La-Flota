import colocacionBarcos
import juego
import tablero
import random

#Esta función está sacada de "calcular estado del tablero", pero con algunas modificaciones
def calcularEstadoIA(lista_barcos, lista_tocados): 
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
    
    #Dependiendo de en qué estado haya sido la última casilla tocada entramos en un estado o en otro
    if estadoCoordenadas[-1] == "T":
        estadoIA = 1
    elif estadoCoordenadas[-1] == "A":
        estadoIA = 0
    else:
        estadoIA = 3
    return estadoIA

def checkearSiHayGanador(barcos, tocados):
    ganador = False
    counter = 0
    for j in range(len(barcos)):
        for k in range(len(barcos[j])):
            if barcos[j][k] in tocados:
                counter += 1
    barcos_total = sum(len(row) for row in barcos)
    if barcos_total == counter:
        ganador = True
    return ganador

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

def jugarIA(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, EstadoIA):
    #Una vez tenemos la coordenada seleccionada la introducimos en los tocados
    #El estado 0 se ejecuta cuando el turno previo no se ha tocado un barco
    coordenadas = 0
    if EstadoIA[0] == "0":
        #Primero conseguimos unas coordenadas aleatorias a las que dar
        ok = False
        while not ok:
            coordenadas = [random.randint(0,16), random.randint(0,16)]
            if coordenadas not in tocadosJ1:
                tocadosJ1.append(coordenadas)
                ok = True
        #Ahora comprobamos si hemos tocado, hundido o nada
        estado = calcularEstadoIA(barcosJ1, tocadosJ1)
        if estado == 1:
            EstadoIA = ["1", [coordenadas], []]
    
    #El estado 1 se ejecuta cuando se está intentando hundir un barco
    elif EstadoIA[0] == "1" and coordenadas == 0:
        ultimaCoordenada = EstadoIA[1]
        coordenadaNoElegir = EstadoIA[2]
        #Elegimos hacia que lado ir
        ok = False
        #Creamos un contador que hace que si se bloquea vuelva al estado 0
        contador = 0
        while not ok:
            #Elegimos que coordenada usar
            coordenadaAelegir = random.randint(1, len(ultimaCoordenada))
            coordenadaElegida = ultimaCoordenada[coordenadaAelegir-1]

            #Elegimos si el barco se va a colocar en vertical u horizontal
            VoH = random.randint(1,2)
            #Elegimos si el barco se va a colocar en positivo o negativo
            if random.randint(1,2) == 1:
                coordenadas = [coordenadaElegida[0], coordenadaElegida[1]+1] if VoH == 1 else [coordenadaElegida[0]+1, coordenadaElegida[1]]
            else:
                coordenadas = [coordenadaElegida[0], coordenadaElegida[1]-1] if VoH == 1 else [coordenadaElegida[0]-1, coordenadaElegida[1]]
            #Ahora compruebo que la coodenada es posible
            if coordenadas not in tocadosJ1 and coordenadas not in coordenadaNoElegir:
                if 0<coordenadas[0]<17 and 0<coordenadas[1]<17:
                    tocadosJ1.append(coordenadas)
                    coordenadaNoElegir.append(coordenadas)
                    ok = True
            
            #Finalmente calculo su estado ahora
            estado = calcularEstadoIA(barcosJ1, tocadosJ1)
            if estado == 1:
                #Si se ha tocado ya tenemos la linea del barco
                if VoH == 2:
                    coordenadaNoElegir.append([coordenadaElegida[0], coordenadaElegida[1]-1])
                    coordenadaNoElegir.append([coordenadaElegida[0], coordenadaElegida[1]+1])
                else:
                    coordenadaNoElegir.append([coordenadaElegida[0]-1, coordenadaElegida[1]])
                    coordenadaNoElegir.append([coordenadaElegida[0]+1, coordenadaElegida[1]])
                ultimaCoordenada.append(coordenadas)
                EstadoIA = ["1", ultimaCoordenada, coordenadaNoElegir]
            elif estado == 3:
                EstadoIA = ["0", [], []]
            else:
                EstadoIA = ["1", ultimaCoordenada, coordenadaNoElegir]
            
            #Si el bucle hace 300 iteraciones digamos que se ha bloqueado asi que salimos del bucle y volvemos a fase 0
            if contador == 300:
                EstadoIA = ["0", [], []]
                ok = True
            contador+=1


    #Compruebo si el jugador 2 ha ganado ya
    ganador = 2 if checkearSiHayGanador(barcosJ1, tocadosJ1) else 0
    return tocadosJ1, tocadosJ2, ganador, EstadoIA


#Esta funcion es parecida a ejecutar partida normal pero se diferencia cuando es turno de la maquina
def ejecutarPartidaIA(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno):
    partidaConcluida = False
    salir = False
    EstadoIA = ["0", [], []]
    while not partidaConcluida:
        if turno == 1:
            juego.limpiar_pantalla()
            tocadosJ1, tocadosJ2, ganador, salir = jugar(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)
        else:
            tocadosJ1, tocadosJ2, ganador, EstadoIA = jugarIA(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, EstadoIA)
        partidaConcluida = True if ganador != 0 and ganador != 3 else False
        if not partidaConcluida and ganador != 3:
            turno = 1 if turno ==2 else 2
        if not partidaConcluida:
            partidaConcluida = True if salir else False
            #Pantalla de pausa
            if ganador == 3:
                juego.limpiar_pantalla()
                input("Jugador 1, presione cualquier tecla cuando esté listo.")
                juego.limpiar_pantalla()
    if not salir:
        juego.limpiar_pantalla()
        print("* ╔═══════════════════╗ *")
        print("* ║ GANA EL JUGADOR", turno, "║ *")
        print("* ╚═══════════════════╝ *")
        input("Presiona cualquier tecla para volver al menú: ")
        return 0, None, None, None, None, None
    else:
        return 0, barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno