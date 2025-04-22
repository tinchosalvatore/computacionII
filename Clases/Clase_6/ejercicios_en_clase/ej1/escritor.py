import os
import time

fifo_path = 'canal_fifo'

with open(fifo_path, 'w') as fifo:
    for i in range(5):
        mensaje = f"Mensaje {i}\n"
        print(f"[ESCRITOR] Enviando: {mensaje.strip()}")
        fifo.write(mensaje)
        fifo.flush()
        time.sleep(1)
