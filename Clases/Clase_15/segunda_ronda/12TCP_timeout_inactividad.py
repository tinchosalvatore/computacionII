"""
Cerrar conexiones “colgadas” para liberar recursos.

Establecemos un tiempo maximo de espera de conexion

nc 127.0.0.1 9012
"""

import socket

HOST, PORT = "127.0.0.1", 9012
IDLE_TIMEOUT = 10  # segundos

# AF_INET = IPv4, SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv: 
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # permite reusar la direccion
    srv.bind((HOST, PORT))     # asocia el socket al puerto
    srv.listen(8)     # backlog (lista de conexiones pendientes)
    print(f"Timeout server en {HOST}:{PORT} (IDLE={IDLE_TIMEOUT}s)")

    while True:
        conn, addr = srv.accept()
        with conn:
            conn.settimeout(IDLE_TIMEOUT)     # 10s de espera pára la conexion
            try:
                while True:    # recibe hasta que no hay mas datos y rompe la conexion
                    b = conn.recv(4096)
                    if not b:
                        break
                    conn.sendall(b)
            except socket.timeout:
                print("Inactividad excedida para", addr)
                # cierre implícito al salir del with