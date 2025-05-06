from multiprocessing import Process
import os

# Tarea que el proceso hijo va a ejecutar
def tarea():
    print(f"Hola desde el proceso hijo. PID: {os.getpid()}")

if __name__ == '__main__':
    print(f"PID del proceso principal: {os.getpid()}")
    p = Process(target=tarea)   # target es un parametro que indica la función que el proceso hijo va a ejecutar
    p.start()  # inicia el proceso hijo
    p.join()   # espera a que el hijo termine
    print("El proceso hijo ha terminado.")
