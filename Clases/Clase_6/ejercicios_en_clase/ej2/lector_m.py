import os
import sys

fifo_path = 'canal_fifo'
nombre = sys.argv[1]  # Para identificar al lector

with open(fifo_path, 'r') as fifo:
    while True:
        linea = fifo.readline()
        if not linea:
            break
        print(f"[{nombre}] Recibió: {linea.strip()}")
