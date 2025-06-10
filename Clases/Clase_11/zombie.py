"""
Cree un script en Python que genere un proceso hijo que finaliza inmediatamente 
El padre no deberá recolectar su estado hasta al menos 10 segundos después

Desde Bash, utilice ps y /proc/[pid]/status para identificar el estado Z (zombi) del hijo.
"""

import os
import time

def create_zombie_process():
    pid = os.fork() # Creamos el hijo con fork
    
    if pid == 0:  # Proceso hijo
        print(f"Proceso hijo {os.getpid()} creado. Y terminado abruptamente.")
        os._exit(0)  # Terminar inmediatamente el proceso hijo

    else:  # Proceso padre
        print(f"Proceso padre {os.getpid()} ha creado un hijo con PID {pid}.")
        print("Esperando 10 segundos antes de recolectar el estado del hijo...")
        time.sleep(10)  # Esperar 10 segundos antes de recolectar el estado del hijo
        
        os.waitpid(pid, 0) # Con el wait chequeamos el estado del hijo
        print(f"Proceso hijo {pid} ha sido recolectado.")

if __name__ == "__main__":
    create_zombie_process()
    