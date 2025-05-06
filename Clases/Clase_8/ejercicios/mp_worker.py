from multiprocessing import Process, current_process
import time
"""
    Este script va a crear dos procesos que impriman su nombre y PID, esperando 1  y terminando
"""

# Definimos la funcion que va a hacer el trabajo
def worker():
    print(f"Worker {current_process().name} PID: {current_process().pid}")
    time.sleep(1)
    print(f"Worker {current_process().name} PID: {current_process().pid} finished")

if __name__ == "__main__":
    # Creamos dos procesos como Workers
    p1 = Process(target=worker, name="Worker 1")
    p2 = Process(target=worker, name="Worker 2")

    print("Starting workers")
    time.sleep(2)
    # Iniciamos los procesos
    p1.start()
    p2.start()

    # Esperamos a que terminen con join
    p1.join()
    p2.join()
    print("All workers finished")