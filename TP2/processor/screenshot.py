from playwright.sync_api import sync_playwright, Error
import base64

def take(url: str) -> bytes:
    """
    Navega a una URL usando Playwright y toma una captura de pantalla.

    Args:
        url: La URL de la página a capturar.

    Returns:
        Los bytes de la imagen en formato PNG.
    
    Raises:
        Error: Si ocurre un problema durante la captura (ej. timeout).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Navegamos a la URL con un timeout de 30s y esperamos a que la página esté cargada.
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Tomamos la captura en formato PNG y la devolvemos directamente.
            screenshot_bytes = page.screenshot(type='png')
            
            return screenshot_bytes
        finally:
            # Nos aseguramos de cerrar el navegador siempre.
            browser.close()
