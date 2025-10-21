"""
Objetivo: Crear un servidor echo IPv6 que devuelva todo lo que recibe en mayúsculas.

Requisitos
    Usar IPv6 exclusivamente
    Escuchar en el puerto 8888
    Convertir mensajes a mayúsculas antes de responder
    Mantener la conexión abierta para múltiples mensajes

Desafío adicional: Implementar un comando "QUIT" para cerrar la conexión.

Para probar el servidor usamos NetCat o Telnet con IPv6:
nc -6 ::1 8888   o    telnet ::1 8888
"""
import socketserver
import socket

# Handler de los echo de los clientes
class ManejadorEchoIPv6(socketserver.BaseRequestHandler):   
    
    def handle(self):
        print(f"Conexión establecida con: {self.client_address}")
        
        try:
            while True:
                # Recibir datos del cliente
                data = self.request.recv(1024)
                
                # Si no hay datos, se cerro la conexion
                if not data:
                    break
                
                # Decodificar el mensaje recibido
                mensaje = data.decode().strip()
                print(f"Recibido de {self.client_address}: {mensaje}")
                
                # Desafio adicional: manejar el comando "QUIT"
                if mensaje.upper() == "QUIT":
                    respuesta = "Conexión cerrada por el cliente"
                    self.request.sendall(respuesta.encode())
                    break
                
                # Convertir a mayúsculas y enviar respuesta
                respuesta = mensaje.upper() + '\n'
                self.request.sendall(respuesta.encode())
            
        # excepciones
        except ConnectionResetError:
            print(f"Conexión reseteada por el cliente: {self.client_address}")
        except Exception as e:
            print(f"Error manejando cliente {self.client_address}: {e}")
        finally:
            print(f"Conexión cerrada con: {self.client_address}")

# servidor con threading
class ServidorEchoIPv6(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6   # IPv6
    allow_reuse_address = True   # para poder reiniciar rapido el server

def iniciar_servidor():
    HOST = '::1'  # localhost IPv6
    PORT = 8888
    
    servidor = ServidorEchoIPv6((HOST, PORT), ManejadorEchoIPv6)    # indicamos que el handler va a ser el de los ECHO
    print(f"Servidor echo IPv6 iniciado en [{HOST}]:{PORT}")
    print("Este servidor hace echo de los mensajes en mayúsculas")
    print("Enviar 'QUIT' o 'quit' para cerrar la conexión")
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        servidor.shutdown()
    finally:
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()