
import socketserver
import argparse
from concurrent.futures import ProcessPoolExecutor
import os
import json
import socket

from processor.screenshot import take_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images

# Explicación: La worker function ahora ejecuta un pipeline de análisis completo.
def worker_function(data):
    """
    Recibe datos, incluyendo una URL, y ejecuta todas las tareas de procesamiento.
    """
    url = data.get("url")
    image_urls = data.get("image_urls", [])
    print(f"[Proceso {os.getpid()}] Iniciando análisis completo para la URL: {url}")
    
    if not url:
        return {"status": "error", "reason": "No se proporcionó URL para la tarea"}

    # --- Ejecución de todas las tareas de procesamiento ---
    screenshot_result = take_screenshot(url)
    performance_result = analyze_performance(url)
    images_result = process_images(image_urls)

    # --- Consolidación de resultados ---
    final_result = {}
    if screenshot_result.get('status') == 'success':
        final_result['screenshot'] = screenshot_result['screenshot']
    
    if performance_result.get('status') == 'success':
        final_result['performance'] = performance_result['performance']

    if images_result.get('status') == 'success':
        final_result['thumbnails'] = images_result['thumbnails']

    # Determinamos el estado general del procesamiento.
    if any(key in final_result for key in ['screenshot', 'performance', 'thumbnails']):
        final_result['status'] = 'success'
    else:
        final_result['status'] = 'error'
        final_result['reason'] = "Todas las tareas de procesamiento fallaron."

    print(f"[Proceso {os.getpid()}] Análisis completo finalizado para: {url}")
    return final_result

# Explicación: Este es el manejador de peticiones. Cada vez que el Servidor A
# se conecte, se creará una instancia de esta clase.
class TCPServerRequestHandler(socketserver.BaseRequestHandler):
    """
    Manejador de peticiones para el servidor TCP.
    Se instancia una vez por cada conexión.
    """
    def handle(self):
        # Explicación: Definimos un protocolo simple:
        # 1. El cliente envía 4 bytes que indican la longitud del mensaje (en big-endian).
        # 2. El cliente envía el mensaje JSON con esa longitud.
        # Esto permite al servidor saber exactamente cuántos bytes leer.
        try:
            # 1. Leer la longitud del mensaje (4 bytes)
            raw_msg_len = self.request.recv(4)
            if not raw_msg_len:
                return # Conexión cerrada por el cliente
            msg_len = int.from_bytes(raw_msg_len, 'big')

            # 2. Leer el mensaje JSON completo
            data = self.request.recv(msg_len)
            task = json.loads(data.decode('utf-8'))
            print(f"[Servidor] Tarea recibida de {self.client_address[0]}: {task}")

            # 3. Enviar la tarea al pool de procesos.
            # `self.server.executor` es la referencia al ProcessPoolExecutor.
            future = self.server.executor.submit(worker_function, task)
            
            # 4. Esperar el resultado del proceso.
            result = future.result()

            # 5. Enviar el resultado de vuelta al Servidor A usando el mismo protocolo.
            response = json.dumps(result).encode('utf-8')
            response_len = len(response).to_bytes(4, 'big')
            self.request.sendall(response_len + response)
            print(f"[Servidor] Resultado enviado a {self.client_address[0]}: {result}")

        except Exception as e:
            print(f"[ERROR] Ocurrió un error manejando la petición: {e}")

# Explicación: Subclase de ThreadingTCPServer para poder pasarle el executor
# al manejador de peticiones. Cada conexión se maneja en un thread separado,
# y ese thread delega el trabajo pesado a un proceso del pool.
class ProcessPoolTCPServer(socketserver.ThreadingTCPServer):
    """
    Servidor TCP que utiliza un pool de procesos para manejar las tareas.
    """
    def __init__(self, server_address, RequestHandlerClass, executor):
        # Habilitar la reutilización de direcciones para reinicios rápidos del servidor
        self.allow_reuse_address = True
        super().__init__(server_address, RequestHandlerClass)
        self.executor = executor
        # Determinar la familia de direcciones (IPv4/IPv6) desde la tupla de dirección
        self.address_family = socket.AF_INET6 if ':' in server_address[0] else socket.AF_INET


def main():
    # Explicación: Usamos argparse para configurar el servidor desde la línea
    # de comandos, como pide el enunciado.
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha (IPv4 o IPv6)")
    parser.add_argument("-p", "--port", required=True, type=int, help="Puerto de escucha")
    parser.add_argument("-n", "--processes", type=int, default=os.cpu_count(), help="Número de procesos en el pool (default: número de CPUs)")
    args = parser.parse_args()

    # Explicación: Creamos el pool de procesos que se compartirá entre todas
    # las conexiones. El `with` asegura que se cierre correctamente al finalizar.
    with ProcessPoolExecutor(max_workers=args.processes) as executor:
        
        # Pasamos el executor al constructor de nuestro servidor personalizado.
        server = ProcessPoolTCPServer((args.ip, args.port), TCPServerRequestHandler, executor)
        
        print(f"Servidor de Procesamiento escuchando en {args.ip}:{args.port} con {args.processes} procesos.")
        
        try:
            # El servidor corre indefinidamente hasta que se interrumpe con Ctrl+C
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
        finally:
            # Cierre limpio del servidor y del pool de procesos.
            server.shutdown()
            server.server_close()
            print("Servidor cerrado.")

if __name__ == "__main__":
    main()
