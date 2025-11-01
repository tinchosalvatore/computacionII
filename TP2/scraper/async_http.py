import aiohttp

async def fetch_html(url: str) -> str:
    """
    Realiza una petición GET asíncrona a una URL y devuelve el contenido HTML.

    Args:
        url: La URL a la que se hará la petición.

    Returns:
        El contenido HTML de la página como una cadena.

    Raises:
        aiohttp.ClientError: Si ocurre un error durante la petición HTTP.
        ValueError: Si el tipo de contenido no es HTML.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=30) as response:
                response.raise_for_status()

                if 'text/html' not in response.content_type:
                    raise ValueError(f"El contenido no es HTML: {response.content_type}")

                return await response.text()
        except aiohttp.ClientError as e:
            print(f"[ERROR] No se pudo obtener el contenido de {url}: {e}")
            raise
