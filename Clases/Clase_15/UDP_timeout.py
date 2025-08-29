"""
UDP puede perder paquetes ya que no garantiza la llegada. Implementamos reintentos con timeout para ver si llega 
en algun momento

Cambie el settimeout de afuera a adentro del bucle for para que se espere 1 segundo en todos los intentos 
no solo en el primero. Y le puse 3 seg para que se note mas la espera
"""

import socket

HOST, PORT = "127.0.0.1", 9007   # localhost

# IPv4, UDP  (como el otro ej de UDP)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    
    retries = 3
    for i in range(1, retries + 1):

        # settimeout establece cuanto tiempo espera el socket para obtener una respuesta del servidor
        s.settimeout(3.0)    
        
        try:
            s.sendto(b"TIME", (HOST, PORT))
            data, _ = s.recvfrom(2048)
            print("Respuesta:", data.decode())
            break   # En caso de haber recibido respuesta, rompe el bucle
        except socket.timeout:
            print(f"Timeout intento {i}; reintentando...")
    else:
        print("Sin respuesta tras 3 reintentos")