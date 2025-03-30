# Haz que un proceso hijo reemplace su contexto de ejecución con un programa del sistema
# Por ejemplo, el comando ls -l, utilizando exec().

import os

pid = os.fork()     # Creamos un proceso hijo
if pid == 0:        # Si es el proceso hijo
    os.execlp('ls', 'ls', '-l')     # Reemplazamos el contexto de ejecución del proceso hijo con el comando ls -l
else:
    os.wait()       # Esperamos a que el proceso hijo termine
    print('Proceso hijo terminado')