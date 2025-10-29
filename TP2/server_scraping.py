
import asyncio
from aiohttp import web
import aiohttp
import argparse
import json
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Explicación: Esta función es un cliente TCP asíncrono. Se encarga de
# comunicarse con el Servidor B (el de procesamiento).
async def send_task_to_processor(host, port, task):
    """
    Se conecta al servidor de procesamiento, envía una tarea y devuelve el resultado.
    """
    try:
        # Explicación: `asyncio.open_connection` establece una conexión de forma no bloqueante.
        # El `await` pausa la ejecución de esta función hasta que la conexión se establece.
        reader, writer = await asyncio.open_connection(host, port)

        # Prepara el mensaje usando el mismo protocolo que el Servidor B espera.
        message = json.dumps(task).encode('utf-8')
        message_len = len(message).to_bytes(4, 'big')

        # Envía los datos.
        writer.write(message_len + message)
        await writer.drain() # Espera a que el buffer de escritura esté vacío.
        print(f"[Cliente TCP] Tarea enviada al procesador: {task}")

        # Recibe la respuesta.
        response_len_raw = await reader.readexactly(4)
        response_len = int.from_bytes(response_len_raw, 'big')
        response_data = await reader.readexactly(response_len)
        result = json.loads(response_data.decode('utf-8'))
        
        print(f"[Cliente TCP] Resultado recibido: {result}")

        # Cierra la conexión.
        writer.close()
        await writer.wait_closed()

        return result

    except Exception as e:
        print(f"[ERROR] No se pudo conectar o comunicar con el servidor de procesamiento: {e}")
        return {"status": "error", "reason": str(e)}

# Explicación: Esta nueva función contiene la lógica de scraping real.
# Es asíncrona porque realiza una petición HTTP de red.
async def scrape_url_data(url):
    """
    Realiza el scraping de una URL para extraer título, links, metas, etc.
    """
    # Explicación: aiohttp.ClientSession() es la forma recomendada de realizar
    # peticiones. Usar `async with` asegura que la sesión se cierre correctamente.
    async with aiohttp.ClientSession() as session:
        try:
            # Realizamos la petición GET de forma asíncrona con un timeout de 30s.
            async with session.get(url, timeout=30) as response:
                response.raise_for_status() # Lanza un error si el status es 4xx o 5xx

                # Verificamos que el contenido sea HTML antes de intentar parsearlo.
                if 'text/html' not in response.content_type:
                    reason = f"Content-Type no soportado: {response.content_type}"
                    print(f"[ERROR] {reason} para la URL {url}")
                    return {"status": "error", "reason": reason}

                html = await response.text()
        except Exception as e:
            print(f"[ERROR] No se pudo obtener el contenido de {url}: {e}")
            # Devolvemos un diccionario con un estado de error claro.
            return {"status": "error", "reason": f"No se pudo acceder a la URL: {e}"}

    # Usamos BeautifulSoup para parsear el HTML. 'lxml' es un parser rápido.
    soup = BeautifulSoup(html, 'lxml')

    # --- Extracción de datos ---
    title = soup.title.string.strip() if soup.title else "Sin título"

    # Extraemos todos los links, los convertimos a absolutos y eliminamos duplicados.
    links = sorted(list(set(
        urljoin(url, a['href']) for a in soup.find_all('a', href=True)
    )))

    # Extraemos meta tags relevantes (name y property) que tengan contenido.
    meta_tags = {
        meta.get('name', meta.get('property', 'unknown')): meta.get('content', '')
        for meta in soup.find_all('meta')
        if meta.get('content') and (meta.get('name') in ['description', 'keywords'] or meta.get('property', '').startswith('og:'))
    }

    images_count = len(soup.find_all('img'))

    # Contamos las etiquetas de encabezado de H1 a H6.
    structure = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}

    # Extraemos las URLs de todas las imágenes para análisis posterior.
    image_urls = sorted(list(set(
        urljoin(url, img['src']) for img in soup.find_all('img', src=True)
    )))

    return {
        "title": title,
        "links": links,
        "meta_tags": meta_tags,
        "images_count": images_count,
        "structure": structure,
        "image_urls": image_urls
    }

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
