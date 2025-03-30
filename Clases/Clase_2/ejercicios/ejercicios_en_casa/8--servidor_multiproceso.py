#Imita el comportamiento de un servidor concurrente que atiende múltiples clientes creando un proceso hijo por cada uno 
# Cada proceso debe simular la atención a un cliente con un sleep().
import os
import time

# Lista de clientes a atender formato ("nombre", "proceso", "resultado")
clientes = [
    ("Descargar archivo", "Descargando archivo...", "Descarga completada"),
    ("Enviar archivo", "Enviando archivo...", "Archivo enviado"),
    ("Actualizar base de datos", "Actualizando base de datos...", "Base de datos actualizada"),
    ("Realizar copia de seguridad", "Realizando copia de seguridad...", "Copia de seguridad completada"),
    ("Generar informe", "Generando informe...", "Informe generado")
]

# Itera sobre el nombre y la tarea creando un hijo por cada tarea
for nombre, proceso, resultado in clientes:
    pid = os.fork()  # Crea un hijo con fork()
    if pid == 0:  # Si pid es 0, es el hijo
        print(f"Hijo PID: {os.getpid()}, atendiendo proceso: {nombre}, {proceso}, {resultado}")
        time.sleep(5)  # Tiempo simula una tarea breve
        os._exit(0)   # Finaliza el hijo

# El padre recoge los resultados de los hijos, y vez por cada uno    
for i in range (len(clientes)):
    pid = os.wait()  # Espera a que un hijo termine
    print(f"El padre ha terminado de esperar al hijo con PID: {pid}")
print("Se han atendido todos los clientes.")