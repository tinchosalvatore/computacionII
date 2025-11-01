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
    # Timeout de 30 segundos según el enunciado
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url, allow_redirects=True) as response:
                response.raise_for_status()

                # Verificar que el contenido es HTML
                content_type = response.content_type
                if 'text/html' not in content_type and 'application/xhtml+xml' not in content_type:
                    raise ValueError(f"El contenido no es HTML: {content_type}")

                return await response.text()
                
        except aiohttp.ClientError as e:
            print(f"[ERROR] No se pudo obtener el contenido de {url}: {e}")
            raise
        except asyncio.TimeoutError:
            print(f"[ERROR] Timeout al intentar acceder a {url}")
            raise aiohttp.ClientError(f"Timeout al cargar {url}")