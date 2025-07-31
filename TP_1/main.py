from csv import list_dialects
from multiprocessing import Process, Queue, Pipe
import time
import random
from datetime import datetime, timedelta


# <------------- Funcion del Proceso Principal ----------------->

def generador_principal(freq_generador, presion_generador, oxigeno_generador):
    print("Proceso Principal generando los datos...")
    for i in range(60):
        # Generacion del diccionario de datos
        datos = {
            "timestamp": datetime.now().isoformat(),
            "frecuencia": random.randint(60, 180),
            "presion": [random.randint(110, 180), random.randint(70, 110)],
            "oxigeno": random.randint(90, 100)
        }
        # Envio de datos con pipes
        freq_generador.send(datos)
        presion_generador.send(datos)
        oxigeno_generador.send(datos)
        time.sleep(1)

    # Enviamos una ultima señal vacia para indicar el fin de la lectura de la pipe
    freq_generador.send(None)
    presion_generador.send(None)
    oxigeno_generador.send(None)  


# <------------- Funciones utilizadas por los analizadores ----------------->

# Funciones de los calculos estadisticos usados 
def media(lista):
    return sum(lista) / len(lista) if lista else 0

def desviacion_estandar(lista):   # Elegi calcular la muestral insesgada
    if len(lista) < 2:
        return 0
    media_valor = media(lista)
    return (sum((x - media_valor) ** 2 for x in lista) / (len(lista) - 1))** 0.5


# Funcion encargada de validar los datos que sean de los ultimos 30s
def datos_validos(lista):
    timestamp_actual = datetime.now()
    datos_aprobados = [] 
    
    for ts, dato in lista:
        ts_dt = datetime.fromisoformat(ts)  # Convertimos el formato de las timestamps para calcular los tiempos
        if (timestamp_actual - ts_dt).total_seconds() <= 30:
            datos_aprobados.append((dato))
    
    return datos_aprobados


# <------------- Funciones de los Procesos Analizadores ----------------->

def analizar_frecuencia(queue, freq_analizador):
    lista = []
    
    while True:
        datos = freq_analizador.recv()
        if datos is None:
            break
        lista.append((datos["timestamp"], datos["frecuencia"]))
        

    frecuencias = datos_validos(lista)    

    media_frecuencia = media(frecuencias)
    desviacion_frecuencia = desviacion_estandar(frecuencias)


def analizar_presion(queue, presion_analizador):
    lista = []
    
    while True:
        datos = presion_analizador.recv()
        if datos is None:
            break
        lista.append((datos["timestamp"], datos["presion"]))
        

    presiones = datos_validos(lista)

    media_presion = media(presiones)
    desviacion_presion = desviacion_estandar(presiones)


def analizar_oxigeno(queue, oxigeno_analizador):
    lista = []

    while True:
        datos = oxigeno_analizador.recv()
        if datos is None:
            break
        lista.append((datos["timestamp"], datos["oxigeno"]))



    oxigenos = datos_validos(lista)

    media_oxigeno = media(oxigenos)
    desviacion_oxigeno = desviacion_estandar(oxigenos)





# <------------- Funcion Main del programa ----------------->

def main():
    queue = Queue()

# Definimos los extremos de las pipes
    freq_generador, freq_analizador = Pipe(duplex=False)   # Duplex False significa que son unidireccionales
    presion_generador, presion_analizador = Pipe(duplex=False)
    oxigeno_generador, oxigeno_analizador = Pipe(duplex=False)


    # Vamos a almacenar los procesos para luego poder terminarlos
    procesos = []

    # Proceso Principal
    p_principal = Process(target=generador_principal, args=(freq_generador, presion_generador, oxigeno_generador))
    procesos.append(p_principal)
    p_principal.start()
    

    # Procesos de análisis
    p_A= Process(target=analizar_frecuencia, args=(queue, freq_analizador))
    p_B= Process(target=analizar_presion, args=(queue, presion_analizador))
    p_C= Process(target=analizar_oxigeno, args=(queue, oxigeno_analizador))
    
    procesos.append(p_A)
    procesos.append(p_B)
    procesos.append(p_C)

    p_A.start()
    p_B.start()
    p_C.start()

