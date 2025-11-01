import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def analyze(url: str) -> dict:
    """
    Analiza el rendimiento de carga de una URL usando Selenium.
    Calcula el tiempo de carga, el número de solicitudes y el tamaño total de los recursos.

    Args:
        url: La URL de la página a analizar.

    Returns:
        Un diccionario con las métricas de rendimiento.
    
    Raises:
        WebDriverException: Si ocurre un problema con el driver de Selenium.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30) # Timeout de 30 segundos para la carga

        print(f"[Performance] Navegando a {url} para análisis de rendimiento...")
        driver.get(url)

        # --- Obtener métricas de rendimiento --- 
        # Usamos Navigation Timing API
        navigation_timing = driver.execute_script("return window.performance.timing")
        
        load_time_ms = 0
        if navigation_timing:
            # loadEventEnd - navigationStart da el tiempo total de carga de la página
            load_time_ms = navigation_timing['loadEventEnd'] - navigation_timing['navigationStart']
            if load_time_ms < 0: # Puede ser negativo si los eventos no se disparan en orden esperado
                load_time_ms = 0

        # Usamos Resource Timing API para el número de requests y tamaño total
        resource_entries = driver.execute_script("return window.performance.getEntriesByType('resource')")
        
        num_requests = len(resource_entries) + 1 # +1 para la solicitud del documento principal
        total_size_bytes = 0
        for entry in resource_entries:
            # transferSize incluye el tamaño de la cabecera y el cuerpo, si está disponible
            # decodedBodySize es el tamaño del cuerpo después de la decodificación de contenido
            if 'transferSize' in entry and entry['transferSize'] > 0:
                total_size_bytes += entry['transferSize']
            elif 'decodedBodySize' in entry and entry['decodedBodySize'] > 0:
                total_size_bytes += entry['decodedBodySize']
            # Si no hay información de tamaño, podríamos estimar o ignorar

        total_size_kb = total_size_bytes / 1024

        print(f"[Performance] Análisis para {url} completado.")
        return {
            "load_time_ms": round(load_time_ms),
            "total_size_kb": round(total_size_kb, 2),
            "num_requests": num_requests
        }

    except WebDriverException as e:
        print(f"[ERROR][Performance] Ocurrió un error con Selenium para la URL {url}: {e}")
        raise
    except Exception as e:
        print(f"[ERROR][Performance] Error inesperado para {url}: {e}")
        raise
    finally:
        if driver:
            driver.quit()