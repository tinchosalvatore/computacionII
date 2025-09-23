import socketserver
from datetime import datetime

# Handler para clientes UDP, gestiona el TIME para obter a hora
class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        try:
            data = self.rfile.read().decode('ascii').strip()
            command = data.upper()   # para que "time" tmb funcione

            if command == "TIME":
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response = f"Current time: {now}"
            else:
                response = "Invalid command, try TIME"

            self.wfile.write(bytes(response, 'ascii'))

        except Exception as e:   # error generico para no parar el servidor
            print(f"Error handling request: {e}")


# Servidor UDP multithread
class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999   # para escuchar en todas las interfaces

    try:
        server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
        print("UDP server listening on port:", PORT)
        server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
