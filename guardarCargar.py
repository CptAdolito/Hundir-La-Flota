import os

def guardarPartida(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno, IA):
    volverAPreguntar = True
    while volverAPreguntar:
        entrada = input("Selecciona una ubicación y un nombre para el archivo de la partida: ")
        try: #Primero intentamos limpiar la entrada por si hay espacios y separamos el tipo de archivo para ver si es de texto
            entradaSeparada = entrada.split(" ")
            if len(entradaSeparada) == 1 or len(entradaSeparada) == 2:
                #Probamos si hay uno o dos argumentos y los unimos todos en una sola ubicación
                if len(entradaSeparada) == 1:
                    nombreCompleto =  os.path.join(entradaSeparada[0]+".txt")
                else:
                    nombreCompleto =  os.path.join(entradaSeparada[0], entradaSeparada[1]+".txt")
                #Comprobamos que el archivo existe para no sobreescribirla
                if not os.path.exists(nombreCompleto):
                    with open(nombreCompleto, "w") as file:
                        #Metemos los barcos en un string con separadores distintivos para cada dimensión de la mtriz original, así logramos tenerlo en una sola linea
                        barcos1 = str()
                        barcos2 = str()
                        for i in range(len(barcosJ1)):
                            for j in range(len(barcosJ1[i])):
                                for k in range(len(barcosJ1[i][j])):
                                    barcos1 += str(barcosJ1[i][j][k]) + ","
                                    barcos2 += str(barcosJ2[i][j][k]) + ","
                                barcos1 += ";"
                                barcos2 += ";"
                            barcos1 += "."
                            barcos2 += "."

                        #Metemos los tocados en un string con separadores distintivos para cada dimensión
                        tocados1 = str()
                        tocados2 = str()
                        #Como la partida empieza aleatoriamente y puede que el primer jugador haya puesto un barco más que el segundo hay que hacer esta diferenciación
                        longitudAElegir = tocadosJ1 if max(len(tocadosJ1),len(tocadosJ2)) == len(tocadosJ1) else tocadosJ2
                        turnoAElegir = 1 if max(len(tocadosJ1),len(tocadosJ2)) == len(tocadosJ1) else 2

                        for i in range(len(longitudAElegir)):
                                for j in range(len(longitudAElegir[i])):
                                    tocados1 += str(tocadosJ1[i][j]) + ","
                                    if i != len(longitudAElegir) - 1 or turno == turnoAElegir:
                                        tocados2 += str(tocadosJ2[i][j]) + ","
                                tocados1 += "."
                                tocados2 += "."

                        #Como todas la variables ocupan una sola linea las escribimos en el archivo como tal, da igual su longitud
                        file.write(barcos1 + "\n")
                        file.write(barcos2+ "\n")
                        file.write(tocados1+ "\n")
                        file.write(tocados2+ "\n")
                        file.write(str(turno)+ "\n")
                        file.write(str(IA)+ "\n")
                    volverAPreguntar = False
                else:
                    print("Partida ya existente. Si deseas sobreescribirla elimina el archivo original.")
                    volverAPreguntar = True
            else:
                print("Introduzca un sólo archivo sin espacios.")
                volverAPreguntar = True
        except Exception as e:
            print(e)
            print("Nombre de archivo o ubicación no válidas.")
            volverAPreguntar = True

def cargarPartida():
    volverAPreguntar = True
    while volverAPreguntar:
        entrada = input("Selecciona una ubicación y el nombre de una partida guardada: ")
        try: #Primero intentamos limpiar la entrada por si hay espacios y separamos el tipo de archivo para ver si es de texto
            entradaSeparada = entrada.split(" ")
            if len(entradaSeparada) == 1 or len(entradaSeparada) == 2:
                #Creamos la ubicación real del archivo
                if len(entradaSeparada) == 1:
                    nombreCompleto =  os.path.join(entradaSeparada[0]+".txt")
                else:
                    nombreCompleto =  os.path.join(entradaSeparada[0], entradaSeparada[1]+".txt")
                with open(nombreCompleto, "r") as file:
                    lineas = file.readlines()
                    i = 0
                    #Cada variable es una linea
                    for linea in lineas:
                        if i == 0:
                            barcosJ1 = linea
                        elif i == 1:
                            barcosJ2 = linea
                        elif i == 2:
                            tocadosJ1 = linea
                        elif i == 3:
                            tocadosJ2 = linea
                        elif i == 4:
                            turno = linea
                        else:
                            IA = linea.strip()
                        i += 1
                volverAPreguntar = False
            else:
                print("Introduzca un sólo archivo sin espacios.")
                volverAPreguntar = True
        except:
            print("Archivo no encontrado")
            volverAPreguntar = True
        try:
            #Volvemos a meter los barcos en su correspondiente lista multidimensional
            #Usamos los separadores distintos que hemos usado en cada dimensión
            barcos1 = barcosJ1.split(".")
            barcos2 = barcosJ2.split(".")
            #Hay que eliminar los separadores que introducimos
            barcos1.pop(-1)
            barcos2.pop(-1)
            for i in range(len(barcos1)):
                barcos1[i] = barcos1[i].split(";")
                barcos2[i] = barcos2[i].split(";")
                barcos1[i].pop(-1)
                barcos2[i].pop(-1)
                for j in range(len(barcos1[i])):
                    barcos1[i][j] = barcos1[i][j].split(",")
                    barcos2[i][j] = barcos2[i][j].split(",")
                    barcos1[i][j].pop(-1)
                    barcos2[i][j].pop(-1)
                    for k in range(len(barcos1[i][j])):
                        barcos1[i][j][k] = int(barcos1[i][j][k]) 
                        barcos2[i][j][k] = int(barcos2[i][j][k])
            #Volvemos a meter los tocados en su correspondiente lista multidimensional
            tocados1 = tocadosJ1.split(".")
            tocados2 = tocadosJ2.split(".")
            tocados1.pop(-1)
            tocados2.pop(-1)
            for i in range(len(tocados1)):
                tocados1[i] = tocados1[i].split(",")
                tocados1[i].pop(-1)
                for j in range(2):
                    try:
                        tocados1[i][j] = int(tocados1[i][j])
                    except:
                        tocados1 = tocados1
            for i in range(len(tocados2)):
                tocados2[i] = tocados2[i].split(",")
                tocados2[i].pop(-1)
                for j in range(2):
                    try:
                        tocados2[i][j] = int(tocados2[i][j])
                    except:
                        tocados2 = tocados2
            #Metemos el turno en su variable como tipo int
            turno = int(turno)
            IA = True if IA == "True" else False
        except:
            print("Parece que el fichero está corrupto. Prueba con otro.")
            barcos1, barcos2, tocados1, tocados2, turno = cargarPartida()

    #Devolvemos todos los valores
    return barcos1, barcos2, tocados1, tocados2, turno, IA
        