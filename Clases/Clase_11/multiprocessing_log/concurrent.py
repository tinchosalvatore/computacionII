"""
Utilice multiprocessing.Process para crear 4 procesos que escriban su identificador y una marca de tiempo
en un mismo archivo de log. 

Utilice multiprocessing.Lock para evitar colisiones
"""
from multiprocessing import Process, Lock
import os
import time
import random


def tarea_proceso(lock, archivo_log):
    tiempo_random = random.randint(1, 10)

    mensaje = f"Soy el Proceso  {os.getpid()}, y tengo una timestamp aleatoria de {tiempo_random}\n"

    with lock:  # Aseguramos la zona critica para que solo un proceso escriba al mismo tiempo
        with open(archivo_log, "a") as f:  # a es de append, para no sobreescribir el titulo del log 
            f.write(mensaje)
            print(mensaje.strip())
            time.sleep(tiempo_random) #Simulamos trabajo con la timestamp


def crear_procesos():
    lock = Lock()
    archivo_log = "log.txt"

    with open(archivo_log, "w") as f:
        f.write("Inicio del log\n")

    procesos = []

    for _ in range(4):
        proceso = Process(target=tarea_proceso, args=(lock, archivo_log))
        procesos.append(proceso)  # Lo añadimos a la lista para despues hacer su join
        proceso.start()
        
    for proceso in procesos:
        proceso.join()  # Esperamos a que todos los procesos terminen, es como un os.wait()


if __name__ == "__main__":
    crear_procesos()
    print("Tareas terminadas!")
    print("log.txt actualizado")