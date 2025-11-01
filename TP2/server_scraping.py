import asyncio
from aiohttp import web
import aiohttp
import argparse
import datetime
from collections import defaultdict
import time

# Modulos del proyecto
from scraper import async_http, html_parser, metadata_extractor
from common.serialization import serialize_data, deserialize_data

# Rate limiting por dominio (Requisito del enunciado)
class RateLimiter:
    """
    Implementa rate limiting por dominio para evitar sobrecargar sitios web.
    Límite: max_requests solicitudes por window_seconds segundos.
    """
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # dominio -> [timestamps]
        self.lock = asyncio.Lock()
    
    async def acquire(self, domain):
        """Espera hasta que se pueda hacer una request a este dominio."""
        async with self.lock:
            now = time.time()
            # Limpiar requests antiguas
            self.requests[domain] = [
                ts for ts in self.requests[domain] 
                if now - ts < self.window_seconds
            ]
            
            # Si estamos en el límite, esperar
            if len(self.requests[domain]) >= self.max_requests:
                oldest = self.requests[domain][0]
                wait_time = self.window_seconds - (now - oldest)
                if wait_time > 0:
                    print(f"[RateLimiter] Esperando {wait_time:.2f}s para {domain}")
                    await asyncio.sleep(wait_time)
                    # Re-limpiar después de esperar
                    now = time.time()
                    self.requests[domain] = [
                        ts for ts in self.requests[domain] 
                        if now - ts < self.window_seconds
                    ]
            
            # Registrar esta request
            self.requests[domain].append(now)

# Cliente TCP asíncrono para comunicarse con el Servidor B
async def send_task_to_processor(host, port, task):
    """
    Se conecta al servidor de procesamiento, envía una tarea y devuelve el resultado.
    """
    try:
        # `asyncio.open_connection` establece una conexión de forma no bloqueante.
        reader, writer = await asyncio.open_connection(host, port)

        # Prepara el mensaje usando el mismo protocolo que el Servidor B espera.
        message = serialize_data(task)
        message_len = len(message).to_bytes(4, 'big')

        # Envía los datos.
        writer.write(message_len + message)
        await writer.drain()
        print(f"[Cliente TCP] Tarea enviada al procesador para URL: {task.get('url')}")

        # Recibe la respuesta con timeout
        try:
            response_len_raw = await asyncio.wait_for(reader.readexactly(4), timeout=120)
            response_len = int.from_bytes(response_len_raw, 'big')
            response_data = await asyncio.wait_for(reader.readexactly(response_len), timeout=120)
            result = deserialize_data(response_data)
            
            print(f"[Cliente TCP] Resultado recibido del procesador")
        except asyncio.TimeoutError:
            print(f"[ERROR] Timeout esperando respuesta del servidor de procesamiento")
            return {"status": "error", "reason": "Timeout del servidor de procesamiento"}

        # Cierra la conexión.
        writer.close()
        await writer.wait_closed()

        return result

    except Exception as e:
        print(f"[ERROR] No se pudo conectar o comunicar con el servidor de procesamiento: {e}")
        return {"status": "error", "reason": str(e)}


async def scrape_url_data(url: str, rate_limiter: RateLimiter) -> dict:
    """
    Orquesta el proceso de scraping de una URL con rate limiting.
    
    Args:
        url: La URL a scrapear
        rate_limiter: Instancia del rate limiter para controlar requests por dominio
    """
    try:
        # Extraer dominio para rate limiting
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        # Aplicar rate limiting
        await rate_limiter.acquire(domain)
        
        # 1. Obtener el HTML de forma asíncrona con timeout de 30s (requisito)
        html = await asyncio.wait_for(async_http.fetch_html(url), timeout=30)

        # 2. Parsear el HTML para extraer datos básicos y el objeto soup
        parsed_data = html_parser.parse_html_data(html, url)
        soup = parsed_data.pop('soup')  # Extraemos soup para el siguiente paso

        # 3. Extraer metadatos usando el objeto soup
        metadata = metadata_extractor.extract_metadata(soup, url)

        # 4. Consolidar todos los datos extraídos
        return {**parsed_data, **metadata}

    except asyncio.TimeoutError:
        print(f"[ERROR] Timeout (30s) al scrapear {url}")
        return {"status": "error", "reason": "Timeout al cargar la página (30s)"}
    except (aiohttp.ClientError, ValueError) as e:
        print(f"[ERROR] Fallo en el scraping de {url}: {e}")
        return {"status": "error", "reason": str(e)}


