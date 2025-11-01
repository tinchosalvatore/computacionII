import base64
import io
import requests
from PIL import Image, UnidentifiedImageError
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_image_urls(url: str) -> list:
    """
    Obtiene las URLs de las imágenes de una página.
    
    Args:
        url: La URL de la página.
        
    Returns:
        Lista de URLs de imágenes encontradas.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        img_urls = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # Ignorar imágenes data: que son muy comunes
                if not src.startswith('data:'):
                    img_urls.append(urljoin(url, src))
        
        return img_urls
    except requests.RequestException as e:
        print(f"[ImageProcessor] Could not fetch image URLs from {url}: {e}")
        return []

def process(url: str) -> list:
    """
    Extrae, descarga y crea thumbnails de las imágenes principales de una URL.

    Args:
        url: La URL de la página a procesar.

    Returns:
        Una lista de strings base64 representando los thumbnails.
    """
    image_urls = get_image_urls(url)
    if not image_urls:
        print(f"[ImageProcessor] No se encontraron imágenes en {url}")
        return []

    images_data = []
    # Limitamos el análisis a las primeras 20 imágenes para ser eficientes.
    for img_url in image_urls[:20]:
        try:
            # Descargamos la imagen con un timeout corto.
            img_response = requests.get(img_url, timeout=5)
            img_response.raise_for_status()
            img_data = img_response.content
            
            # Usamos Pillow para verificar que es una imagen válida y obtener su tamaño
            with Image.open(io.BytesIO(img_data)) as img:
                width, height = img.size
                # Solo consideramos imágenes con un tamaño mínimo para evitar iconos.
                if width > 100 and height > 100:
                    images_data.append({
                        "area": width * height,
                        "data": img_data
                    })
        except (requests.RequestException, IOError, UnidentifiedImageError) as e:
            # Ignoramos imágenes que no se pueden descargar o procesar.
            # print(f"[ImageProcessor] Skipping image {img_url}: {e}")
            continue

    if not images_data:
        print(f"[ImageProcessor] No se encontraron imágenes válidas (>100x100) en {url}")
        return []

    # Ordenamos las imágenes por área (de mayor a menor) y tomamos las 3 principales.
    images_data.sort(key=lambda x: x['area'], reverse=True)
    main_images_data = [img['data'] for img in images_data[:3]]

    thumbnails_base64 = []
    for img_data in main_images_data:
        try:
            with Image.open(io.BytesIO(img_data)) as img:
                # Generamos un thumbnail de 128x128 manteniendo el aspect ratio.
                img.thumbnail((128, 128))
                
                thumb_buffer = io.BytesIO()
                img.save(thumb_buffer, format="PNG")
                thumb_bytes = thumb_buffer.getvalue()
                
                base64_thumb = base64.b64encode(thumb_bytes).decode('utf-8')
                thumbnails_base64.append(base64_thumb)
        except (IOError, UnidentifiedImageError) as e:
            print(f"[ImageProcessor] Could not create thumbnail: {e}")
            continue
    
    print(f"[ImageProcessor] Generados {len(thumbnails_base64)} thumbnails para {url}")
    return thumbnails_base64