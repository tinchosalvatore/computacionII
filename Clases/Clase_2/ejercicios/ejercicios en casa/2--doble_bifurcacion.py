#Escribe un programa donde un proceso padre cree dos hijos diferentes (no en cascada)
# y cada hijo imprima su identificador. 
#El padre deberá esperar a que ambos terminen.

import os

for i in range(2):      # Iteramos dos veces para crear dos hijos
    pid = os.fork()     # Creamos los hijos con fork
    if pid == 0:
        print("Soy el hijo con PID = ", os.getpid())
        os._exit(0)
    else:
        os.wait()     # Esperamos a que los hijos terminen

print(f"Soy el padre con PID = ({os.getpid()}). Mis hijos terminaron")