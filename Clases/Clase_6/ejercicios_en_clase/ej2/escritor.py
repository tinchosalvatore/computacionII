import os
import time

fifo_path = 'canal_fifo'

with open(fifo_path, 'w') as fifo:
    for i in range(10):
        mensaje = f"MSG-{i}\n"
        print(f"[ESCRITOR] -> {mensaje.strip()}")
        fifo.write(mensaje)
        fifo.flush()
        time.sleep(0.5)
