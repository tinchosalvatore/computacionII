"""
Leer payloads grandes en bucle hasta que el peer cierre. Importa para archivos o mensajes largos.

nc -l 127.0.0.1 9003 < archivo_grande.bin
"""

import socket

# Misma idea que en el anterior, recibimos los datos de a poco y los agregamos al chunk (bloque)
# Pero ahora leyendo de un archivo externo
def recv_all(sock):
    chunks = []
    while True:
        b = sock.recv(64 * 1024)  # leemos solo 64 KiB por iteración del archivo_grande.bin
        if not b:
            break
        chunks.append(b)
    return b"".join(chunks)

# Tambien igual que antes
def main():
    HOST, PORT = "127.0.0.1", 9003
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = recv_all(s)
        print(f"Recibidos {len(data)} bytes")

if __name__ == "__main__":
    main()