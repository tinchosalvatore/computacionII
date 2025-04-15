# Crea una cadena de tres procesos conectados por pipes donde: el primer proceso genera números aleatorios entre 1-100 
# El segundo proceso filtra solo los números pares, y el tercer proceso calcula el cuadrado de estos números pares.

import os
import random


# definimos la funcion que va a generar los numeros
def generar_num():
    numeros = []   # Con esta lista vamos a almacenar los numeros para enviarlos
    # El for se ejecuta 10 veces, para generar los 10 numeros
    for i in range(10):
        num = random.randint(1, 100)        # genera un num random entre 1 y 100
        print(f"Numero generado: {num}")
        numeros.append(str(num))          # Los almacena en una variable numeros
    return numeros

# Definimos la funcion que va a filtrar los numeros pares de la lista
def filtrar_pares(numeros):
    pares = []   # Con esta lista vamos a almacenar los numeros pares
    for num in numeros:
        if int(num) % 2 == 0:      # Si el numero es par
            pares.append(str(num))      # Lo agregamos a la lista de pares
    return pares

# Definimos la funcion que va a calcular el cuadrado de los numeros pares
def cuadrados(pares):
    resultados = []
    for par in pares:
        calculo = int(par*par)
        resultados.append(str(calculo))
    return resultados

def main ():
    pid = os.fork()
    write_fd, read_fd = os.pipe()
    write_fd2, read_fd2 = os.pipe()

    if pid == 0:
        os.close(read_fd)
        print(f"Soy el proceso {os.getpid()} que genera 10 numeros random entre 1 y 100")
        
        # Enviamos la lista de numeros que retorno la funcion
        numeros = generar_num()
        numeros_str = ",".join(numeros)     # Convertimos la lista en una string para poder enviarlos
        print (f"Los numeros aleatorios son {numeros}")

        os.write(write_fd, numeros_str.encode())
        os.close(write_fd)

        os._exit(0)     # Terminamos el proceso

    else:
        # Este proceso solo lo vamos a usar para tener otro proceso mas
        os.wait()
        pid = os.fork()

        if pid == 0:
            os.close(write_fd)
            os.close(read_fd2)
            print(f"Soy el proceso{os.getpid()} que se encarga de filtar los numeros pares ")

            # Vamos a leer la lista de numeros recibida
            numeros = []    #Lista vacia para llenarla
            
            nums = os.read(read_fd, 1024)       #Leemos los numeros
            nums = nums.decode()        # Los decodificamos
            nums = int(nums)        # Los convertimos en enteros
            numeros.append(nums)        # Los metemos en la lista

            # Enviamos la lista de numeros pares
            pares = filtrar_pares(numeros)
            pares_str = ",".join(pares)
            print (f"Los numeros pares son {pares}")
            
            os.write(write_fd, pares_str.encode())
            os.close(write_fd2)

            os._exit(0)     # Terminamos el proceso

        else:
            os.close(write_fd2)
            print(f"Soy el proceso{os.getpid()} que se encarga de calcular el cuadrado de los numeros pares recibidos ")
            
            pares = []      # Lista para almacenar los numeros pares

            # Leemos la lista de numeros pares que llega
            pars = os.read(read_fd2, 1024)     # Leemos los numeros
            pars = pars.decode()        # Los decodificamos
            pars = int(pars)        # Los convertimos en enteros
            pares.append(pars)        # Los metemos en la lista

            resultados = cuadrados(pares)

            print (f"Los resultados al calcular los cuadrados de los numeros pares son {resultados}")

            os.wait()

if __name__ == "__main__":
    main()