"""
Atender una conexion por vez, y luego volver a accept()

nc 127.0.0.1 9101
"""

import socket

HOST = "127.0.0.1"   
PORT = 9101

# AF_INET = IPv4, SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reusar la direccion
    srv.bind((HOST, PORT))  # asocia el socket al puerto
    srv.listen(8)   # backlog
    print(f"[TCP/IPv4] Escuchando en {HOST}:{PORT} — Ctrl+C para salir")

    try:
        while True:  # servidor secuencial
            conn, addr = srv.accept()
            print("Conexión de", addr)
            with conn:
                # TCP es un stream de bytes: podemos recibir trozos parciales.
                # Acumulamos en 'buffer' y vamos extrayendo líneas terminadas en \n.

                buffer = bytearray()    # array pero en vez de cualquier tipo de dato, de bytes
                while True:
                    chunk = conn.recv(4096)   
                    if not chunk:             # si no hay msj, el peer cerró escritura
                        break
                    buffer.extend(chunk)   # agrega lo recibido al buffer

                    # Procesar todas las líneas completas presentes en el buffer
                    while True:
                        nl = buffer.find(b"\n")   # busca salto de linea
                        
                        if nl == -1:   #significa que aun no hay salto de linea
                            break  
                        line = buffer[:nl]            

                        # Convierte el \r\n (Windows) en \n  (UNIX)
                        if line.endswith(b"\r"):
                            line = line[:-1]   # elimina el \r

                        # repueste prefija, un eco
                        resp = b"eco: " + line + b"\n"
                        conn.sendall(resp)

                        # Consumimos la línea + el salto de línea del buffer
                        del buffer[:nl+1]
                print("Cierre de", addr)
    
    except KeyboardInterrupt:   # en caso de presionar Ctrl+C
        print("\nServidor detenido")