#!/usr/bin/env python3

"""
Implemente dos scripts:

    generador.py: genera una serie de números aleatorios (parámetro --n) y los imprime por salida estándar.
    filtro.py: recibe números por entrada estándar y muestra solo los mayores que un umbral (parámetro --min).

Desde Bash, encadene la salida del primero a la entrada del segundo:

./generador.py --n 100 | ./filtro.py --min 50
"""

import argparse
import sys

def main():
    # Explicacion de esto en el otro script
    parser = argparse.ArgumentParser(description='Filtro de números mayores que un umbral.')
    parser.add_argument('--min', type=int, required=True, help='Umbral mínimo para filtrar los números.')
    args = parser.parse_args()

    umbral = args.min

    # Leer números de la entrada estándar  (osea los que vienen desde generador.py con el pipe)
    for line in sys.stdin:
        try:
            numero = int(line.strip())
            if numero > umbral:
                print(numero)
        except ValueError:
            # Si no se puede convertir a entero, ignorar la línea
            continue

if __name__ == '__main__':
    main()