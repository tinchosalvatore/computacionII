import os
import time

fifo_path = 'canal_logs'

with open(fifo_path, 'w') as fifo:
    for i in range(3):
        mensaje = f"[SERVICIO B] Alerta crítica {i}\n"
        fifo.write(mensaje)
        fifo.flush()
        print(f"[SERVICIO B] Enviado")
        time.sleep(2)
