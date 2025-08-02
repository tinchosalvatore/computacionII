from multiprocessing import Process, Queue, Pipe
import time
import random
from datetime import datetime, timedelta
import os
# Imports para el blockchain
import json
import hashlib


# <------------- Funcion del Proceso Principal ----------------->

def generador_principal(freq_generador, presion_generador, oxigeno_generador):
    print("Proceso Principal generando los datos...")
    print("Tomara aproximadamente 1 minuto")
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
    print("Generacion de datos terminada")

# <------------- Funciones utilizadas por los analizadores ----------------->

# Funciones de los calculos estadisticos usados 
def media(lista):
    return sum(lista) / len(lista) if lista else 0

def desviacion_estandar(lista):   # Elegi calcular la muestral insesgada
    if len(lista) < 2:
        return 0
    media_valor = media(lista)
    return (sum((x - media_valor) ** 2 for x in lista) / (len(lista) - 1))** 0.5


# Funcion encargada de validar los datos que sean de la ventana de los ultimos 30s
def validar_datos(ventana: list, ts_str: str, valor, ventana_segundoos: int = 30):  
    
# ventana es una lista de tuplas con la siguiente forma: (timestamp, valor)

    ts_dt = datetime.fromisoformat(ts_str) # Convertimos la timestamp de str a datetime
    ventana.append((ts_dt, valor))
    
    segundos = ts_dt - timedelta(seconds=ventana_segundoos) #timedelta convierte int a unidades de tiempo para operar con tiempos

    while ventana and ventana[0][0] < segundos:
        ventana.pop(0) # Con pop eliminamos los datos viejos de la lista cada vez que superamos el tiempo limite

    # Filtramos los valores sacando las timestamps
    # En el caso de la presion, hay dos valores
    if ventana:
        muestra = ventana[0][1]
        if isinstance(muestra, (list, tuple)) and len(muestra) == 2:
            sistolicas = [v[0] for _, v in ventana]
            diastolicas = [v[1] for _, v in ventana]
            return sistolicas, diastolicas
    
    # En el caso del oxigeno y la frecuencia, hay un solo valor
    return [v for (_, v) in ventana]


# <------------- Funciones de los Procesos Analizadores ----------------->

def analizar_frecuencia(queue, freq_analizador):
    ventana = []  # Lista para los datos dentro de la ventana de tiempo  
    
    print("Iniciando calculos para el analisis de la frecuencia")
    while True:
        datos = freq_analizador.recv()  # recibimos los datos por pipe
        if datos is None:
            break
        ts = datos["timestamp"]
        frecuencia = datos["frecuencia"]
        
        # Evaluamos la ventana de los ultimo 30 segundos por cada iteracion y calculamos sus estadisticos muestrales
        frecuencias = validar_datos(ventana, ts, frecuencia)

        media_frecuencia = media(frecuencias)
        desviacion_frecuencia = desviacion_estandar(frecuencias)

        # Enviamos los resultados a la queue para el Verificador
        resultados = {
            "tipo": "frecuencia",
            "timestamp": ts,
            "media": media_frecuencia,
            "desviacion": desviacion_frecuencia
        }
        queue.put(resultados)
    # Señal de fin
    queue.put({"tipo": "fin", "origen": "frecuencia"})
    print("Fin de calculos para el analisis de la frecuencia")




def analizar_presion(queue, presion_analizador):
    ventana = []
    
    print("Iniciando calculos para el analisis de la presion")
    while True:
        datos = presion_analizador.recv()
        if datos is None:
            break
        ts = datos["timestamp"]
        presion = datos["presion"]

        sistolicas, diastolicas = validar_datos(ventana, ts, presion)

        media_sistolicas = media(sistolicas)
        desviacion_sistolicas = desviacion_estandar(sistolicas)

        media_diastolicas = media(diastolicas)
        desviacion_diastolicas = desviacion_estandar(diastolicas)
        
        resultados = {
          "tipo": "presion",
          "timestamp": ts,
          "media": {"sistolica": media_sistolicas, "diastolica": media_diastolicas},
          "desv": {"sistolica": desviacion_sistolicas, "diastolica": desviacion_diastolicas}
        }

        queue.put(resultados)
    
    queue.put({"tipo": "fin", "origen": "presion"})
    print("Fin de los calculos para el analisis de la presion")  



def analizar_oxigeno(queue, oxigeno_analizador):
    ventana = []

    print("Iniciando calculos para el analisis de oxigeno")
    while True:
        datos = oxigeno_analizador.recv()
        if datos is None:
            break
        ts = datos["timestamp"]
        oxigeno = datos["oxigeno"]

        oxigenos = validar_datos(ventana, ts, oxigeno)

        media_oxigeno = media(oxigenos)
        desviacion_oxigeno = desviacion_estandar(oxigenos)

        resultados = {
            "tipo": "oxigeno",
            "timestamp": ts,
            "media": media_oxigeno,
            "desviacion": desviacion_oxigeno
        }
        queue.put(resultados)

    queue.put({"tipo": "fin", "origen": "oxigeno"})
    print("Fin de los calculos para el analisis de oxigeno")


