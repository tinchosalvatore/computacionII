import os
import time

fifo_path = 'canal_logs'


with open(fifo_path, 'w') as fifo:
    for i in range(5):
        mensaje = f"[SERVICIO A] Evento número {i}\n"
        fifo.write(mensaje)
        fifo.flush()
        print(f"[SERVICIO A] Enviado")
        time.sleep(1)
