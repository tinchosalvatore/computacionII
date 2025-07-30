import os

fifo_path = '/tmp/mi_fifo'

# Abrimos el FIFO en modo escritura
with open(fifo_path, 'w') as fifo:

    fifo.write("Hola desde el emisor!")