"""
El UDP de llegada trae la direccion del remitente, asi que le respondemos
No se garantiza la llegada de los mensajes
"""

import socket

HOST, PORT = "0.0.0.0", 9201  # 0.0.0.0 = todas las interfaces

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))  # asocia el socket al puerto
    print(f"[UDP/IPv4] {HOST}:{PORT}")
    try:
        while True:
            data, addr = s.recvfrom(4096)  # bloquea hasta recibir data
            print(f"{addr} -> {data!r}")
            s.sendto(data, addr)           # eco al remitente
    except KeyboardInterrupt:
        print("\nServidor UDP detenido")