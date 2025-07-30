"""
Enunciado:

Escriba un script en Python llamado gestor.py que reciba argumentos desde la línea de comandos utilizando argparse:

    La opción --num indica la cantidad de procesos hijos a crear.
    La opción --verbose activa mensajes detallados.

Cada proceso hijo debe dormir entre 1 y 5 segundos y luego terminar. 
El proceso padre debe imprimir su PID y mostrar la jerarquía de procesos usando pstree -p.

Desde otra terminal, el estudiante deberá observar el estado de los procesos con ps o accediendo a /proc.
"""


import argparse
import os
import random
import time



def create_child_processes(num_processes, verbose):
    
    # Por el numero de procesos hijos a crear
    for _ in range(num_processes):
        pid = os.fork()
        
        if pid == 0:  # Proceso hijo
            sleep_time = random.randint(5, 10)

            # Imprimir el PID del proceso hijo y el tiempo de sueño
            if verbose:
                print(f"Proceso hijo {os.getpid()} durmiendo por {sleep_time} segundos.")
            time.sleep(sleep_time)
            os._exit(0)  # Terminar el proceso hijo


        else:  # Proceso padre
            if verbose:
                print(f"Proceso padre {os.getpid()} ha creado un hijo con PID {pid}.")
                
                jerarquia = os.system(f"pstree -p {os.getpid()}")  # Mostrar la jerarquía de procesos
                print (f"Imprimiendo la jerarquía de procesos: {jerarquia}")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Gestor de procesos hijos")
    
    # Argmento para la cantidad de procesos hijos
    parser.add_argument("--num", type=int, required=True, help="Cantidad de procesos hijos a crear")
    
    # Argumento para activar los mensajes detallados
    parser.add_argument("--verbose", action="store_true", help="Activar mensajes detallados")

    
    args = parser.parse_args()

    # Crear los procesos hijos
    create_child_processes(args.num, args.verbose)


# Al ejecutar este script, se deben proporcionar los argumentos necesarios, por ejemplo:
# python3 gestor.py --num 3 --verbose