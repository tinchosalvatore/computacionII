#!/usr/bin/env python3
from multiprocessing import Process
import json
import hashlib
from main import cargar_cadena    # Importamos lectura de cadenas desde main

# <------------- Funciones relacionadas con la verificacion de la blockchain -----------------> 

# Recalculamos el hash de cada bloque para verificar que sea correcta
def calcular_hash_determinista(bloque):
    prev_hash = bloque.get("prev_hash", "")
    datos = bloque.get("datos", {})
    timestamp = bloque.get("timestamp", "")
    datos_serializados = json.dumps(datos, sort_keys=True, separators=(",", ":"))
    to_hash = prev_hash + datos_serializados + timestamp
    return hashlib.sha256(to_hash.encode()).hexdigest()

# <------------- Funciones relacionadas al reporte final -----------------> 

# Calcula los promedios generales de los bloques no corruptos
def promedios_generales(chain, corruptos_indices):
    suma_freq = suma_oxi = suma_sis = suma_dia = 0.0
    bloques_validos = 0

     # Por cada diccionario (bloque) en la cadena
    for i, bloque in enumerate(chain):

        # Si el indice del bloque, esta en la lista de indices de bloques corruptos, saltea esa iteracion
        if i in corruptos_indices:   
            continue

        # Obtenemos los datos de cada bloque
        datos = bloque["datos"]
        frecu_media = datos["frecuencia"]["media"]
        oxi_media = datos["oxigeno"]["media"]
        pres_media = datos["presion"]["media"]
        sistolica = pres_media["sistolica"]
        diastolica = pres_media["diastolica"]

        # Sumamos la frecuencia para calcular sus promedios
        suma_freq += frecu_media
        suma_oxi += oxi_media
        suma_sis += sistolica
        suma_dia += diastolica
        bloques_validos += 1

    # Si todos eran invalidos devolvemos 0 en todas las medias generales
    if bloques_validos == 0:
        return {
            "frecuencia": 0,
            "oxigeno": 0,
            "presion_sistolica": 0,
            "presion_diastolica": 0,
        }

    return {
        "frecuencia": suma_freq / bloques_validos,
        "oxigeno": suma_oxi / bloques_validos,
        "presion_sistolica": suma_sis / bloques_validos,
        "presion_diastolica": suma_dia / bloques_validos,
    }


def escribir_reporte(resultados, path="reporte.txt"):
    
    # Organizamos como vamos a escribir la informacion importante en el reporte
    lines = []
    lines.append(f"Total de bloques: {resultados['total_bloques']}")
    lines.append(f"Bloques con alerta (válidos): {resultados['alertas']}")
    lines.append(f"Bloques corruptos: {len(resultados['corruptos'])}")
    
    # Escribimos los detalles de los bloques corruptos, si es que los hay
    if resultados["corruptos"]:
        lines.append("Detalle de bloques corruptos:")
        for idx, errores in resultados["corruptos"]:
            for err in errores:
                lines.append(f"  - Bloque {idx}: {err}")
    
    # Escribimos los promedios generales de los datos
    lines.append("")
    lines.append("Promedios (solo bloques íntegros):")
    avg = resultados["promedios"]
    lines.append(f"  Frecuencia: {avg['frecuencia']:.2f}")
    lines.append(f"  Oxígeno: {avg['oxigeno']:.2f}")
    lines.append(f"  Presión sistólica: {avg['presion_sistolica']:.2f}")
    lines.append(f"  Presión diastólica: {avg['presion_diastolica']:.2f}")

    # Escribimos el reporte
    contenido = "\n".join(lines)
    with open(path, "w") as f:
        f.write(contenido)
    print(contenido)
    print ("Informe finalizado!")


def verificar_cadena(chain):
    corruptos = []
    total_bloques = len(chain)
    alertas = 0

    prev_hash_esperado = "0" * 64
    corruptos_indices = set()

    for i, bloque in enumerate(chain):
        errores = []

        # 1. Verificamos el encadenamiento previo
        if bloque.get("prev_hash", "") != prev_hash_esperado:
            errores.append(f"Encadenamiento incorrecto, debia ser {prev_hash_esperado}, pero llego {bloque.get('prev_hash')}")

        # 2. Verificamos el hash actual
        hash_recalculado = calcular_hash_determinista(bloque)
        hash_almacenado = bloque.get("hash", "")
        if hash_recalculado != hash_almacenado:
            errores.append(f"Hash incorrecto, debia ser {hash_almacenado}, pero llego {hash_recalculado}")

        if errores:
            corruptos.append((i, errores))
            corruptos_indices.add(i)

        # Actualizar prev_hash esperado (se sigue la cadena tal como está escrita, incluso si está corrupta)
        prev_hash_esperado = bloque.get("hash", "")

    # Contar alertas: solo en bloques no corruptos
    for i, bloque in enumerate(chain):
        if i in corruptos_indices:
            continue
        if bloque.get("alerta", False):
            alertas += 1

    # promedios
    promedios = promedios_generales(chain, corruptos_indices)

    resultados = {
        "total_bloques": total_bloques,
        "alertas": alertas,
        "corruptos": corruptos,
        "promedios": promedios
    }

    # Escribir informe
    escribir_reporte(resultados)
    return resultados


def main():
    blockchain_path = "blockchain.json"
    chain = cargar_cadena(blockchain_path)      # Chain es una lista de diccionarios con cada bloque como diccionario
    if not chain:
        print("No hay cadenas que verificar en blockchain.json")
    else:
        p = Process(target=verificar_cadena, args=(chain,))
        p.start()
        p.join()


if __name__ == "__main__":
    main()