import pytest
from unittest.mock import patch
import base64

# Importamos la función a testear
from server_processing import processing_task

@patch('processor.image_processor.process')
@patch('processor.performance.analyze')
@patch('processor.screenshot.take')
def test_processing_task_success(mock_screenshot_take, mock_performance_analyze, mock_image_process):
    """
    Test para la función processing_task en un caso de éxito.
    """
    # --- Configuración de los Mocks ---
    # Mock de screenshot.take para que devuelva unos bytes de imagen falsos
    fake_screenshot_bytes = b'fake_image_data'
    mock_screenshot_take.return_value = fake_screenshot_bytes
    expected_screenshot_base64 = base64.b64encode(fake_screenshot_bytes).decode('utf-8')

    # Mock de performance.analyze para que devuelva datos de rendimiento simulados
    mock_performance_analyze.return_value = {"load_time_ms": 250, "total_size_kb": 1024}

    # Mock de image_processor.process para que devuelva una lista de thumbnails simulada
    mock_image_process.return_value = ["thumb1_base64", "thumb2_base64"]

    # --- Ejecución de la función a testear ---
    url = "https://example.com"
    result = processing_task(url)

    # --- Verificaciones ---
    # Asegurarnos de que las funciones mockeadas fueron llamadas con la URL correcta
    mock_screenshot_take.assert_called_once_with(url)
    mock_performance_analyze.assert_called_once_with(url)
    mock_image_process.assert_called_once_with(url)

    # Verificar que el resultado tiene la estructura y contenido esperados
    assert result['status'] == 'success'
    assert result['screenshot'] == expected_screenshot_base64
    assert result['performance'] == {"load_time_ms": 250, "total_size_kb": 1024}
    assert result['thumbnails'] == ["thumb1_base64", "thumb2_base64"]

@patch('processor.screenshot.take', side_effect=Exception("Screenshot failed"))
def test_processing_task_failure(mock_screenshot_take):
    """
    Test para la función processing_task cuando una de las subtareas falla.
    """
    url = "https://example.com"
    result = processing_task(url)

    # Verificar que el resultado refleje el fallo
    assert result['status'] == 'failed'
    assert 'error' in result
    assert "Screenshot failed" in result['error']
