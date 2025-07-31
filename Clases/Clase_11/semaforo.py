"""
Implemente una versión del problema de los "puestos limitados" usando multiprocessing.Semaphore

Cree 10 procesos que intenten acceder a una zona crítica que solo permite 3 accesos simultáneos
"""
from multiprocessing import Process, Semaphore, current_process
import time
import random

# Voy a simular que en la zona critica pueden estar 3 procesos a la vez

def zona_critica(sem):
    with sem:
        proceso = current_process()     # Esto es para debuggear el print con los nombres de los procesos
        print(f"Proceso {proceso.name} ha entrado en la zona crítica.")
        time.sleep(random.uniform(1, 3))  # Simulamos tarea
        print(f"Proceso {proceso.name} ha salido de la zona crítica.")


def main():
    sem = Semaphore(3)  # Argumentamos que solo 3 procesos pueden acceder
    procesos = [] 

    for i in range(10):
        p = Process(target=zona_critica, args=(sem,), name=f"Proceso {i+1}")
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()


if __name__ == "__main__":
    main()
    print("Todos los procesos han entrado y salido de la zona critica.")
    print("Fin del programa")