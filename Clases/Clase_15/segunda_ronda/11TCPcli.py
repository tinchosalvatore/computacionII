"""
Implementar un mini-protocolo textual:
     PING→PONG, ECHO <msg>, TIME

Es como si tuvieramos un servidor que responde a los comandos del cliente

ejecutar primero el script y despues el nc
nc 127.0.0.1 9011     
"""

import socket
import time

HOST, PORT = "127.0.0.1", 9011

# gestiona una linea que entra
def handle_line(line: str) -> str:
    line = line.strip()
    if line == "PING":
        return "PONG\n"
    if line.startswith("ECHO "):   #si es ECHO respone con un eco de lo que sigue
        return line[5:] + "\n"
    if line == "TIME":    
        return time.strftime("%Y-%m-%d %H:%M:%S") + "\n"   # devuelve la hora
    return "ERR desconocido\n"

# IPv4, TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # permite reusar la direccion
    srv.bind((HOST, PORT))   # asocia el socket al puerto
    srv.listen(8)    # backlog, max 8
    print(f"CMD en {HOST}:{PORT}")

    while True:    # aceptar conexiones secuencialmente
        conn, addr = srv.accept()
        with conn, conn.makefile("rwb", buffering=0) as f:   # crea una file que usa como buffer
            for raw in f:  # itera por líneas (bloqueante)
                resp = handle_line(raw.decode("utf-8", "replace"))  # llama a la funcion
                f.write(resp.encode("utf-8"))   # responde