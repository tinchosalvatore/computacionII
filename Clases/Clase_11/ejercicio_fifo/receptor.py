import os
import time
fifo_path = '/tmp/mi_fifo'


# Abre el FIFO para lectura
print("Leyendo el mensaje desde la FIFO con el receptor...")
time.sleep(3)  

with open(fifo_path, 'r') as fifo:
    mensaje = fifo.read()

print(f"El receptor recibió el mensaje: {mensaje}")
