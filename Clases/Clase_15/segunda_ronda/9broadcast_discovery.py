"""
Enviar broadcasts para descubrir servidores en la red

    -u es para UDP
    -l es listen 
nc -u -l 0.0.0.0 9008
"""
import socket

PORT = 9008
BROADCAST = ("255.255.255.255", PORT)     # definimos la IP broadcast

 # AF_INET = IPv4, SOCK_DGRAM = UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    # setsockopt es de option (configura el socket) y lo que hacemos es indicarle que puede enviar broadcast
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    
    s.settimeout(3.0)   # aumente un poco el t de espera de rta del servidor
    
    s.sendto(b"DISCOVER?", BROADCAST)  # se supone que el 9008 reciba el broadcast
    
    try:
        data, addr = s.recvfrom(4096)
        print(f"{addr} -> {data!r}")
    except socket.timeout:
        print("Nadie respondió al broadcast (o la red lo filtra)")   # efectivamente, en mi caso, la red lo filtra