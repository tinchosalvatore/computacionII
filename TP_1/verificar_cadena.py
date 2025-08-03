#!/usr/bin/env python3
from multiprocessing import Process
import json
import hashlib
import os
from main import cargar_cadena    # Traemos de main la funcion que lee las cadenas

# <------------- Funciones relacionadas con la verificacion de la blockchain -----------------> 

# Recalculamos el hash de cada bloque para verificar que sea correcta
def calcular_hash_determinista(bloque):
    prev_hash = bloque.get("prev_hash", "")
    datos = bloque.get("datos", {})
    timestamp = bloque.get("timestamp", "")
    datos_serializados = json.dumps(datos, sort_keys=True, separators=(",", ":"))
    to_hash = prev_hash + datos_serializados + timestamp
    return hashlib.sha256(to_hash.encode()).hexdigest()


def escribir_reporte(resultados, path="reporte.txt"):
    lines = []
    lines.append(f"Total de bloques: {resultados['total_bloques']}")
    lines.append(f"Bloques con alerta (válidos): {resultados['alertas']}")
    lines.append(f"Bloques corruptos: {len(resultados['corruptos'])}")
    if resultados["corruptos"]:
        lines.append("Detalle de bloques corruptos:")
        for idx, errores in resultados["corruptos"]:
            for err in errores:
                lines.append(f"  - Bloque {idx}: {err}")

    contenido = "\n".join(lines)
    with open(path, "w") as f:
        f.write(contenido)
    print(contenido)


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

    resultados = {
        "total_bloques": total_bloques,
        "alertas": alertas,
        "corruptos": corruptos
    }

    # Escribir informe
    escribir_reporte(resultados)
    return resultados


def main():
    blockchain_path = "blockchain.json"
    chain = cargar_cadena(blockchain_path)
    if not chain:
        print("No hay cadena que verificar en blockchain.json")
    else:
        p = Process(target=verificar_cadena, args=(chain,))
        p.start()
        p.join()


if __name__ == "__main__":
    main()
