from multiprocessing import Process, Queue
import time

def productor(q):
    for i in range(3):
        mensaje = f"Dato {i}"
        print(f"[Productor] Enviando: {mensaje}")
        q.put(mensaje)
        time.sleep(0.5)

def consumidor(q):
    time.sleep(1)
    while not q.empty():
        dato = q.get()
        print(f"[Consumidor] Recibido: {dato}")

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()