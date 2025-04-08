import os

def main():
    # Crear el pipe (retorna dos file descriptors), uno para lectura y otro para escritura
    read_fd, write_fd = os.pipe()

    pid = os.fork()     # Crea un nuevo proceso hijo

    if pid > 0:         # Si es el proceso padre
        os.close(read_fd)  # Cierra el fd de lectura, ya que el padre va a escribir, no leer

        mensaje = "Hola desde el padre!"
        os.write(write_fd, mensaje.encode())      # Escribe en el pipe el mensaje
        print("Padre escribió:", mensaje)

        os.close(write_fd)      # Cierra el fd de escritura, porque ya escribio
        os.wait()       # Espera a que finalice el proceso hijo

    else:            # Si es el proceso hijo    
        os.close(write_fd)  # Cierra el fd de escritura, porque el hijo va a leer, no escribir 

        datos = os.read(read_fd, 1024)      # Leer hasta 1024 bytes del pipe
        print("Hijo recibió:", datos.decode())      # .decode() decodifica los bytes a un string

        os.close(read_fd)   # Cierra el fd de lectura, porque ya leyo
        os._exit(0)         # Termina el proceso hijo

if __name__ == "__main__":
    main()