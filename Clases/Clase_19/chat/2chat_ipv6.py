#!/usr/bin/env python3
"""
Servidor de chat (IPv4/IPv6 según HOST).
Comentarios en español. Nombres de variables en inglés. Mensajes de excepción en inglés.
"""

import socketserver
import socket
import threading


# -----------------------------------------------------------
# Clase principal que gestiona los clientes y la difusión
# -----------------------------------------------------------
class ChatServer:
    def __init__(self):
        # Diccionario de clientes conectados: socket -> dirección (como string)
        self.clients = {}

        # Lock para proteger el acceso concurrente a 'self.clients'
        # ya que múltiples hilos del servidor pueden modificarlo a la vez
        self.lock = threading.Lock()

    # -------------------------------------------------------------------
    # Formatea la dirección (IPv4 o IPv6) a un string legible: "ip:puerto"
    # -------------------------------------------------------------------
    def _format_address(self, addr_tuple):
        try:
            if isinstance(addr_tuple, tuple):
                ip = addr_tuple[0]
                port = addr_tuple[1] if len(addr_tuple) > 1 else 0
                return f"{ip}:{port}"
            return str(addr_tuple)
        except Exception:
            return "unknown:0"

    # -------------------------------------------------------------------
    # Agrega un nuevo cliente al diccionario de clientes conectados
    # y anuncia su conexión al resto (fuera del lock)
    # -------------------------------------------------------------------
    def add_client(self, client_socket, client_address):
        address_str = self._format_address(client_address)

        # Sección crítica: modificamos el diccionario compartido
        with self.lock:
            self.clients[client_socket] = address_str

        # Mensaje informativo en consola
        print(f"Cliente conectado: {address_str}")

        # Aviso al resto de clientes (fuera del lock para evitar deadlocks)
        admin_msg = f"ADMIN: El cliente {address_str} se ha unido al chat\r\n".encode()
        self.broadcast(admin_msg, origin_socket=client_socket)

    # -------------------------------------------------------------------
    # Elimina un cliente del diccionario y avisa al resto
    # -------------------------------------------------------------------
    def remove_client(self, client_socket):
        address_str = None

        # Eliminamos del diccionario dentro del lock (sección crítica)
        with self.lock:
            if client_socket in self.clients:
                address_str = self.clients.pop(client_socket)

        # Si efectivamente existía, notificamos al resto
        if address_str:
            print(f"Cliente desconectado: {address_str}")
            admin_msg = f"ADMIN: El cliente {address_str} ha dejado el chat\r\n".encode()
            self.broadcast(admin_msg, origin_socket=client_socket)
        else:
            print("El cliente indicado no está conectado al chat")

    # -------------------------------------------------------------------
    # Asegura que el mensaje termine en salto de línea (\n)
    # Esto mejora la compatibilidad con clientes como 'nc'
    # -------------------------------------------------------------------
    def _ensure_newline(self, msg_bytes):
        if not msg_bytes.endswith(b"\n"):
            return msg_bytes + b"\n"
        return msg_bytes

    # -------------------------------------------------------------------
    # Envía un mensaje a todos los clientes conectados (excepto al emisor)
    # Se evita el deadlock haciendo un snapshot de los sockets activos
    # -------------------------------------------------------------------
    def broadcast(self, message, origin_socket=None):
        # Copiamos los sockets bajo lock, para que no cambie mientras iteramos
        with self.lock:
            clients_snapshot = list(self.clients.keys())

        # Aseguramos que el mensaje tenga salto de línea
        message = self._ensure_newline(message)

        # Enviamos el mensaje a todos (fuera del lock)
        dead_clients = []
        for sock in clients_snapshot:
            if sock == origin_socket:
                continue
            try:
                sock.sendall(message)
            except Exception:
                # Si un cliente falla, lo marcamos para eliminarlo
                dead_clients.append(sock)

        # Eliminamos los clientes que fallaron (bajo lock)
        if dead_clients:
            with self.lock:
                for dead in dead_clients:
                    addr = self.clients.pop(dead, None)
                    try:
                        dead.close()
                    except Exception:
                        pass
                    if addr:
                        print(f"Removed dead client: {addr}")


# Instancia global única del servidor de chat
server_chat = ChatServer()


# -----------------------------------------------------------
# Manejador para cada cliente (cada hilo usa una instancia)
# -----------------------------------------------------------
class ChatHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Log inicial del hilo de conexión
        print("DEBUG: handle() iniciado")

        # El socket del cliente y su dirección
        client_socket = self.request
        client_address_str = server_chat._format_address(self.client_address)

        print(f"DEBUG: client_socket={client_socket}, cliente={client_address_str}")

        try:
            # Se agrega el cliente a la lista global y se notifica
            server_chat.add_client(client_socket, self.client_address)

            # Bucle principal: recepción de mensajes del cliente
            while True:
                data = client_socket.recv(1024)
                print(f"DEBUG: recibido raw={data}")

                # Si el cliente cerró la conexión, salir del bucle
                if not data:
                    break

                # Intentamos decodificar el mensaje (con reemplazo de errores)
                try:
                    message = data.decode(errors="replace").strip()
                except Exception:
                    message = "<undecodable>"

                # Comandos de salida
                if message.upper() in ("/SALIR", "/QUIT", "/EXIT"):
                    print(f"Cliente {client_address_str} solicitó salir")
                    break

                # Formateamos el mensaje con el remitente
                formatted = f"[{client_address_str}]: {message}\r\n".encode()
                print(f"MENSAJE: [{client_address_str}]: {message}")

                # Difundimos el mensaje al resto de clientes
                server_chat.broadcast(formatted, origin_socket=client_socket)

        # Excepciones comunes en conexiones de red
        except ConnectionResetError:
            print(f"Connection reset by peer: {client_address_str}")
        except Exception as e:
            print(f"Error handling client {client_address_str}: {e}")
        finally:
            # Al salir, eliminar el cliente de la lista global
            server_chat.remove_client(client_socket)

            # Cerrar el socket (en caso de seguir abierto)
            try:
                client_socket.close()
            except Exception:
                pass


# -----------------------------------------------------------
# Función principal para iniciar el servidor
# -----------------------------------------------------------
def start_server(host="127.0.0.1", port=9000):
    """
    Inicia el servidor de chat.
    - Si el host contiene ":", se asume IPv6.
    - De lo contrario, se usa IPv4.
    """

    # Determinamos la familia de direcciones según el host
    server_class = socketserver.ThreadingTCPServer
    if ":" in host:
        server_class.address_family = socket.AF_INET6
    else:
        server_class.address_family = socket.AF_INET

    # Permitir reutilizar el puerto inmediatamente después de cerrar
    server_class.allow_reuse_address = True

    # Creamos la instancia del servidor con el manejador
    server = server_class((host, port), ChatHandler)

    print(f"Servidor de chat iniciado en {host}:{port}")
    print("Todos los clientes verán los mensajes.")
    print("Para salir de un cliente: /SALIR o /QUIT")

    try:
        # Bucle principal del servidor (acepta conexiones indefinidamente)
        server.serve_forever()
    except KeyboardInterrupt:
        # Interrupción manual: cerrar ordenadamente
        print("\nCerrando servidor...")

        # Cerramos todas las conexiones activas
        with server_chat.lock:
            sockets = list(server_chat.clients.keys())
        for s in sockets:
            try:
                s.close()
            except Exception:
                pass

        # Detenemos el servidor
        server.shutdown()
    finally:
        # Liberamos recursos del socket principal
        server.server_close()


# -----------------------------------------------------------
# Ejecución directa del script
# -----------------------------------------------------------
if __name__ == "__m
