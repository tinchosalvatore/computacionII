import base64
import urllib.request
from PIL import Image
import io

def process_images(image_urls: list) -> dict:
    """
    Descarga un número limitado de imágenes de una lista, selecciona las más
    grandes por área y genera thumbnails codificados en Base64.
    """
    if not image_urls:
        return {"status": "success", "thumbnails": []}

    images_with_dims = []
    # Limitamos el análisis a las primeras 10 imágenes para ser eficientes.
    for url in image_urls[:10]:
        try:
            # Descargamos la imagen con un timeout corto.
            with urllib.request.urlopen(url, timeout=5) as response:
                img_data = response.read()
                img = Image.open(io.BytesIO(img_data))
                width, height = img.size
                # Solo consideramos imágenes con un tamaño mínimo para evitar iconos pequeños.
                if width > 100 and height > 100:
                    images_with_dims.append({
                        "area": width * height,
                        "data": img_data
                    })
        except Exception:
            # Ignoramos imágenes que no se pueden descargar, abrir o no cumplen el tamaño.
            continue

    # Ordenamos las imágenes por área (de mayor a menor) y tomamos las 3 principales.
    images_with_dims.sort(key=lambda x: x['area'], reverse=True)
    main_images_data = [img['data'] for img in images_with_dims[:3]]

    thumbnails_base64 = []
    for img_data in main_images_data:
        try:
            img = Image.open(io.BytesIO(img_data))
            # Generamos un thumbnail de 128x128 manteniendo el aspect ratio.
            img.thumbnail((128, 128))
            
            # Guardamos el thumbnail en un buffer en memoria en formato PNG.
            thumb_buffer = io.BytesIO()
            img.save(thumb_buffer, format="PNG")
            thumb_bytes = thumb_buffer.getvalue()
            
            # Codificamos a Base64 para el JSON.
            base64_thumb = base64.b64encode(thumb_bytes).decode('utf-8')
            thumbnails_base64.append(base64_thumb)
        except Exception:
            # Si falla la creación del thumbnail, simplemente la omitimos.
            continue
            
    return {"status": "success", "thumbnails": thumbnails_base64}
