import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def take(url: str) -> bytes:
    """
    Navega a una URL usando Selenium con Chrome y toma una captura de pantalla.
    La imagen se guarda en el directorio 'imagenes' y luego se devuelve como bytes.

    Args:
        url: La URL de la página a capturar.

    Returns:
        Los bytes de la imagen en formato PNG.
    
    Raises:
        WebDriverException: Si ocurre un problema con el driver de Selenium.
        IOError: Si hay un problema al guardar o leer el archivo de imagen.
    """
    # --- Configuración de Selenium ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # Tamaño de ventana para la captura

    driver = None
    try:
        # --- Inicialización del WebDriver ---
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30) # Timeout de 30 segundos para la carga

        # --- Navegación y Captura ---
        print(f"[Screenshot] Navegando a {url} para captura...")
        driver.get(url)
        
        # --- Generación de Nombre de Archivo ---
        # Limpiamos la URL para crear un nombre de archivo seguro
        safe_filename = re.sub(r'https://?|www\.', '', url)
        safe_filename = re.sub(r'[\/:*?"<>|]', '_', safe_filename)
        # Nos aseguramos de que el nombre no sea demasiado largo
        safe_filename = (safe_filename[:100] + '..') if len(safe_filename) > 100 else safe_filename
        
        # --- Guardado de la Imagen ---
        output_dir = '/home/martinsalvatore/repos/python/computacionII/TP2/imagenes'
        os.makedirs(output_dir, exist_ok=True) # Asegura que el directorio exista
        
        screenshot_path = os.path.join(output_dir, f"{safe_filename}.png")
        
        print(f"[Screenshot] Guardando captura en: {screenshot_path}")
        driver.save_screenshot(screenshot_path)
        
        # --- Lectura y Retorno de los Bytes ---
        with open(screenshot_path, 'rb') as f:
            screenshot_bytes = f.read()
        
        print(f"[Screenshot] Captura para {url} completada y leída.")
        return screenshot_bytes

    except WebDriverException as e:
        print(f"[ERROR][Screenshot] Ocurrió un error con Selenium para la URL {url}: {e}")
        # En caso de error, devolvemos una imagen vacía o placeholder si es necesario.
        # Por ahora, relanzamos para que el manejador superior lo capture.
        raise
    except IOError as e:
        print(f"[ERROR][Screenshot] Ocurrió un error de I/O al manejar el archivo de captura: {e}")
        raise
    finally:
        # --- Limpieza ---
        if driver:
            driver.quit()