import socket
import os

SOCKET_PATH = "/tmp/eco.sock"

# Primero hay que iniciar el socket UNIX con `nc -lU /tmp/eco.sock`
def main():
    if not os.path.exists(SOCKET_PATH):
        raise SystemExit(f"No existe {SOCKET_PATH}. ¿Arrancaste `nc -lU {SOCKET_PATH}`?")

    # socket.socket() crea un socket, la familia se ingresa como argumento
    # AF_UNIX = socket archivo local, tipo archivo, por ser UNIX, STREAM = similar a TCP 
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)   # Establece la conexion con el servidor local de UNIX (si fuera online, lo haria con el servidor remoto)
        s.sendall(b"hola desde UDS\n")

        # `nc` no hace eco automático, pero podés teclear algo y ENTER en la terminal del nc
        
        data = s.recv(4096)  # especificamos cuantos datos queremos recibir
        print(f"< {data!r}")

if __name__ == "__main__":
    main()