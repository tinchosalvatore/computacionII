import socket

def send_data(sock: socket.socket, data: bytes):
    """
    Envía datos a través de un socket prefijando el mensaje con su longitud.
    Protocolo: 4 bytes para la longitud (big-endian) + datos.
    """
    try:
        # Empaqueta la longitud de los datos en 4 bytes y la envía.
        message_len = len(data).to_bytes(4, 'big')
        sock.sendall(message_len + data)
    except socket.error as e:
        print(f"[Protocol] Error al enviar datos: {e}")
        # Relanzamos la excepción para que el llamador pueda manejarla.
        raise

def receive_data(sock: socket.socket) -> bytes | None:
    """
    Recibe datos de un socket que usan el protocolo de longitud prefijada.
    """
    try:
        # Lee los primeros 4 bytes para obtener la longitud del mensaje.
        raw_msglen = sock.recv(4)
        if not raw_msglen:
            # Si no se reciben datos, el cliente cerró la conexión.
            return None
        
        msglen = int.from_bytes(raw_msglen, 'big')
        
        # Lee exactamente la cantidad de bytes que se esperan.
        # MSG_WAITALL asegura que la recepción se bloquee hasta que todos los bytes lleguen.
        return sock.recv(msglen, socket.MSG_WAITALL)
    except (socket.error, ConnectionResetError) as e:
        print(f"[Protocol] Error al recibir datos: {e}")
        return None
    except Exception as e:
        print(f"[Protocol] Error inesperado al recibir datos: {e}")
        return None
