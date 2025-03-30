# Construye un programa que cree tres hijos en paralelo (no secuenciales). 
# Cada hijo ejecutará una tarea breve y luego finalizará. El padre debe esperar por todos ellos.
import os
import time

# Variables para las tareas
x = 4
y= 5

print(f"Las variables son: x = {x}, y = {y}")

# Lista de las tareas por "nombre, tarea"
tareas = [
    ("Sumar", x+y),
    ("Restar", x-y),
    ("Multiplicar", x*y)
]

# Itera sobre el nombre y la tarea creando un hijo por cada tarea
for nombre, tarea in tareas:
    pid = os.fork()  # Crea un hijo con fork()
    if pid == 0:  # Si pid es 0, es el hijo
        print(f"Hijo PID: {os.getpid()}, tarea a cargo: {nombre}, resultado: {tarea}")
        time.sleep(2)  # Tiempo simula una tarea breve
        os._exit(0)   # Finaliza el hijo

# El padre recoge los resultados de los hijos, y vez por cada uno    
for i in range (3):
    pid = os.wait()  # Espera a que un hijo termine
    print(f"El padre ha terminado de esperar al hijo con PID: {pid}")
print("El padre ha terminado de esperar a todos los hijos.")