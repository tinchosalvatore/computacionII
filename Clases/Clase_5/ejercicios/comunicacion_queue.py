"""
    Hay que recordar que esto anda gracias a que Queue funciona internamente con mecanismos de
    IPC con pipes o memoria compartida
    Y anda en sitemas UNIX solo si se define la Queue antes de hacer el fork()
"""

import os
from multiprocessing import Queue
import time

# Definicmos la funcino productor que va a tener como parametro de entrada a la Queue
# y va a enviar 5 mensajes a la Queue
def productor(q):
    for i in range(5):
        mensaje = f"Dato {i}"
        q.put(mensaje)      #q.put() lo que hace es agregar el parametro de entrada a la queue
        print(f"[Productor] Enviado: {mensaje}")
        time.sleep(0.5)
        

def consumidor(q):
    for _ in range(5):
        dato = q.get(timeout=5)  # q.get() obtiene los datos de la queue
                                # timeout = 5, Lanza excepción si pasan 5 segundos para evitar deadlock
        print(f"[Consumidor] Recibido: {dato}")
        time.sleep(0.5)

if __name__ == "__main__":
    q = Queue()         # Para que no hayan errores, solo en sistemas UNIX, definimos la Queue antes que el fork()
    pid = os.fork()
    
    if pid == 0:
        # Proceso hijo: consumidor      Consume y luego finaliza
        consumidor(q)
        os._exit(0)
    else:
        # Proceso padre: productor          Produce y espera a que el hijo termine
        productor(q)
        os.wait()
        print("[Main] Comunicación finalizada.")