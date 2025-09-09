"""
Es el cliente que envia los comandos al servidor, despues recibe e imprime las respuestas

Se debe levantar antes el otro socket para poder establecer la conexion
"""

import socket

HOST, PORT = "127.0.0.1", 9102

# Se crea el socket, se conecta y manda todos los cmd posibles. Luego apaga su r/w
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, PORT))
    for msg in ["PING", "ECHO hola", "TIME", "FOO"]:
        c.sendall((msg + "\n").encode("utf-8"))
    c.shutdown(socket.SHUT_WR)

# recibe e imprime toda las respuestas
    data = []
    while True:
        b = c.recv(1024)
        if not b: 
            break
        data.append(b)

print(b"".join(data).decode("utf-8", "replace"))