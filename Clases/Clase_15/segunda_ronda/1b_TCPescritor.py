"""
Este es el que mande y recibe el eco del lector del makefile

Se debe ejecutar primero el lector, que abre el socket
"""

import socket

HOST = "127.0.0.1"
PORT = 9101

# AF_INET = IPv4, SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    
    # Se conecta, manda el mensaje y cierra la escritura / lectura
    c.connect((HOST, PORT))    # si el lector no se inicia antes, no se conecta a nada
    for msg in ["hola", "mundo", "fin"]:
        c.sendall((msg + "\n").encode("utf-8"))
    c.shutdown(socket.SHUT_WR)

    buf = [] # buffer para recibir el eco
    while True:
        b = c.recv(4096)
        if not b: 
            break
        buf.append(b)

print(b"".join(buf).decode("utf-8", "replace"))   # imprime lo recibido en el buffer