# <------------- Funciones utilisadas por el Proceso Verificador -----------------> 

# Extrae las medias de los diccionarios de entrada
def extraer_medias(grupo):
    frecuencia_media = grupo["frecuencia"]["media"]
    oxigeno_media = grupo["oxigeno"]["media"]
    sistolica_media = grupo["presion"]["media"]["sistolica"]  # solo sistólica

    return frecuencia_media, oxigeno_media, sistolica_media

# Usa extraer_medias para evaluar si hay alerta con ellas
def evaluar_alerta(grupo):
    frecuencia_media, oxigeno_media, sistolica_media = extraer_medias(grupo)

    if frecuencia_media >= 200:
        return True
    if not (90 <= oxigeno_media <= 100):
        return True
    if sistolica_media >= 200:
        return True
    return False

# <------------- Funciones relacionadas con la construccion de la blockchain ----------------->  


# <------------- Funcion del Proceso Verificador ----------------->  

# Encargada de verificar si hay alerta en los datos, y de escribir la blockchain
def verificador(queue, blockchain_path):
    buffer = {}  # Para agrupar los datos por timestamp 
    finishes = set()  # Vamos a usarlo para confirmar que todos los procesos han terminado
    
    chain = []
    prev_hash = "0" * 64  # genesis


    while True:
        datos = queue.get()  

    # Este bloque se encarga de verificar la llegada del "fin" de cada medicion para medir el fin de la queue
        if datos["tipo"] == "fin":
            finishes.add(datos["origen"])
            # Si llego el "fin" de todos las mediciones que evaluamos, rompemos el bucle 
            if finishes == {"frecuencia", "presion", "oxigeno"}:    
                break
            continue # Aun no se coleccionario todos los "fin", asi que continuamos la iteracion

        ts = datos["timestamp"]
        tipo = datos["tipo"]

        # Este bloque de codigo junta los datos por timestamp
        buffer.setdefault(ts, {})[tipo] = datos # Creamos un sub-diccionario para cada timestamp

        if all(k in buffer[ts] for k in ("frecuencia", "presion", "oxigeno")): # Verifica si las ts tienen los 3 datos 
            grupo = buffer.pop(ts)  # Junta los tres datos con el ts
            alerta = evaluar_alerta(grupo)
            if alerta:
                print(f"Alerta detectada en {ts}")  # Debuggin, no se producen porque los datos no pueden dar alerta

            # Armado del campo "datos"
            datos = {
                "frecuencia": {
                    "media": grupo["frecuencia"]["media"],
                    "desv": grupo["frecuencia"]["desviacion"]
                },
                "presion": {
                    "media": {
                        "sistolica": grupo["presion"]["media"]["sistolica"],
                        "diastolica": grupo["presion"]["media"]["diastolica"]
                    },
                    "desv": {
                        "sistolica": grupo["presion"]["desv"]["sistolica"],
                        "diastolica": grupo["presion"]["desv"]["diastolica"]
                    }
                },
                "oxigeno": {
                    "media": grupo["oxigeno"]["media"],
                    "desv": grupo["oxigeno"]["desviacion"]
                }
            }

            # Construcción del bloque
            bloque = {
                "timestamp": ts,
                "datos": datos,
                "alerta": alerta,
                "prev_hash": prev_hash  # hash de la cadena anterior
            }

                            # Hash determinista
            # Convertimos el diccionario a string de .json
            datos_serializados = json.dumps(datos, sort_keys=True, separators=(",", ":")) 
            to_hash = prev_hash + datos_serializados + ts     # Calcula la base del hash, aun no hasheado
            hash_actual = hashlib.sha256(to_hash.encode()).hexdigest()   # Hasheamos la base que construimos
            bloque["hash"] = hash_actual  # Añadimos el hash al bloque


            # Encadenar en memoria
            chain.append(bloque)
            prev_hash = hash_actual  # actualizo para el siguiente bloque

            # Ultimo requisito del 
            indice = len(chain) - 1
            print(f"Bloque {indice}: hash={hash_actual} alerta={alerta}")
    


# <------------- Funcion Main del programa ----------------->

def main():
    queue = Queue()

# Definimos los extremos de las pipes, el primero es read y el segundo es write (receive y send)
    freq_analizador, freq_generador = Pipe(duplex=False)   # Duplex False significa que son unidireccionales
    presion_analizador, presion_generador = Pipe(duplex=False)
    oxigeno_analizador, oxigeno_generador = Pipe(duplex=False)


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

    # Proceso Verificador
    blockchain_path = "blockchain.json"  
    p_Verificador = Process(target=verificador, args=(queue, blockchain_path))
    procesos.append(p_Verificador)
    p_Verificador.start()


    # Nos aseguramos de que todos los procesos terminen
    for p in procesos:
        p.join()



if __name__ == "__main__":
    main()