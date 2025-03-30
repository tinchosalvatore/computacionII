# Genera un proceso hijo que siga ejecutándose luego de que el padre haya terminado. 
# Verifica que su nuevo PPID corresponda al proceso init o systemd.

import os
import time

pid = os.fork()

if pid > 0:  # Si el PID es mayor a 0, entonces es el padre
    print("Proceso padre eliminado")
    os._exit(0)
else:
    print("Proceso hijo huérfano. Padre desaparecido.")
    time.sleep(10)  # Tiempo para observar el estado del proceso
    
    # Verificar el nuevo PPID del proceso hijo
    nuevo_ppid = os.getppid()
    print(f"Soy el proceso hijo y mi nuevo PPID es: {nuevo_ppid}")
    
    # Verificación simple de que el nuevo padre es un proceso de sistema
    if nuevo_ppid == 1:
        print("Verificado: Mi nuevo padre es init/systemd")
    else:
        print("Advertencia: El nuevo padre no es init/systemd")
        print("Esto puede ocurrir en diferentes sistemas operativos")