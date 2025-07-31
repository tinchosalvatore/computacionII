"""
Implemente en Python un programa que cree 3 hijos que finalizan en distinto orden

El padre deberá recolectar manualmente cada estado usando os.waitpid, y registrar en qué orden terminaron
"""
import os
import time
import random

# Creamos 3 hijos con sleep times random
def hijos():
    
    for i in range(3):
        num_random = random.randint(1, 10)
        pid = os.fork()
        if pid == 0:
            print(f"Hijo {i + 1} con PID {os.getpid()} durmiendo {num_random} segundos")
            time.sleep(num_random)
            print(f"Hijo {i + 1} con PID {os.getpid()} ha terminado")
            os._exit(0)


def padre():
    hijos_pids = []
    
    for i in range(3):
        #LINEA CLAVE, -1 indica esperar a cualquier hijo, 0 indica que no se espera un estado específico
        pid, status = os.waitpid(-1, 0) 
        hijos_pids.append(pid)
        print(f"Padre ha recolectado el hijo con PID {pid} que terminó con estado {status}")

    print("Todos los hijos han terminado.")
    print("Orden de finalización de los hijos:", hijos_pids)

if __name__ == "__main__":
    hijos()
    padre()