"""
    Implementa un cronómetro compartido: tres procesos actualizan cada segundo un valor Value('d')
    con el instante actual. Un cuarto proceso lee el valor cada 0,5s  y registra si hay incoherencias temporales 
    (> 1s de salto), demostrando la necesidad de sincronización.
"""
import multiprocessing as mp
import time


def productores(valor_compartido):
        
    while True:
        current_time = time.time() #Actualiza el valor_compartido con el tiempo actual cada segundo
        
        with valor_compartido.get_lock():  # Con lock marca el contenido como exclusivo, no pueden acceder procesos en simultáneo
            valor_compartido.value = current_time    # .value permite acceder al valor de la variable compartida
            print(f"Proceso {mp.current_process().name} actualizó el tiempo a: {valor_compartido.value}")
        
        time.sleep(1) # Esperar 1 segundo antes de la próxima actualización
        
        if current_time == 17:
            return False # Condición de salida para el proceso productor


# El lector lee el valor compartido y comprueba si hay incoherencias temporales
def lector(valor_compartido):

    ultimo_tiempo_leido = 0.0 # Variable para almacenar el tiempo leído en la iteración anterior, comienza en 0.0

    for i in range(30): # Leer durante 30 iteraciones (aproximadamente 15 segundos)
        with valor_compartido.get_lock():  # Sincroniza el acceso para leer
            tiempo_actual_leido = valor_compartido.value    # Lee el valor actual de la variables (cronometro) compartido

        # Si no es la primera lectura, calculamos el salto temporal, desde la ultima vez leída
        if ultimo_tiempo_leido != 0.0:  
            salto_temporal = tiempo_actual_leido - ultimo_tiempo_leido

            # Consideramos un pequeño margen de error debido a la naturaleza de los procesos
            if salto_temporal > 1.1: # Usamos 1.1 para dar un pequeño margen
                 print(f"\n--- Proceso {mp.current_process().name}: ¡Incoherencia temporal detectada! ---")
                 print(f"  Tiempo anterior: {ultimo_tiempo_leido:.4f}")
                 print(f"  Tiempo actual leído: {tiempo_actual_leido:.4f}")
                 print(f"  El Salto fue de : {salto_temporal:.4f} segundos\n")


        ultimo_tiempo_leido = tiempo_actual_leido # Actualizamos el último tiempo leído para la próxima iteración

        time.sleep(0.5) # Esperar 0.5 segundos antes de la próxima lectura


if __name__ == '__main__':
    # Valor compartido para el tiempo actual (usamos 'd' para float)
    valor_cronometro = mp.Value('d', 0.0)       # .Value() permite crear una variable compartida entre procesos
                                                # que llamamos luego con .value

    # Creamos los procesos
    p1 = mp.Process(target=productores, name="Productor 1", args=(valor_cronometro,))
    p2 = mp.Process(target=productores, name="Productor 2", args=(valor_cronometro,))
    p3 = mp.Process(target=productores, name="Productor 3", args=(valor_cronometro,))
    p4 = mp.Process(target=lector, name="Lector", args=(valor_cronometro,))

    # Inicializamos los procesos
    print("Iniciando procesos...")
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # El proceso padre espera a que terminen los procesos hijos
    p4.join()
    p1.join()
    p2.join()
    p3.join()

    print("Fin del programa")