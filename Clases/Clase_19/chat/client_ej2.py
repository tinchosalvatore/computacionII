# guarda como cliente_chat.py y ejecuta python3 cliente_chat.py
import socket, threading
def recv_loop(s):
    while True:
        d = s.recv(1024)
        if not d:
            break
        print(d.decode(), end="")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 9000))
    threading.Thread(target=recv_loop, args=(s,), daemon=True).start()
    while True:
        m = input()
        if m.lower() in ("/salir", "/quit", "/exit"):
            break
        s.sendall(m.encode() + b"\n")
