#Crea un programa en Python que establezca comunicación entre un proceso padre y un hijo mediante un pipe.
#El padre debe enviar un mensaje al hijo, y el hijo debe recibir ese mensaje y devolverlo al padre (eco).

import os

def eco():
    read_fd, write_fd = os.pipe()  # Crear el pipe para que el padre envie el msj y retorna los file descriptors
    read_fd2, write_fd2 = os.pipe()     # Crear otro pipe para que el padre reciba el mensaje del hijo
    
    pid = os.fork()  # Crear un nuevo proceso hijo

    if pid > 0:  # Proceso padre
        os.close(read_fd)  # Cerrar el file descriptor de lectura, solo va a enviar el mensaje (escribir)
        
        # Envia el mensaje
        mensaje = "Hola desde el padre!"  
        os.write(write_fd, mensaje.encode())    # Leer y escribir en el pipe, con encode para convertirlo a bytes
        os.close(write_fd)      # Cerrar el file descriptor de escritura ya que terminó de escribir
        print(f"Padre envio el mensaje: {mensaje} al hijo")
        

        # Leer el mensaje reenviado del hijo
        os.close(write_fd2)     # Cerrar el file descriptor de escritura
        datos = os.read(read_fd2, 1024)     # Leer hasta 1024 bytes del pipe
        print(f"Padre recibió: {datos.decode()}")
        
        os.close(read_fd2)  # Cerrar el file descriptor de lectura ya que terminó de leer
        
        os.wait()  # Esperar a que el proceso hijo termine

    
    else:  # Proceso hijo
        os.close(write_fd)  # Cerrar el file descriptor de escritura

        # Recibe el mensaje
        datos = os.read(read_fd, 1024)  # Leer hasta 1024 bytes del pipe
        print(f"Hijo recibio el mensaje: {datos.decode()}")  # .decode() decodifica los bytes a un string
        os.close(read_fd)  # Cerrar el file descriptor de lectura ya que terminó de leer

        # Reenvia el mismo mensaje que recibio, al padre
        mensaje2 = datos.decode()
        os.write(write_fd2, mensaje2.encode())  # Escribir en el pipe el mensaje
        os.close(write_fd2)  # Cerrar el file descriptor de escritura
        
        os._exit(0) # Termina el proceso hijo


if __name__ == "__main__":
    eco()