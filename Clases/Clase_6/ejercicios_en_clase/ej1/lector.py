import os

fifo_path = 'canal_fifo'

with open(fifo_path, 'r') as fifo:
    while True:
        mensaje = fifo.readline()
        if not mensaje:
            break
        print(f"[LECTOR] Recibido: {mensaje.strip()}")
