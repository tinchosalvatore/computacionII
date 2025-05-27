"""
Desarrolla un load balancer simple: un proceso maestro reparte una lista de URLs a descargar entre k procesos worker
mediante una Queue. Cada worker registra su PID y el tiempo de descarga. 
Al finalizar, el maestro debe generar un reporte ordenado por duración.

Un loadbalancer es un sistema que distribuye la descarga de tareas entre varios procesos
"""
from multiprocessing import Process, Queue, cpu_count
import os
import random


lista_urls = [
    "http://example.com",
    "http://example.org",
    "http://example.net",
    "http://example.edu",
    "http://example.gov",
    "http://example.info",
]


def worker(queue, result_queue):
    while True:
        url = queue.get()
        if url is None:
            break
        
        # Simular descarga
        t_duration = random.uniform(0.1, 2.0)  # Simular tiempo de descarga aleatorio entre 0.1 y 2 segundos
        
        result_queue.put((os.getpid(), url, t_duration))



if __name__ == "__main__":
    
    # Creamos la queue
    q = Queue() #Cola de las URLs
    result_queue = Queue()  #Cola con los resultados para el reporte ordenado por duracion
    k = cpu_count() # Numero de procesos workers que podemos crear

    # Lista para procesos workers
    workers = []

    # El maestro reparte crea los workers en base al numero de CPUs
    for _ in range(k):
        p = Process(target=worker, name= "worker", args=(result_queue, q))
        workers.append(p)
        p.start()

    # Carga las URLs en la cola
    for url in lista_urls:
        q.put(url)
    # Enviamos una señal de terminación a cada worker (La logica del worker toma None como señal de break)
    for _ in range(k):
        q.put(None)
    
    # Esperar a que todos los procesos terminen
    for p in workers:
        p.join()

    # Generar el reporte
    report = []
    while not result_queue.empty():     # Mientras haya resultados en la cola de resultados
        report.append(result_queue.get())       # Ponerlos en la lista report
    
    # Ordenar el reporte por duración
    report.sort(key=lambda x: x[2])  
    
    # Imprimir el reporte
    print("Reporte de descargas:")
    print("PID\tURL\tDuración")
    for pid, url, duration in report:   # Por cada resultado en el reporte
        print(f"{pid}\t{url}\t{duration:.2f} segundos")
    
    # Imprimir el tiempo total de ejecución
    total_time = sum(duration for _, _, duration in report)     # Sumar todas las duraciones
    print(f"\nTiempo total de ejecución de todas las descargas: {total_time:.2f} segundos")