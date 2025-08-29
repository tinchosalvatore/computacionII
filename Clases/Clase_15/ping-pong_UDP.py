"""
UDP es datagramas: no hay conexión ni stream. La idea es enviar/recibir con sendto/recvfrom.

La diferencia entre UDP y TCP es que UDP no garantiza la llegada de los mensajes (mas bien, no revisa si llego)

nc -u -l 127.0.0.1 9006
Escribir la respuesta manual “pong” desde el local host cuando el cliente envíe “ping” 

"""

import socket

HOST, PORT = "127.0.0.1", 9006   # puerto local


# AF_INET = IPv4, SOCK_DGRAM = UDP  
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"ping", (HOST, PORT))      # Enviamos el mensaje ping al servidor
    
#El mensaje se almacena en la variable data y la dirección del servidor que lo envió se almacena en la variable addr
    data, addr = s.recvfrom(2048)  
    print(f"< {data!r} desde {addr}")