#!/usr/bin/env python3
#
# Copyright (c) Universidad Pontifica de Comillas (ICAI). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import sys
import menu
import colocacionBarcos
import partida
import guardarCargar
import random
import IAHandler

def limpiar_pantalla():
  
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

#Esta función maneja la partida
def ejecutarPartida(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno):
    partidaConcluida = False
    #Se repite cada turno hasta acabar
    while not partidaConcluida:
        #Esconde el tablero para que el jugador contrario no lo vea mientras cambian de sitio
        limpiar_pantalla()
        input(f"Jugador {turno}, presione cualquier tecla cuando esté listo.")
        limpiar_pantalla()
        tocadosJ1, tocadosJ2, ganador, salir = partida.jugar(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)
        partidaConcluida = True if ganador != 0 and ganador != 3 else False
        #Cambiamos de turno
        if not partidaConcluida and ganador != 3:
            turno = 1 if turno == 2 else 2
        if not partidaConcluida:
            partidaConcluida = True if salir else False
    #Si la partida acaba sin salir hay un ganador
    if not salir:
        limpiar_pantalla()
        print("* ╔═══════════════════╗ *")
        print("* ║ GANA EL JUGADOR", turno, "║ *")
        print("* ╚═══════════════════╝ *")
        input("Presiona cualquier tecla para volver al menú: ")
        return 0, None, None, None, None, None
    #Si la partida acaba saliendo devuelvo todas las variables para poder guardar el estado de la partida
    else:
        return 0, barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno

if __name__ == "__main__":
    modo = 0
    salir = color = False
    #Lo primero de todo es elegir si se va a jugar a color o en blanco y negro
    entrada = input("Escribe COLOR si quieres jugar con GRÁFICOS A COLOR.\nEscribe cualquier otra cosa si deseas jugar en modo BLANCO Y NEGRO\nEl modo a COLOR puede NO FUNCIONAR CORRECTAMENTE en todos los equipos\n")
    entrada = entrada.upper()
    entrada = entrada.split(" ")
    if entrada[0] == "COLOR":
        color = True

    while not salir:
        while modo == 0: #Si la entrada no es válida se vuelve a preguntar
            limpiar_pantalla()
            modo = menu.generarMenu(color)
        #-------------#
        #----SALIR----#
        #-------------#
        if modo == 4:
            limpiar_pantalla()
            salir = True

        #-------------#
        #----JUGAR----#
        #-------------#
        elif modo == 1: 
            ok = False
            while not ok:
                entrada = input("¿Deseas Jugar contra la máquina? (S/N): ")
                #Dependiendo de la respuesta elegiremos el modo manual o automático
                if entrada == "S" or entrada == "s" or entrada == "Y" or entrada == "y":
                    IA = True
                    ok = True
                    
                elif entrada == "N" or entrada == "n":
                    IA = False
                    ok = True
            
            #Para el modo manual ambos jugadores deben introducir sus barcos como deseen
            if not IA:
                turno = random.randint(1,2)
                tocadosJ1 = []
                tocadosJ2 = []
                #Primero cada jugador coloca sus barcos
                limpiar_pantalla()
                barcosJ1, numero = colocacionBarcos.colocarBarcos(1)
                limpiar_pantalla()
                barcos = list()
                for i in range(numero):
                    barcos.append([])
                #Ya hemos elegido el número de barcos previamente por lo que se lo pasamos al jugador 2 directamente
                barcosJ2, numero = colocacionBarcos.colocarBarcos(2, numero, barcos)
                #Ya podemos jugar
                modo, barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno = ejecutarPartida(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)
            
            #Al jugar contra la máquina solo el jugador debe introducir sus barcos
            else:
                turno = random.randint(1,2)
                tocadosJ1 = []
                tocadosJ2 = []
                #Primero cada jugador coloca sus barcos
                limpiar_pantalla()
                barcosJ1, numero = colocacionBarcos.colocarBarcos(1)
                limpiar_pantalla()
                barcos = list()
                for i in range(numero):
                    barcos.append([])
                #Ya hemos elegido el número de barcos previamente por lo que se lo pasamos al jugador 2 directamente
                barcosJ2 = colocacionBarcos.ElegirPosicionIA(numero)
                modo, barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno = IAHandler.ejecutarPartidaIA(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)

        #---------------#
        #----GUARDAR----#
        #---------------#
        elif modo == 2:
            try:
                guardarCargar.guardarPartida(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno, IA)
            except:
                input("Algo ha ido mal. Pulsa cualquier tecla para intentarlo de nuevo.")
            modo = 0
        #--------------#
        #----CARGAR----#
        #--------------#
        elif modo == 3: 
            try:
                barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno, IA = guardarCargar.cargarPartida()
                #Hay que rotar el turno antes de jugar
                turno = 1 if turno == 2 else 2
                if not IA:
                    modo, barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno = ejecutarPartida(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)
                else:
                    modo, barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno = IAHandler.ejecutarPartidaIA(barcosJ1, barcosJ2, tocadosJ1, tocadosJ2, turno)
            except:
                input("Algo ha ido mal. Pulsa cualquier tecla para intentarlo de nuevo.")
                modo = 0
        else:
            limpiar_pantalla()
            salir = True

    sys.exit(0)
    