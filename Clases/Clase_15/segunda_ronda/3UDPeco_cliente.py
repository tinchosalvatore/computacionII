"""
Se conecta y manda un ping. Recibe el eco y lo imprime
"""

import socket

HOST, PORT = "127.0.0.1", 9201

# AF_INET = IPv4, SOCK_DGRAM = UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
    # Enviamos y esperamos respuesta (bloqueante)
    c.sendto(b"ping", (HOST, PORT))
    data, addr = c.recvfrom(4096)
    print(f"< {data!r} desde {addr}")