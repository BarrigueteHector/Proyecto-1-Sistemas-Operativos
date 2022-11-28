import threading
import time
import random

barrera = threading.Semaphore(5)
mutex = threading.Semaphore(1)

personas_mesa = 4
lista_turnos = []
cuenta = 0
id_crupier = 4

#104 CARTAS EN TOTAL
#id 0
cartas_corazon = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
#id 1
cartas_diamante = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
#id 2
cartas_trebol = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
#id 3
cartas_pica = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

puntaje = [0, 0, 0, 0, 0]
puntaje_crupier = 0
dinero = [0, 0, 0, 0]
apuesta = [0, 0, 0, 0, 0]

tipo = 0
numero = 0

pedir_carta = True
pedir_carta_crupier = True

carta_repetida = False

diferencia = 0
decision = 0

def jugador(id):
    mutex.acquire()
    lista_turnos.append(id)

    if len(lista_turnos) == 4:
        lista_turnos.append(id_crupier)

    #print("Jugador", id, "\n")
    mutex.release()
    mesa(id)

def crupier():
    #print("Crupier\n")
    mesa(id_crupier)

def mesa(id):
    global cuenta, puntaje, puntaje_crupier, dinero, apuesta
    puntaje[id] = 0
    apuesta[id] = 0
    pedir_carta = True
    pedir_carta_crupier = True
    carta_repetida = False

    time.sleep(5)
    while True:
        #print(lista_turnos)
        #time.sleep(10)

        for turno in lista_turnos:
            if turno == id:
                mutex.acquire()

                tipo = random.randrange(0, 4)
                numero = random.randrange(1, 11)

                #COMPROBANDO
                print(id != id_crupier and int(puntaje[id]) < 22 and pedir_carta)
                print(id == id_crupier and int(puntaje_crupier) < 22 and pedir_carta_crupier)
                    
                if (id != id_crupier and int(puntaje[id]) < 22 and pedir_carta) or (id == id_crupier and int(puntaje_crupier) < 22 and pedir_carta_crupier):
                    if(tipo == 0):
                        carta_repetida = repartiendo(numero, cartas_corazon, "CORAZONES")
                    elif(tipo == 1):
                        carta_repetida = repartiendo(numero, cartas_diamante, "DIAMANTES")
                    elif(tipo == 2):
                        carta_repetida = repartiendo(numero, cartas_trebol, "TREBOLES")
                    elif(tipo == 3):
                        carta_repetida = repartiendo(numero, cartas_pica, "PICAS")

                time.sleep(2)

                #COMPROBANDO
                print(id != id_crupier)

                if id != id_crupier:
                    if int(puntaje[id]) < 22 and pedir_carta:
                        #print("Repartiendo cartas al jugador", id, "\n")

                        if carta_repetida == False: #Si la carta no ha sido repetida
                            puntaje[id] += numero
                        
                        if (int(puntaje[id]) == 21):
                            pedir_carta = False
                        #elif(int(puntaje[id]) > 21):
                        #    break
                        else:
                            print("JUGADOR #" + str(id) + " Puntaje actual:", puntaje[id], "\n")
                            
                            if int(puntaje[id]) >= 11: #Puntaje mayor/igual a 11
                                pedir_carta = probabilidad(int(puntaje[id])) #¿Se pide otra carta?
                                
                    else:
                        print("-> JUGADOR #" + str(id) + " Puntaje final:", puntaje[id], "\n")

                else:
                    #print("Repartiendo cartas al crupier\n")

                    if int(puntaje_crupier) < 22 and pedir_carta_crupier: 
                        if carta_repetida == False:
                            puntaje_crupier += numero

                        if puntaje_crupier >= 17:
                            pedir_carta_crupier = False
                        
                        print("Crupier Puntaje actual:", puntaje_crupier, "\n")        
                    else:
                        print("-> Crupier Puntaje final:", puntaje_crupier, "\n")

                mutex.release()

                time.sleep(2)
            else:
                #print("Esperando\n")
                time.sleep(5) #Antes 10
    
def repartiendo(valor, lista_carta, str_carta):
    if (valor in lista_carta):
        lista_carta.remove(valor)
        print(valor, "DE", str_carta)
        return False
    else:
        #print("La carta", valor, "de", str_carta, "ya fue repartida\n")
        return True
        
def probabilidad(puntaje):
    diferencia = 21 - puntaje

    decision = random.randrange(1, 11) 

    if decision <= diferencia:
        print("Pide otra carta\n")
        return True
    else:
        print("Se planta\n")
        return False 

def main():
    for i in range(personas_mesa):
        threading.Thread(target=jugador, args=[i]).start()
    
    time.sleep(1)

    threading.Thread(target=crupier).start()
    
    # ****************** IDEA BASE PARA EL SISTEMA POR TURNOS ******************
    #turnos_lista = [1,2,3,4]
    #for turno in turnos_lista:
    #    if turno == 2:
    #        print("Iguales\n")
    #    else:
    #        print("Diferentes")

main()