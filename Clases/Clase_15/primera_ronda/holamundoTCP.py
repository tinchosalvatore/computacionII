"""
Conectarse a 127.0.0.1:9001, enviar el "hola mundo!", leer respuesta y cerrar
"""

import socket

def main():

    # Debemos iniciarlizar el servidor  -->  nc -l 127.0.0.1 9001
    HOST, PORT = "127.0.0.1", 9001   # es el local host y un puerto que seguro esta libre
        
        # familias -->  AF_INET = IPv4, SOCK_STREAM = TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))                # Inica la conexion 3-way handshake TCP
        s.sendall(b"hola mundo\n")            # envío atómico, van a parar a un buffer para su futura lectura
        data = s.recv(4096)                    # bloquea hasta recibir algo o cerrar
        print(f"< {data!r}")

if __name__ == "__main__":
    main()