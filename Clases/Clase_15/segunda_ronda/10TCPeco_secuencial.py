"""
Atender una conexion por vez, y luego volver a accept()
util para entender el ciclo de vida sin concurrencia

nc 127.0.0.1 9010

"""
import socket

HOST, PORT = "127.0.0.1", 9010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #config que permite reusar direccion
    srv.bind((HOST, PORT))   # asocia el socket al puerto
    srv.listen(8)  # backlog   (donde llegan las peticiones de conexion), max 8
    print(f"Escuchando en {HOST}:{PORT} ... Ctrl+C para salir")

    while True:     # acepta conexiones de manera secuencial
        conn, addr = srv.accept() 
        print("Conexión de", addr)
        with conn:
            while True:
                b = conn.recv(4096)   
                if not b:
                    break  # si no hay msj, el peer cerró
                conn.sendall(b)  # hace eco de lo recibido, en el mismo servidor
        print("Cierre de", addr)