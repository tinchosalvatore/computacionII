"""
5
Manejar servidores que responden lento o aún no están arriba

# Arrancarlo más tarde para forzar reintentos
nc -l 127.0.0.1 9004

La idea es que una vez que arranco y se hizo el "ping" que imprime el server al conectarse el socket, 
el servidor debe responder algo para que se terminen los intentos de conexion. 
Si no responde algo el servidor se cuenta como un fallo
"""

import socket
import time

HOST, PORT = "127.0.0.1", 9004

# base_backoff es el tiempo de espera entre reintentos que despues se multiplica por el numero de intento
def try_connect(max_retries=5, base_backoff=0.5):   
    for attempt in range(1, max_retries + 1):  # Va a intentar max 5 veces
        
        # Intento de conexion, seria el caso en el que si sale bien la conexion
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Socket IPv4, TCP. Como antes
                s.settimeout(1.5)  # segundos
                s.connect((HOST, PORT))
                s.sendall(b"ping\n")
                data = s.recv(1024)
                return data
            
            # Si el servidor no responde, se lanza la excepcion que espera y reintenta
        except (socket.timeout, ConnectionRefusedError) as e:
            sleep_s = base_backoff * attempt   # aumentamos el tiempo de espera por cada intento fallido
            print(f"Intento {attempt} falló ({e}). Reintento en {sleep_s:.1f}s...")
            time.sleep(sleep_s)
    raise TimeoutError("Servidor no disponible tras varios reintentos")   # levantamos la excepcion

if __name__ == "__main__":
    print(try_connect())   # Queremos que se muestre en pantalla el contenido de la execpcion o la data recibida