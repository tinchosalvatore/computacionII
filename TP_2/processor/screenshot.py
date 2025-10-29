from playwright.sync_api import sync_playwright, Error
import base64

def take_screenshot(url: str) -> dict:
    """
    Navega a una URL usando Playwright y toma una captura de pantalla.

    Args:
        url: La URL de la página a capturar.

    Returns:
        Un diccionario con el estado y la imagen en base64 o un mensaje de error.
    """
    try:
        with sync_playwright() as p:
            # Lanzamos un navegador Chromium en modo headless (sin interfaz gráfica).
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navegamos a la URL con un timeout de 30s y esperamos a que la página esté cargada.
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Tomamos la captura en formato PNG, como pide el enunciado.
            screenshot_bytes = page.screenshot(type='png')
            
            browser.close()
            
            # Codificamos los bytes de la imagen en Base64 (formato texto).
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # El enunciado espera un campo "screenshot" con la imagen.
            return {"status": "success", "screenshot": base64_image}

    except Error as e:
        # Capturamos errores específicos de Playwright (ej. TimeoutError).
        print(f"[ERROR Screenshot] No se pudo tomar la captura para {url}: {e}")
        return {"status": "error", "reason": f"Error de Playwright: {e}"}
    except Exception as e:
        # Capturamos cualquier otro error inesperado.
        print(f"[ERROR Screenshot] Error inesperado para {url}: {e}")
        return {"status": "error", "reason": f"Error inesperado: {e}"}
