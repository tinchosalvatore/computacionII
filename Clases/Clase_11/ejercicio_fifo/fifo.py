"""
Cree un FIFO en /tmp/mi_fifo usando Bash (mkfifo). Luego:

    Escriba un script emisor.py que escriba mensajes en el FIFO.
    Escriba un script receptor.py que lea desde el FIFO e imprima los mensajes.

Ejecute ambos scripts en terminales distintas.

"""
import os


def crear_fifo():
    fifo_path = '/tmp/mi_fifo'      # /tmp es un directorio temporal en sistemas UNIX / LINUX

    # En caso de que no exista el FIFO, lo creamos
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)
        print(f"FIFO creado en {fifo_path}")
    else:
        print(f"La FIFO ya existe en {fifo_path}")


# Hago un proceso hijo que ejecute los scripts de escritura y lectura
def hijos():
    pid_emisor = os.fork()
    if pid_emisor == 0:
        os.execlp('python3', 'python3', 'emisor.py')
        
    pid_receptor = os.fork()
    if pid_receptor == 0:
        os.execlp('python3', 'python3', 'receptor.py')

    else:
        # Proceso padre: Espera a que el hijo termine
        os.waitpid(pid_emisor, 0)
        os.waitpid(pid_receptor, 0)
        print("Programa terminado")


if __name__ == "__main__":
    crear_fifo()
    hijos()