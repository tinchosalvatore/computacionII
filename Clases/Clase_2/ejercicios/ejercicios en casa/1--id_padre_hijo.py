# Crea un programa que genere un proceso hijo utilizando fork() y que ambos (padre e hijo) impriman sus respectivos PID y PPID.
#  El objetivo es observar la relación jerárquica entre ellos.

import os

pid = os.fork()     #Crea un hijo con fork()
if pid == 0:        #Si pid es 0, es el hijo
    print(f"Hijo PID: {os.getpid()}, PPID: {os.getppid()}")     #Imprime el PID y PPID del hijo
else:
    print(f"Padre PID: {os.getpid()}, PPID: {os.getppid()}")    #Imprime el PID y PPID del padre
    os.wait()       #Espera a que el hijo termine
    print("El hijo ha terminado")   #Imprime que el hijo ha terminado
    print("El padre ha terminado")  #Imprime que el padre ha terminado