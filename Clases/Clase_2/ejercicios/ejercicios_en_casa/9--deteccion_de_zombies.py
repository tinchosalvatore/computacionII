#Escribe un script que recorra /proc y detecte procesos en estado zombi, listando su PID, PPID y nombre del ejecutable. 
#Este ejercicio debe realizarse sin utilizar ps.
import os

# Este script detecta procesos en estado zombi en el sistema Linux
# y muestra su PID, PPID y nombre del ejecutable.
def detectar_zombis():
    # os.listdir('/proc'): Lista todos los archivos y directorios dentro de /proc
    for pid in os.listdir('/proc'):
        if pid.isdigit():   # Verifica si el nombre del archivo es un número (PID)
            try:
                with open(f"/proc/{pid}/status") as f:  # Abre el archivo de estado del proceso
                    lines = f.readlines()       # Lee todas las líneas del archivo
                    estado = next((l for l in lines if l.startswith("State:")), "") # Busca la línea que comienza con "State:"
                    if "Z" in estado:       # Si el estado contiene "Z", es un proceso zombi
                        nombre = next((l for l in lines if l.startswith("Name:")), "").split()[1]
                        ppid = next((l for l in lines if l.startswith("PPid:")), "").split()[1]
                        print(f"Zombi detectado → PID: {pid}, PPID: {ppid}, Nombre: {nombre}")
            except IOError:     # Maneja el error si el proceso ya no existe y continua
                continue

detectar_zombis()