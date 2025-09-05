"""
Responder al remitente con lo mismo que envía; no hay conexiones.

nc -u 127.0.0.1 9013
"""

import socket

HOST, PORT = "0.0.0.0", 9013

# AF_INET = IPv4, SOCK_DGRAM = UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"UDP eco en {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(4096)
        print(f"{addr} -> {data!r}")
        s.sendto(data, addr)    # recibe la data y la envia de vuelta con UDP