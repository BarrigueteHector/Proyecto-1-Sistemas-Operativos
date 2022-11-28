import threading
import time
import random

barrera = threading.Semaphore(5)
mutex = threading.Semaphore(1)

personas_mesa = 4
lista_turnos = []
cuenta = 0
id_crupier = 5

def jugador(id):
    mutex.acquire()
    lista_turnos.append(id)

    if len(lista_turnos) == 4:
        lista_turnos.append(5)

    print("Jugador", id, "\n")
    mutex.release()
    mesa(id)

def crupier():
    print("Crupier\n")
    mesa(id_crupier)

def mesa(id):
    global cuenta

    time.sleep(5)
    while True:
        for turno in lista_turnos:
            if turno == id:
                mutex.acquire()

                if id != 5:
                    print("Repartiendo cartas al jugador", id, "\n")
                else:
                    print("Repartiendo cartas al crupier\n")

                #if cuenta == 5:
                #    barrera.acquire(5)

                #barrera.release()
                mutex.release()

                time.sleep(2)
            else:
                #print("Esperando\n")
                time.sleep(5) #Antes 10
    
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