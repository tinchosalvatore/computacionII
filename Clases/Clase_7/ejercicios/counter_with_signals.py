"""
Imprime un contador por cada segundo

1. Si recibe SIGUSR1, reinicia el contador a 0
2. Si recibe SIGINT (Ctrl+C), muestra un mensaje de salida y termina
"""
import os
import signal
import sys
import time

# Inicamos el contador desde 0
contador = 0

# DEFINIMOS LOS HANDLERS

# Si recibe la señal SIGUSR1 reinicia el contador
def reiniciar_contador(signum, frame):
    global contador     #Importa la variable contador
    print(f"\n[+] Señal {signum} recibida: reiniciando contador a 0.")
    contador = 0        #Reinicia su valor

# Funcion encargada de terminar el programa en caso de recibir SIGINT
def terminar_programa(signum, frame):
    print(f"\n[+] Señal {signum} recibida: terminando programa.")
    sys.exit(0)

# Asociar señales a los handlers
signal.signal(signal.SIGUSR1, reiniciar_contador)
signal.signal(signal.SIGINT, terminar_programa)

print(f"[PID]: {os.getpid()}")
print("Ctrl+C para terminar, o usá `kill -USR1 <pid>` desde otra terminal para reiniciar el contador.")

# Bucle principal que mantiene el programa en ejecucion y contando
while True:
    print(f"Contador: {contador}")
    contador += 1
    time.sleep(1)
