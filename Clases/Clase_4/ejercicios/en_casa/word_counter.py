#Implementa un sistema donde el proceso padre lee un archivo de texto 
# y envía su contenido línea por línea a un proceso hijo a través de un pipe.
# El hijo debe contar las palabras en cada línea y devolver el resultado al padre.

import os

def main():
    pid = os.fork()  # Crea un nuevo proceso hijo

    # Creo las dos pipes
    read_fd, write_fd = os.pipe()
    read_fd2, write_fd2 = os.pipe()

    if pid > 0:  # Proceso padre
        os.close(read_fd)  # Cierra el extremo de lectura del primer pipe
        os.close(write_fd2)  # Cierra el extremo de escritura del segundo pipe

        # Lee el texto y lo almacena en una variable "texto"
        with open("ej2.txt", "r", encoding="utf-8") as f:
            texto = f.read()

        palabras = texto.split()  # Divide el texto en una lista de palabras

        # Envía cada palabra al hijo a través del pipe
        for palabra in palabras:
            os.write(write_fd, (palabra + "\n").encode())  # Envía cada palabra con un salto de línea
        print("El padre envió todas las palabras")
        os.close(write_fd)  # Cierra el extremo de escritura del primer pipe

        # Lee el resultado del hijo
        resultado = os.read(read_fd2, 1024).decode()  # Lee y decodifica el resultado
        print(f"Soy el padre y recibí: {resultado}")
        os.close(read_fd2)  # Cierra el extremo de lectura del segundo pipe

        os.wait()  # Espera a que el hijo termine

    else:  # Proceso hijo
        os.close(write_fd)  # Cierra el extremo de escritura del primer pipe
        os.close(read_fd2)  # Cierra el extremo de lectura del segundo pipe

        # Lee las palabras enviadas por el padre
        datos = os.read(read_fd, 1024).decode()  # Lee y decodifica los datos
        palabras = datos.strip().split("\n")  # Divide las palabras por líneas

        # Calcula la cantidad de palabras
        resultado = f"La cantidad de palabras es {len(palabras)}"
        print("Soy el hijo y envié el resultado al padre")

        # Envía el resultado al padre
        os.write(write_fd2, resultado.encode())
        os.close(write_fd2)  # Cierra el extremo de escritura del segundo pipe
        os.close(read_fd)  # Cierra el extremo de lectura del primer pipe
        os._exit(0)  # Termina el proceso hijo

if __name__ == "__main__":
    main()