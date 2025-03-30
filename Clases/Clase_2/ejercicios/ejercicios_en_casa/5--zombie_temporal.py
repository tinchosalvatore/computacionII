#Crea un programa que genere un proceso hijo que termine inmediatamente 
# Pero el padre no debe recoger su estado de salida durante algunos segundos.
# Observa su estado como zombi con herramientas del sistema.

import os
import time


pid = os.fork()
if pid == 0:        # Proceso hijo y vemos su pid
    print(f"Soy el hijo con PID {os.getpid()}") 
else:
    print(f"Soy el padre con PID {os.getpid()}")    # Proceso padre no llama a wait para que el hijo sea zombie
    time.sleep(15)  # Esperamos 15 segundos para que el hijo sea zombie durante este tiempo
    print("fin del tiempo, el hijo ya no es zombie")
    os.wait()       # El padre recoge el estado de salida del hijo