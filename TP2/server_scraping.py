import asyncio
from aiohttp import web
import aiohttp
import argparse
import datetime

# Modulos del proyecto
from scraper import async_http, html_parser, metadata_extractor
from common.serialization import serialize_data, deserialize_data

# Esta función es un cliente TCP asíncrono. Se encarga de
# comunicarse con el Servidor B (el de procesamiento).
async def send_task_to_processor(host, port, task):
    """
    Se conecta al servidor de procesamiento, envía una tarea y devuelve el resultado.
    """
    try:
        # `asyncio.open_connection` establece una conexión de forma no bloqueante.
        # El `await` pausa la ejecución de esta función hasta que la conexión se establece.
        reader, writer = await asyncio.open_connection(host, port)

        # Prepara el mensaje usando el mismo protocolo que el Servidor B espera.
        message = serialize_data(task)
        message_len = len(message).to_bytes(4, 'big')

        # Envía los datos.
        writer.write(message_len + message)
        await writer.drain() # Espera a que el buffer de escritura esté vacío.
        print(f"[Cliente TCP] Tarea enviada al procesador: {task}")

        # Recibe la respuesta.
        response_len_raw = await reader.readexactly(4)
        response_len = int.from_bytes(response_len_raw, 'big')
        response_data = await reader.readexactly(response_len)
        result = deserialize_data(response_data)
        
        print(f"[Cliente TCP] Resultado recibido: {result}")

        # Cierra la conexión.
        writer.close()
        await writer.wait_closed()

        return result

    except Exception as e:
        print(f"[ERROR] No se pudo conectar o comunicar con el servidor de procesamiento: {e}")
        return {"status": "error", "reason": str(e)}


async def scrape_url_data(url: str) -> dict:
    """
    Orquesta el proceso de scraping de una URL.
    """
    try:
        # 1. Obtener el HTML de forma asíncrona
        html = await async_http.fetch_html(url)

        # 2. Parsear el HTML para extraer datos básicos y el objeto soup
        parsed_data = html_parser.parse_html_data(html, url)
        soup = parsed_data.pop('soup')  # Extraemos soup para el siguiente paso

        # 3. Extraer metadatos usando el objeto soup
        metadata = metadata_extractor.extract_metadata(soup, url)

        # 4. Consolidar todos los datos extraídos
        return {**parsed_data, **metadata}

    except (aiohttp.ClientError, ValueError) as e:
        print(f"[ERROR] Fallo en el scraping de {url}: {e}")
        return {"status": "error", "reason": str(e)}



# Explicación: El manejador ahora llama a la función de scraping real.
async def scrape_handler(request):
    """
    Manejador para la ruta /scrape. Recibe una URL, coordina el trabajo
    y devuelve el resultado consolidado.
    """
    url = request.query.get('url')
    if not url:
        return web.json_response({"status": "error", "reason": "URL no especificada"}, status=400)

    print(f"[Servidor HTTP] Petición recibida para scrapear: {url}")

    # --- 1. Tareas de Scraping (Servidor A) ---
    # Ahora llamamos a nuestra función de scraping real.
    scraping_data = await scrape_url_data(url)
    # Si el scraping falló, devolvemos el error inmediatamente.
    if scraping_data.get("status") == "error":
        return web.json_response(scraping_data, status=500)
    
    print(f"[Servidor HTTP] Scraping local para {url} completado.")

    # --- 2. Tareas de Procesamiento (Servidor B) ---
    processor_host = request.app['config']['processor_host']
    processor_port = request.app['config']['processor_port']
    
    # Creamos una tarea genérica para el Servidor B, incluyendo las URLs de las imágenes.
    task_for_processor = {
        "url": url,
        "image_urls": scraping_data.get("image_urls", [])
    }
    
    # El Servidor B ahora devuelve un diccionario con todos los datos procesados.
    processing_data = await send_task_to_processor(processor_host, processor_port, task_for_processor)

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
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha del servidor de scraping")
    parser.add_argument("-p", "--port", required=True, type=int, help="Puerto de escucha del servidor de scraping")
    parser.add_argument("--processor-host", required=True, help="Dirección del servidor de procesamiento")
    parser.add_argument("--processor-port", required=True, type=int, help="Puerto del servidor de procesamiento")
    # El enunciado pide -w/--workers, pero aiohttp.web.run_app no lo usa directamente.
    # Se añade por completitud, pero su uso real sería con un runner como Gunicorn.
    parser.add_argument("-w", "--workers", type=int, default=4, help="Número de workers (no usado en modo de desarrollo)")
    
    args = parser.parse_args()

    # Creamos la aplicación de aiohttp
    app = web.Application()
    
    # Guardamos la configuración en la app para que los manejadores puedan accederla.
    app['config'] = {
        'processor_host': args.processor_host,
        'processor_port': args.processor_port
    }

    # Añadimos la ruta y el manejador.
    app.router.add_get('/scrape', scrape_handler)

    print(f"Servidor de Scraping escuchando en http://{args.ip}:{args.port}")
    print(f"Conectándose al Servidor de Procesamiento en {args.processor_host}:{args.processor_port}")

    # Ejecutamos la aplicación.
    web.run_app(app, host=args.ip, port=args.port)

if __name__ == '__main__':
    main()