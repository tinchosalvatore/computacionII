import socketserver
import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from processor import screenshot, performance, image_processor
from common.protocol import receive_data, send_data
from common.serialization import serialize_data, deserialize_data
import base64

# Esta función será ejecutada en un proceso separado por el ProcessPoolExecutor
def processing_task(url):
    """
    Ejecuta las tareas de procesamiento CPU-bound para una URL dada.
    Devuelve un diccionario con los resultados.
    """
    print(f"[ProcessPool] Processing URL: {url}")
    try:
        # 1. Generar screenshot (debe devolver bytes)
        screenshot_bytes = screenshot.take(url)
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')

        # 2. Analizar rendimiento
        perf_data = performance.analyze(url)
        
        # 3. Procesar imágenes y generar thumbnails (debe devolver lista de strings base64)
        thumbnails_base64 = image_processor.process(url)

        return {
            "screenshot": screenshot_base64,
            "performance": perf_data,
            "thumbnails": thumbnails_base64,
            "status": "success"
        }
    except Exception as e:
        print(f"[ProcessPool] Error processing {url}: {e}")
        return {"error": str(e), "status": "failed"}

# Hacemos el pool global para que sea accesible desde el handler.
# En una aplicación más compleja, se podría inyectar de otra forma.
PROCESS_POOL = None

class TCPHandler(socketserver.BaseRequestHandler):
    """
    Handler para las conexiones TCP. Recibe una tarea, la envía al pool de procesos
    y devuelve el resultado al Servidor A.
    """
    def handle(self):
        data = receive_data(self.request)
        if not data:
            print("No data received or connection closed.")
            return

        try:
            task = deserialize_data(data)
            url = task.get("url")
            if not url:
                raise ValueError("Task dictionary must contain a 'url' key")

            print(f"Received task for URL: {url}. Submitting to process pool.")
            
            # Envía la tarea al pool de procesos y espera el resultado
            future = PROCESS_POOL.submit(processing_task, url)
            result = future.result()

            send_data(self.request, serialize_data(result))
            print(f"Result for {url} sent back to Server A.")

        except (ValueError) as e:
            print(f"Invalid request received: {e}")
            error_response = {"error": f"Invalid request: {e}", "status": "failed"}
            send_data(self.request, serialize_data(error_response))
        except Exception as e:
            print(f"An unexpected error occurred in the handler: {e}")
            error_response = {"error": f"Unexpected server error: {e}", "status": "failed"}
            send_data(self.request, serialize_data(error_response))

def main():
    global PROCESS_POOL
    
    parser = argparse.ArgumentParser(
        description="Servidor de Procesamiento Distribuido",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha (IPv4 o IPv6)")
    parser.add_argument("-p", "--port", required=True, type=int, help="Puerto de escucha")
    parser.add_argument(
        "-n", "--processes", 
        type=int, 
        default=os.cpu_count(), 
        help="Número de procesos en el pool (default: número de CPUs)"
    )
    args = parser.parse_args()

    # Creamos el pool de procesos que se compartirá entre las peticiones
    with ProcessPoolExecutor(max_workers=args.processes) as pool:
        PROCESS_POOL = pool
        
        # Usamos ThreadingTCPServer para manejar múltiples conexiones simultáneamente.
        # El trabajo pesado real se hace en procesos separados, por lo que no hay GIL-contention.
        with socketserver.ThreadingTCPServer((args.ip, args.port), TCPHandler) as server:
            print(f"Server B (Processing) listening on {args.ip}:{args.port} with {args.processes} worker processes.")
            server.serve_forever()

if __name__ == "__main__":
    main()