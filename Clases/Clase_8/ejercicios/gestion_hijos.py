from multiprocessing import Process
import time

def tarea():
    print("Inicia tarea...")
    time.sleep(5)
    print("Termina tarea.")

if __name__ == '__main__':
    p = Process(target=tarea)
    p.start()
    print(f"¿Sigue vivo?: {p.is_alive()}")  # Chequea si esta vivo el proceso, que si lo va a estar
    p.join()
    print(f"¿Sigue vivo después de join?: {p.is_alive()}")  # Despues de hacer join, ya no está vivo
