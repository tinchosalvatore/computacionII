import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from aiohttp import web

# Importamos el manejador y la aplicación a testear
from server_scraping import scrape_handler, main

@pytest_asyncio.fixture
async def cli(aiohttp_client):
    """
    Fixture para crear un cliente de prueba para la aplicación aiohttp.
    """
    app = web.Application()
    app.router.add_get('/scrape', scrape_handler)

    # Mock de la configuración que normalmente se añade en main()
    app['config'] = {
        'processor_host': 'localhost',
        'processor_port': 9000
    }
    
    return await aiohttp_client(app)

@pytest.mark.asyncio
async def test_scrape_handler_success(cli):
    """
    Test para el manejador /scrape en un caso de éxito.
    """
    # Mockeamos la función que se comunica con el Servidor B
    # para que devuelva un resultado exitoso simulado.
    with patch('server_scraping.send_task_to_processor', new_callable=AsyncMock) as mock_send_task:
        mock_send_task.return_value = {
            "status": "success",
            "screenshot": "fake_base64_screenshot",
            "performance": {"load_time_ms": 100},
            "thumbnails": []
        }

        # Usamos una URL real y simple para el test
        url_to_scrape = "http://info.cern.ch/"
        resp = await cli.get(f'/scrape?url={url_to_scrape}')

        assert resp.status == 200
        data = await resp.json()

        # Verificaciones de la estructura de la respuesta
        assert data['status'] == 'success'
        assert data['url'] == url_to_scrape
        assert 'timestamp' in data

        # Verificaciones de los datos de scraping
        assert 'scraping_data' in data
        scraping_data = data['scraping_data']
        assert 'title' in scraping_data
        assert 'links' in scraping_data
        assert 'meta_tags' in scraping_data
        assert 'images_count' in scraping_data
        assert 'structure' in scraping_data

        # Verificaciones de los datos de procesamiento (mockeados)
        assert 'processing_data' in data
        assert data['processing_data']['status'] == 'success'

@pytest.mark.asyncio
async def test_scrape_handler_missing_url(cli):
    """
    Test para el caso en que no se proporciona una URL.
    """
    resp = await cli.get('/scrape')
    assert resp.status == 400
    data = await resp.json()
    assert data['status'] == 'error'
    assert 'URL no especificada' in data['reason']

@pytest.mark.asyncio
async def test_scrape_handler_invalid_url(cli):
    """
    Test para el caso de una URL inválida o inaccesible.
    """
    # Usamos una URL que sabemos que fallará la conexión
    url_to_scrape = "http://localhost:9999/nonexistent"
    resp = await cli.get(f'/scrape?url={url_to_scrape}')
    
    assert resp.status == 500
    data = await resp.json()
    assert data['status'] == 'error'
    assert 'reason' in data
