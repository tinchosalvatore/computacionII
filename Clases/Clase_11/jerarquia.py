"""
Ejecute un script en Python que cree dos procesos hijos
Desde Bash, utilice pstree -p y ps --forest para observar la jerarquía

Capture la salida y explique la genealogía de los procesos.
"""
import os
import time

pid1 = os.fork()
pid2 = os.fork()

if pid1 == 0:
    print(f"Proceso hijo 1 con PID: {os.getpid()} y PPID: {os.getppid()}")
    time.sleep(20)


elif pid2 == 0:
    print(f"Proceso hijo 2 con PID: {os.getpid()} y PPID: {os.getppid()}")
    time.sleep(20)


else:
    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)
    print(f"Proceso padre con PID: {os.getpid()} ha terminado.")
    print("Todos los procesos hijos han finalizado.")

# Al ejecutar, conviene verlo con pstree -p PPID
# Asi vemos la jerarquia desde el padre