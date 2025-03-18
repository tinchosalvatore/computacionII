import argparse

def main():
    parser = argparse.ArgumentParser(description='Procesa un archivo de entrada y generar uno de salida')
    
    parser.add_argument('-i', '--input',  required=True, help='Nombre del archivo de entrada')
    parser.add_argument('-o', '--output', required=True, help='Nombre del archivo de salida')
    
    args = parser.parse_args()
    
    print(f'Input file is {args.input}')
    print(f'Output file is {args.output}')
    print('Los archivos han sido procesados.')

if __name__ == '__main__':
    main()
