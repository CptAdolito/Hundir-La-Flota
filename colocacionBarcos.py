from juego import limpiar_pantalla
import tablero
import random
#Tuplas para los textos
NOMBRE_BARCOS = ("La patrullera", "La fragata", "El submarino", "El destructor", "El portaaviones","")
NOMBRE_BARCOS_SIN_ARTICULO = ("patrullera", "fragata", "submarino", "destructor", "portaaviones","")
LETRAS_ORDENADAS = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","")

def colocarBarcos(jugador, numero = 0, barcos = 0):
    if numero == 0:
        numero = NumeroBarcos()
    ok = False
    while not ok: #Esperamos a que se introduzca una entrada correcta
        limpiar_pantalla()
        print('Jugador', jugador)
        entrada = input("¿Deseas que tus barcos se coloquen automáticamente? (S/N): ")
        #Dependiendo de la respuesta elegiremos el modo manual o automático
        if entrada == "S" or entrada == "s" or entrada == "Y" or entrada == "y":
            ok = True
            barcos = ElegirPosicionAuto(numero, jugador)
        elif entrada == "N" or entrada == "n":
            ok = True
            barcos = ElegirPosicion(numero, jugador)
        
    return barcos, numero

#Esta función se utiliza para colocar de forma manual las coordenadas de los barcos
def ElegirPosicion(numero, jugador):
    limpiar_pantalla()
    superposicion = []

    #Cada barco es una lista con sus coordenadas que se guardará en una lista que contendrá a todos ellos
    barcos = list()
    for i in range(numero):
        barcos.append([])

    #Vamos a pedir las coordenadas mientras existan barcos
    k = 0
    while k < numero:
        tablero.imprimirJugador(jugador)
        tablero.generarTablero(barcos, [], [[0,0]], "", 1)
        posicionvalida = False
        superpuesto = False

        #Si la posición es válida se guardarán las coordenadas del barco, si no lo son se pedirán de nuevo
        while posicionvalida == False:
            try:
                #Gracias a las tuplas de antes podemos poner textos distintos para cada barco
                #Pedimos la posición inicial del barco
                print('Indica la primera posición ', "del " if k +1 > 2 else "de la ", NOMBRE_BARCOS_SIN_ARTICULO[k], " (", k + 2, " casillas)", sep='')
                entrada = input()
                entradaCorrecta, entradareal = conseguirCoordenada(entrada)
                i0 = int(entradareal[0])
                j0 = int(entradareal[1])
                l1 = j0
                l10 = i0

                #Pedimos la posición final del barco
                print('Indica última posición ', "del " if k +1 > 2 else "de la ", NOMBRE_BARCOS_SIN_ARTICULO[k], " (", k + 2, " casillas)", sep='')
                entrada = input()
                entradaCorrecta, entradareal = conseguirCoordenada(entrada)
                i = int(entradareal[0])
                j = int(entradareal[1])
                l2 = j
                l20 = i

                #Comprobamos que las coordenadas están dentro del tablero
                if (0<i<17 and 0<j<17) or (0<i0<17 and 0<j0<17):

                    #Barcos verticales
                    if (i == i0 and j != j0):
                        #Comprobamos que cumple la longitud del barco
                        if l2-l1 == k+1:
                            posicionvalida = True
                            #Como hemos introducido la coordenada inicial y final, este las iteraciones del bucle rellenarán el barco
                            for j in range(l1,l2+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])
                            #Llamamos a la función de superposición para ver si el barco está superponiendo a alguno anterior
                            superpuesto = BarcosSuperpuestos(superposicion)
                            #Si eso ocurre, vaciamos ese nuevo barco e indicamos que la posición no es válida para que se nos pidan de nuevo
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                            if superpuesto == True:
                                    print('Oh no, hay barcos superpuestos!')

                        #Hace exactamente los mismo que lo anterior pero está hecho por si se intruce la 'coordenada mayor' primero y
                        #por tanto la longitud saldría negativa y habría que rellenar las posiciones al revés
                        elif l2-l1 == -1*(k+1):
                            posicionvalida = True
                            for j in range(l2,l1+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])                                
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                            if superpuesto == True:
                                    print('Oh no, hay barcos superpuestos!')
                        else:
                            posicionvalida = False
                            print('Distancia no válida ',"(",k + 2," casillas)",sep='')

                    #Barcos horizontales, similar funcionamiento a los verticales
                    elif (i != i0 and j == j0):
                        if l20-l10 == k+1:
                            posicionvalida = True
                            for i in range(l10,l20+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                            if superpuesto == True:
                                print('Oh no, hay barcos superpuestos!')
                        elif l20-l10 == -1*(k+1):
                            posicionvalida = True
                            for i in range(l20,l10+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                            if superpuesto == True:
                                print('Oh no, hay barcos superpuestos!')
                        else:
                            posicionvalida = False
                            print('Distancia no válida ',"(",k + 2," casillas)",sep='')

                    #Solo podemos poner barcos verticales u horizontales, cualquier otro intento es incorrecto
                    else:
                        posicionvalida = False
                        print('No están en fila o columna')
                else:
                    posicionvalida = False
                    print('Pero pon números de las casillas')
            except:
                posicionvalida = False
                print('Capitán, no beba whiskey en el campo de batalla')

        limpiar_pantalla()
        tablero.imprimirJugador(jugador)
        tablero.generarTablero(barcos, [], [[0,0]], "", 1)
        ok = False
        while not ok:
            print(NOMBRE_BARCOS[k], 'está',  "colocado" if k +1 > 2 else "colocada" ,'correctamente')
            entrada = input("Capitán, ¿está usted conforme con esa ubicación? (S/N): ")
            if entrada == "S" or entrada == "s" or entrada == "Y" or entrada == "y":
                ok = True
            elif entrada == "N" or entrada == "n":
                #Si se desea repetir la colocación de algún barco limpiamos las variables y repetimos la iteracion del bucle
                ok = True
                for popear in range(k+2):
                    superposicion.pop()
                barcos[k].clear()
                k -= 1
        k+=1
        limpiar_pantalla()
    tablero.imprimirJugador(jugador)
    tablero.generarTablero(barcos, [], [[0,0]], "", 1)
    input("Este es su mapa final.")
    return barcos

#Esta función coloca los barcos automáticamente de forma aleatoria
#Funciona casi igual a la manual
def ElegirPosicionAuto(numero, jugador):

    superposicion = []

    barcos = list()
    for i in range(numero):
        barcos.append([])
    for k in range(numero):
        posicionvalida = False
        superpuesto = False
        while posicionvalida == False:
            try:
                #En vez de coordenadas introducidas por un input metemos una coordenada aleatoria
                x = random.randint(1,16)
                y = random.randint(1,16)
                
                i0 = l10 = x
                j0 = l1 = y
                
                #Elegimos si el barco se va a colocar en vertical u horizontal
                abajo = random.randint(1,2)
                #Elegimos si el barco se va a colocar en positivo o negativo
                if random.randint(1,2) == 1:
                    if abajo == 1:
                        l20 = i = (i0 + k+1)  
                    else:
                        l20 = i =(i0 - (k+1))
                    j = j0
                else:
                    if abajo == 1:
                        l2 = j = (j0 + k+1)  
                    else: 
                        l2 = j = (j0 - (k+1))
                    i = i0

                if (0<i<17 and 0<j<17):
                    if (i == i0 and j != j0):
                        if l2-l1 == k+1:
                            posicionvalida = True
                            for j in range(l1,l2+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])                                
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                        else:
                            posicionvalida = False
                    elif (i != i0 and j == j0):
                        if l20-l10 == k+1:
                            posicionvalida = True
                            for i in range(l10,l20+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                        else:
                            posicionvalida = False
                    else:
                        posicionvalida = False
                else:
                    posicionvalida = False
            except:
                posicionvalida = False
    tablero.imprimirJugador(jugador)
    tablero.generarTablero(barcos, [], [[0,0]], "", 1)
    ok = False
    while not ok:
        entrada = input("Capitán, este es su mapa final.\n¿Está usted conforme con estas posiciones? (S/N)")
        if entrada == "S" or entrada == "s" or entrada == "Y" or entrada == "y":
            ok = True
        elif entrada == "N" or entrada == "n":
            ok = True
            limpiar_pantalla()
            #Si se quiere volver a intentar se vuelve a ejecutar la función hasta que esté contento
            barcos = ElegirPosicionAuto(numero, jugador)
    
    return barcos
def ElegirPosicionIA(numero):
    superposicion = []
    barcos = list()
    for i in range(numero):
        barcos.append([])
    for k in range(numero):
        posicionvalida = False
        superpuesto = False
        while posicionvalida == False:
            try:
                #En vez de coordenadas introducidas por un input metemos una coordenada aleatoria
                x = random.randint(1,16)
                y = random.randint(1,16)
                
                i0 = l10 = x
                j0 = l1 = y
                
                #Elegimos si el barco se va a colocar en vertical u horizontal
                abajo = random.randint(1,2)
                #Elegimos si el barco se va a colocar en positivo o negativo
                if random.randint(1,2) == 1:
                    if abajo == 1:
                        l20 = i = (i0 + k+1)  
                    else:
                        l20 = i =(i0 - (k+1))
                    j = j0
                else:
                    if abajo == 1:
                        l2 = j = (j0 + k+1)  
                    else: 
                        l2 = j = (j0 - (k+1))
                    i = i0

                if (0<i<17 and 0<j<17):
                    if (i == i0 and j != j0):
                        if l2-l1 == k+1:
                            posicionvalida = True
                            for j in range(l1,l2+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])                                
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                        else:
                            posicionvalida = False
                    elif (i != i0 and j == j0):
                        if l20-l10 == k+1:
                            posicionvalida = True
                            for i in range(l10,l20+1):
                                superposicion.append([i,j])
                                barcos[k].append([i,j])
                            superpuesto = BarcosSuperpuestos(superposicion)
                            if superpuesto == True:
                                posicionvalida = False
                                for s in range(len(barcos[k])):
                                    superposicion.pop()
                                    barcos[k].pop()
                        else:
                            posicionvalida = False
                    else:
                        posicionvalida = False
                else:
                    posicionvalida = False
            except:
                posicionvalida = False
    return barcos

#Esta función comprobará que en la lista de posiciones de los barcos no haya ninguna que se repita, es decir, que no se superpongan barcos
def BarcosSuperpuestos(superposicion):
    repetido = []
    unico = []
    #Recorremos la lista y si esa coordenada no se encuentra en la lista 'único' la introduce
    #Pero si sí que está, la introduce la lista 'repetido'
    for x in superposicion:
        if x not in unico:
            unico.append(x)
        else:
            if x not in repetido:
                repetido.append(x)
    #Si hay algo dentro de la lista 'repetido' es que se están superponiendo barcos. Nos devolverá un True, si está vacía un False
    if len(repetido)>0:
        return True
    else:
        return False


#Esta función se utiliza al principio del programa para definir el número de barcos con los que queremos jugar y se guardará en una variable
def NumeroBarcos():
    numerocorrecto = False
    while numerocorrecto == False:
        print('¿Con cuántos barcos queréis jugar?')
        #Comprobamos que valor de entrada es válido (un número del 2 al 5) 
        try:
            numero = int(input())
            if numero > 1 and numero < 6:
                print("Has elegido ", numero, " barcos")
                numerocorrecto = True
            else:
                print('Número de barcos no válido. Introduzca un valor entre el 2 y el 5')
                numerocorrecto = False
            input('Pulsa cualquier tecla para comenzar')
        except:
            print("Capitán, introduzca un valor correcto entre el 2 y el 5")
    return numero


#Esta función se utiliza en todo el programa y recoge una entrada de la forma letra-número y la pasa a coordenadas del tablero
#También detecta la entrada "salir"
def conseguirCoordenada(entradaRaw):
    coordenadas = []
    entradaCorrecta = False
    #Primero probamos número-letra
    try:
        entrada = entradaRaw.split(" ")
        if len(entrada) == 1:
            #Separamos el string por números y letras
            if len(entrada[0]) == 2:
                entrada = [entrada[0][0], entrada[0][1]]
            else:
                entrada = [entrada[0][0], entrada[0][1] + entrada[0][2]]
        coordenadas.append(LETRAS_ORDENADAS.index(entrada[1].upper()) + 1) 
        coordenadas.append(int(entrada[0]))
        if coordenadas[0] > 0 and coordenadas[0] < 17 and coordenadas[1] > 0 and coordenadas[1] < 17: 
            entradaCorrecta = True
    except:
        #Segundo probamos letra-número
        try:
            entrada = entradaRaw.split(" ")
            if len(entrada) == 1:
                if len(entrada[0]) == 2:
                    entrada = [entrada[0][0], entrada[0][1]]
                else:
                    entrada = [entrada[0][0], entrada[0][1] + entrada[0][2]]
            coordenadas.append(LETRAS_ORDENADAS.index(entrada[0].upper()) + 1) 
            coordenadas.append(int(entrada[1]))
            if coordenadas[0] > 0 and coordenadas[0] < 17 and coordenadas[1] > 0 and coordenadas[1] < 17: 
                entradaCorrecta = True     
        except:
            #Si ninguna funciona probamos si ha escrito "salir" de cualquier forma
            try:
                entrada = entradaRaw.upper()
                entrada = entrada.split(" ")
                if entrada[0] == "SALIR":
                    entradaCorrecta = True
                    coordenadas = "salir"
                elif entrada[0] == "PAUSA":
                    entradaCorrecta = True
                    coordenadas = "pausa"
            except:
                entradaCorrecta = False
                coordenadas = []
    return entradaCorrecta, coordenadas




    