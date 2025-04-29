"""
Crear un proceso padre que crea un hijo, espera una señal del hijo con SIGUSR1 y que al recibirla 
imprima un msj y termine

El hijo duerme unos segundos y luego envia la señal SIGUSR1 al padre con os.kill()
"""
import os
import signal
import time
import sys

# Definimos el handler que todo lo que va a hacer es imprimir la señal y finalizar el script
def handler_usr1(signum, frame):
    print(f"\n[Padre] Señal {signum} recibida desde el hijo. Finalizando.")
    sys.exit(0)

if __name__ == "__main__":
    # Obtener el PID del proceso actual (será el del padre)
    pid_padre = os.getpid()

    # Establecer handler para SIGUSR1 en el padre
    signal.signal(signal.SIGUSR1, handler_usr1)

    pid_hijo = os.fork()

    if pid_hijo == 0:
        # Estamos en el hijo
        print(f"[Hijo] Soy el proceso hijo con PID {os.getpid()}")
        time.sleep(3)
        print(f"[Hijo] Enviando SIGUSR1 al padre con PID {pid_padre}")
        os.kill(pid_padre, signal.SIGUSR1)  #Envia la señal con kill
        print(f"[Hijo] Señal enviada. Terminando.")
        sys.exit(0)

    else:
        # Estamos en el padre
        print(f"[Padre] Esperando señal de mi hijo con PID {pid_hijo}...")
        while True:
            time.sleep(1)
