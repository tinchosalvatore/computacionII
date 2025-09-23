import socket

def client(ip,port,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #IPv4, TCP
    sock.connect((ip,port))
    sock.sendall(message.encode("ascii"))
    data = sock.recv(1024).decode("ascii")
    print(f"Received from server: {data}")

if __name__ == "__main__":
    client("localhost",9999,"Hola Mundo!")