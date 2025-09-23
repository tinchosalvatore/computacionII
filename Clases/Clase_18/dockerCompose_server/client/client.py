import socket

SERVER_HOST = "server"  # nombre del servicio del servidor en docker-compose
SERVER_PORT = 9999

message = "time"   #en minuscula pero el .upper del server lo va a gestionar correctamente

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
    data, addr = s.recvfrom(1024)
    print("Time received from server:", data.decode())