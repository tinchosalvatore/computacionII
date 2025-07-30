"""
Implemente un script que use fork() para crear un proceso hijo. 
Ese hijo deberá reemplazar su imagen de ejecución por el comando ls -l usando exec().

Desde Bash, verifique el reemplazo observando el nombre del proceso con ps.
"""

import os

# exec nos permite reemplazar la imagen del proceso actual con un nuevo programa.
def main():
    pid = os.fork()
    
    # hijo
    if pid == 0:
        os.execlp("ls", "ls", "-l")  # Reemplaza la imagen del proceso hijo con 'ls -l'
    
    else:  
        os.wait()

if __name__ == "__main__":
    main()

# Al ejecutar este script se deberia ejecutar el comando ls -l