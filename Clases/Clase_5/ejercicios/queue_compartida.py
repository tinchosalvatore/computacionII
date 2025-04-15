import os
import time
from multiprocessing import Queue

# La funcion de los productores, como parametro tiene la queue obviamente, y el id del productor para diferenciarlos
def productor(q, id):
    for i in range(5):          # Cada productor produce 5 items
        item = f"P{id}-{i}"
        print(f"[Productor {id}] Produciendo: {item}")
        q.put(item)     # Se agrega el item a la queue
        time.sleep(0.3 + id * 0.1)  # Tiempos distintos por productor para evitar conflictos

# La funcion del consumidor
def consumidor(q, total_items):
    count = 0       # Contador de items consumidos empieza en 0 y aumenta por cada item consumido   

    while count < total_items:      # El while se rompe cuando se consumen todos los items
        if not q.empty():       #queue.empty() devuelve True si la queue esta vacia
            item = q.get()      # Se obtiene el item de la queue
            print(f"[Consumidor] Consumiendo: {item}")
            count += 1      # count aumenta una unidad por cada vez que se leyeron los datos
        else:
            print("[Consumidor] Esperando datos...")
            time.sleep(0.2)


if __name__ == "__main__":
    q = Queue()
    total_items = 10  # 5 items por productor

    # Primer fork - Productor 1
    pid1 = os.fork()
    if pid1 == 0:
        productor(q, 1)
        os._exit(0)

    # Segundo fork - Productor 2
    pid2 = os.fork()
    if pid2 == 0:
        productor(q, 2)
        os._exit(0)

    # Proceso padre actúa como consumidor
    consumidor(q, total_items)

    # Esperar a los hijos para evitar zombies
    os.wait()
    os.wait()
