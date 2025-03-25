# Diseña un programa donde se creen dos hijos de manera secuencial: se lanza el primero, se espera a que finalice, y luego se lanza el segundo.
# Cada hijo debe realizar una tarea mínima.

import os
import time

# definimos las tareas (sumas)
tarea_1= (2+2)
tarea_2= (3+3)

# creamos el primer hijo
pid = os.fork()
if pid == 0:
    print("Soy el hijo 1 con PID: ", os.getpid())       # impresion del PID del hijo 1
    print("Tarea 1: ", tarea_1)                    # ejecucion de la tarea 1
    time.sleep(3)                               # tiempo de espera
    print("Hijo 1 terminado")
else:
    os.wait()                                # espera a que el hijo 1 termine
    pid = os.fork()                     # creamos el segundo hijo
    if pid == 0:    
        print("Soy el hijo 2 con PID: ", os.getpid())       # impresion del PID del hijo 2
        print("Tarea 2: ", tarea_2)               # ejecucion de la tarea 2
        time.sleep(3)                    # tiempo de espera
        print("Hijo 2 terminado")
    else:
        os.wait()                 # espera a que el hijo 2 termine
        print("Soy el padre con PID: ", os.getpid())        # impresion del PID del padre
        print("Padre terminado")