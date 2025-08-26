"""
Para ejecutar este código, primero debemos levantar un servidor TCP con netcat en el puerto 9002:

nc -l 127.0.0.1 9002
"""

import socket

# Función para enviar varias líneas de texto a través de un socket
def send_lines(sock, lines):
    for line in lines:
        # Aseguramos que cada línea termine con un salto de línea (\n)
        if not line.endswith("\n"):
            line += "\n"
        sock.sendall(line.encode("utf-8"))   # Enviamos la linea


# Función para recibir datos a través de un socket hasta que el servidor cierre la conexión
def recv_until_closed(sock):
    # chunks son bloques de datos qeu se reciben atraves del socket
    chunks = []
    while True:
        # Recibimos datos de a 1024 bytes
        b = sock.recv(1024)
        # Si no se reciben datos, significa que el servidor cerró la conexión
        if not b:  
            break
        
        # Agregamos los datos recibidos al chunk
        chunks.append(b)
    return b"".join(chunks)

def main():
    HOST, PORT = "127.0.0.1", 9002    # Direccion y puerto del servidor
    
    # Creamos un socket TCP con contexto (osea el with)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # Conectamos al servidor
        
        send_lines(s, ["uno", "dos", "tres"])  # Enviamos las tres lineas
        
        s.shutdown(socket.SHUT_WR)      # Cerramos la conexion de escritura
        
        data = recv_until_closed(s)    # Recibimos los datos del servidor
        
        print(data.decode("utf-8", errors="replace"))   # Imprimimos los datos recibidos traducidos

if __name__ == "__main__":
    main()