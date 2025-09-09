"""
Igual que el 1a pero usando makefile

Hay que tener precaucion en el modo de lectura de la file, porque puede desincronizar el buffer
Por otro lado, hace el codigo mas legible

Se ejecuta antes de que el socket escritor
"""

import socket

HOST = "127.0.0.1"
PORT = 9101

# AF_INET = IPv4, SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(8)
    print(f"[TCP/IPv4 makefile] {HOST}:{PORT}")

    try:
        while True:    # servidor secuencial
            conn, addr = srv.accept()
            print("Conexión de", addr)
            # `makefile("rwb", buffering=0)` → read/write binario, sin buffer adicional
            with conn, conn.makefile("rwb", buffering=0) as f:

        # lee línea a línea hasta que no haya mas, raw hace que incluya el salto de linea
                for raw in f:
                    
                    line = raw.rstrip(b"\r\n")  # elimina el salto de linea de Windows (igual que antes)
                    f.write(b"eco: " + line + b"\n")
            print("Cierre de", addr)
    except KeyboardInterrupt:
        print("\nServidor detenido")