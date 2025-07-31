"""
Implemente un contador compartido entre dos procesos usando Lock, para evitar la condicion de carrera
"""
from multiprocessing import Process, Lock, Value
import time


def contar(lock, contador):

    for i in range(10):
        with lock:
            contador.value += 1
            print(f"El contador esta en: {contador.value}")
        time.sleep(0.5)


def crear_procesos():
    lock = Lock()
    # Value permite que los procesos tengan un valor compartido, en este caso el contador
    contador = Value('i', 0)  # 'i' indica que es un entero con signo

    procesos = []

    for i in range(2):
        p = Process(target=contar, args=(lock, contador))
        
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()


    mensaje_final = f"Valor final del contador: {contador.value}"
    return mensaje_final


if __name__ == "__main__":
    mensaje = crear_procesos()
    print("Contador y procesos finalizados")
    print(mensaje)