#!/usr/bin/env python3

"""
Implemente dos scripts:

    generador.py: genera una serie de números aleatorios (parámetro --n) y los imprime por salida estándar.
    filtro.py: recibe números por entrada estándar y muestra solo los mayores que un umbral (parámetro --min).

Desde Bash, encadene la salida del primero a la entrada del segundo:

./generador.py --n 100 | ./filtro.py --min 50
"""

import random
import argparse

# --n es la cantidad de números aleatorios a generar

def main():
    # Definimos el objeto que nos deja recibir los argumentos, descriptor es lo que aparece si el usuario pide --help
    parser = argparse.ArgumentParser(description='Generador de números aleatorios.')
    # Añadimos el argumento 
    parser.add_argument('--n', type=int, required=True, help='Cantidad de números aleatorios a generar.')
    # Procesa los argumentos recibidos del usuario
    args = parser.parse_args()

    numeros_generados = []

    for _ in range(args.n):
        numero = random.randint(0, 100)
        print(numero)
        numeros_generados.append(numero)

    return numeros_generados

# Despues de ejecutar el script, usar el grep (pipe |) para enviar los numeros aleatorio como parametros a filtro.py
if __name__ == '__main__':
    main()