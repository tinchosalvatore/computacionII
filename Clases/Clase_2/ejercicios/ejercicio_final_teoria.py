# La ia me pidio crear un programa que:
# 1. Cree 5 procesos hijos
# 2. Cada proceso hijo debe simular una tarea diferente (ej:calculos, E/S)
# 3. El proceso padre debe esperar a todos los hijos y muestre sus codigos de salida
# 4. Maneja adecuadamente a los procesos zombies

import os
import math
import time
#Importamos la libreria de math para realizar calculos y time para controlar tiempos de espera

# Definimos las tareas en una lista de tuplas 
tareas = [
    ("cálculos", lambda: math.factorial(10), 0),
    ("E/S", lambda: time.sleep(2), 1),
    ("red", lambda: os.system("ping -c 1 localhost"), 2),
    ("cálculos", lambda: sum(range(1000)), 3),
    ("E/S", lambda: open("temp.txt", "w").write("test"), 4)
]

# Funcion para generar procesos hijos
def generar_procesos():     
    for i, (nombre, tarea, codigo) in enumerate(tareas):    # Iteramos sobre las tareas (5)
        pid = os.fork()     # Crear un proceso hijo
        if pid == 0:        # Si es el proceso hijo
            print(f"Proceso hijo {i+1} ({nombre}),  PID {os.getpid()}")
            tarea()         # Realizar la tarea
            os._exit(codigo)    # Termina con un codigo de salida unico
        else:               # Si es el proceso padre
            print(f"Proceso padre {os.getpid()} creó al hijo {pid}")
        
# Funcion para esperar a los procesos hijos
def esperar_procesos():
    for i in range(len(tareas)):    # Iteramos sobre las tareas (5)
        pid, codigo = os.wait()     # Esperar a un proceso hijo
        print(f"Proceso hijo {pid} terminó con código de salida {codigo}")