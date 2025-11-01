from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_html_data(html: str, base_url: str) -> dict:
    """
    Parsea el contenido HTML para extraer datos estructurales y de contenido.

    Args:
        html: El contenido HTML de la página.
        base_url: La URL base para resolver las URLs relativas.

    Returns:
        Un diccionario con el título, enlaces, contador de imágenes y estructura.
    """
    soup = BeautifulSoup(html, 'lxml')

    title = soup.title.string.strip() if soup.title else "Sin título"

    links = sorted(list(set(
        urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)
    )))

    images_count = len(soup.find_all('img'))

    structure = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}

    return {
        "title": title,
        "links": links,
        "images_count": images_count,
        "structure": structure,
        "soup": soup  # Devolvemos el objeto soup para no tener que parsear de nuevo
    }
