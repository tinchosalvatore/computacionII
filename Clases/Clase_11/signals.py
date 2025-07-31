"""
Cree un script que instale un manejador para la señal SIGUSR1.
El proceso deberá estar en espera pasiva (pause() o bucle infinito)

Desde Bash, envíe la señal al proceso con kill -SIGUSR1 [pid] y verifique la respuesta.
"""
import os
import signal
import sys
import time

# La señal SIGUSR1 es una señal definida por el usuario, por eso dice USR

# Para el manejo de señales primero debemos definir el manejador de señales
def signal_handler(signum, frame):
    print(f"Señal {signum} recibida!")
    sys.exit(0)


pid = os.fork()

if pid == 0:
    while True:
        print(f"Proceso {os.getpid()} Esperando señal SIGUSR1...")
        signal.signal(signal.SIGUSR1, signal_handler)
        signal.pause()
        time.sleep(1)

else:
    os.waitpid(pid, 0)  