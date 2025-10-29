from playwright.sync_api import sync_playwright, Error
import json
import os
import tempfile
import uuid

def analyze_performance(url: str) -> dict:
    """
    Analiza el rendimiento de carga de una URL usando la grabación de archivos HAR de Playwright.
    """
    # Creamos una ruta de archivo temporal única para guardar los datos HAR.
    har_path = os.path.join(tempfile.gettempdir(), f"perf_{uuid.uuid4()}.har")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Creamos un nuevo "contexto" de navegador con la grabación HAR habilitada.
            context = browser.new_context(record_har_path=har_path)
            page = context.new_page()

            page.goto(url, wait_until='load', timeout=30000)
            
            # Es crucial cerrar el contexto para que Playwright escriba el archivo HAR en disco.
            context.close()
            browser.close()

        # Una vez cerrado el contexto, leemos y procesamos el archivo HAR.
        with open(har_path, 'r', encoding='utf-8') as f:
            har_data = json.load(f)

        # Extraemos las métricas del log del archivo HAR.
        entries = har_data['log']['entries']
        num_requests = len(entries)
        # `bodySize` es el tamaño del cuerpo de la respuesta en bytes. -1 si no aplica.
        total_size_bytes = sum(entry['response']['bodySize'] for entry in entries if entry['response']['bodySize'] > -1)
        total_size_kb = total_size_bytes / 1024

        # El tiempo de carga se obtiene de los timings de la página en el HAR.
        page_timings = har_data['log']['pages'][0]['pageTimings']
        # `onLoad` es el tiempo en ms hasta que se dispara el evento `load` de la página.
        load_time_ms = page_timings.get('onLoad', 0)

        return {
            "status": "success",
            "performance": {
                "load_time_ms": round(load_time_ms),
                "num_requests": num_requests,
                "total_size_kb": round(total_size_kb, 2)
            }
        }

    except Error as e:
        print(f"[ERROR Performance] No se pudo analizar {url}: {e}")
        return {"status": "error", "reason": f"Error de Playwright: {e}"}
    except Exception as e:
        print(f"[ERROR Performance] Error inesperado para {url}: {e}")
        return {"status": "error", "reason": f"Error inesperado: {e}"}
    finally:
        # Nos aseguramos de limpiar el archivo temporal HAR sin importar lo que pase.
        if os.path.exists(har_path):
            os.remove(har_path)
