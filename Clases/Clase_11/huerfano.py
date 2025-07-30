"""
Diseñe un script que cree un proceso hijo que siga ejecutándose luego de que el proceso padre haya terminado.

Verifique desde Bash que el nuevo PPID del proceso hijo corresponde a init o systemd  (Osea el proceso 1).
"""

import os
import time

def main():
    # Crear un proceso hijo que se ejecuta en segundo plano
    pid = os.fork()
    
    # Proceso hijo
    if pid == 0:
        # Cuando el PPID es 1 es que fue adoptado por init o systemd. 
        # En mi caso (Fedora) fue systemd --user, el cual tenia pid 2522
        while True:
           print(f"Soy el proceso hijo con PID {os.getpid()}. Mi PPID es {os.getppid()}.")
           time.sleep(2)   
    
    else:
        # Proceso padre
        print(f"Soy el proceso padre y he creado un hijo con PID {pid}. Ahora terminaré.")
        os._exit(0)
    
if __name__ == "__main__":
    main()
