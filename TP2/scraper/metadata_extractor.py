from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_metadata(soup: BeautifulSoup, base_url: str) -> dict:
    """
    Extrae metadatos (meta tags, URLs de imágenes) de un objeto BeautifulSoup.

    Args:
        soup: El objeto BeautifulSoup parseado de la página.
        base_url: La URL base para resolver las URLs relativas de las imágenes.

    Returns:
        Un diccionario conteniendo los meta tags y las URLs de las imágenes.
    """
    # Extraemos meta tags relevantes (description, keywords, Open Graph)
    meta_tags = {
        meta.get('name', meta.get('property', 'unknown')): meta.get('content', '')
        for meta in soup.find_all('meta')
        if meta.get('content') and (
            meta.get('name') in ['description', 'keywords'] or 
            meta.get('property', '').startswith('og:')
        )
    }

    # Extraemos las URLs de todas las imágenes para su posterior análisis
    image_urls = sorted(list(set(
        urljoin(base_url, img['src']) for img in soup.find_all('img', src=True)
    )))

    return {
        "meta_tags": meta_tags,
        "image_urls": image_urls
    }