async def scrape_handler(request):
    """
    Manejador para la ruta /scrape. Recibe una URL, coordina el trabajo
    y devuelve el resultado consolidado.
    """
    url = request.query.get('url')
    if not url:
        return web.json_response(
            {"status": "error", "reason": "URL no especificada"}, 
            status=400
        )

    print(f"[Servidor HTTP] Petición recibida para scrapear: {url}")

    # --- 1. Tareas de Scraping (Servidor A) ---
    rate_limiter = request.app['rate_limiter']
    scraping_data = await scrape_url_data(url, rate_limiter)
    
    # Si el scraping falló, devolvemos el error inmediatamente.
    if scraping_data.get("status") == "error":
        return web.json_response(scraping_data, status=500)
    
    print(f"[Servidor HTTP] Scraping local para {url} completado.")

    # --- 2. Tareas de Procesamiento (Servidor B) ---
    processor_host = request.app['config']['processor_host']
    processor_port = request.app['config']['processor_port']
    
    # Creamos una tarea para el Servidor B con la URL
    task_for_processor = {
        "url": url,
        "image_urls": scraping_data.get("image_urls", [])
    }
    
    # Comunicación con Servidor B
    processing_data = await send_task_to_processor(
        processor_host, 
        processor_port, 
        task_for_processor
    )

    # --- 3. Consolidar y Responder ---
    final_response = {
        "url": url,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "scraping_data": scraping_data,
        "processing_data": processing_data,
        "status": "success"
    }

    return web.json_response(final_response)

def main():
    parser = argparse.ArgumentParser(
        description="Servidor de Scraping Web Asíncrono",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--ip", 
        required=True, 
        help="Dirección de escucha (soporta IPv4/IPv6)"
    )
    parser.add_argument(
        "-p", "--port", 
        required=True, 
        type=int, 
        help="Puerto de escucha"
    )
    parser.add_argument(
        "--processor-host", 
        required=True, 
        help="Dirección del servidor de procesamiento"
    )
    parser.add_argument(
        "--processor-port", 
        required=True, 
        type=int, 
        help="Puerto del servidor de procesamiento"
    )
    parser.add_argument(
        "-w", "--workers", 
        type=int, 
        default=4, 
        help="Número de workers (default: 4)"
    )
    
    args = parser.parse_args()

    # Creamos la aplicación de aiohttp
    app = web.Application()
    
    # Guardamos la configuración en la app
    app['config'] = {
        'processor_host': args.processor_host,
        'processor_port': args.processor_port,
        'workers': args.workers
    }
    
    # Inicializamos el rate limiter (10 requests por minuto por dominio)
    app['rate_limiter'] = RateLimiter(max_requests=10, window_seconds=60)

    # Añadimos la ruta y el manejador.
    app.router.add_get('/scrape', scrape_handler)

    print(f"Servidor de Scraping escuchando en http://{args.ip}:{args.port}")
    print(f"Conectándose al Servidor de Procesamiento en {args.processor_host}:{args.processor_port}")
    print(f"Workers configurados: {args.workers}")
    print(f"Rate limiting: 10 requests/minuto por dominio")

    # Ejecutamos la aplicación (soporta IPv4 e IPv6 automáticamente)
    web.run_app(app, host=args.ip, port=args.port)

if __name__ == '__main__':
    main()