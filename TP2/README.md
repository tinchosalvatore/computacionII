# TP2 - Sistema de Scraping y Análisis Web Distribuido

Este proyecto implementa un sistema distribuido para el scraping y análisis de páginas web. El sistema está compuesto por dos servidores que trabajan de forma coordinada para procesar solicitudes de manera eficiente, separando las tareas de red (I/O-bound) de las tareas de procesamiento intensivo (CPU-bound).

## Arquitectura del Sistema

La arquitectura se basa en un modelo de dos servidores desacoplados con responsabilidades bien definidas:

### Servidor A: Frontend de Scraping (`server_scraping.py`)
- **Rol**: Actúa como el punto de entrada para el cliente. Recibe peticiones HTTP con la URL a analizar.
- **Tareas**: 
  - Realiza scraping inicial y ligero de la página (título, links, meta tags, estructura)
  - Implementa rate limiting por dominio (10 requests/minuto)
  - Coordina con el Servidor B para análisis pesados
  - Maneja timeouts de 30 segundos por página (requisito del enunciado)
- **Tecnología**: Construido con `asyncio` y `aiohttp` para manejar un gran número de conexiones concurrentes de forma no bloqueante, ideal para tareas de red.

### Servidor B: Backend de Procesamiento (`server_processing.py`)
- **Rol**: Funciona como un "worker" de tareas pesadas. No tiene contacto directo con el cliente.
- **Tareas**: Ejecuta operaciones que consumen CPU:
  - Renderización de páginas para capturas de pantalla
  - Análisis de rendimiento de carga (tiempo, tamaño, número de requests)
  - Procesamiento de imágenes (descarga y generación de thumbnails)
- **Tecnología**: Construido con `socketserver` y `multiprocessing`. Utiliza un `ProcessPoolExecutor` para distribuir el trabajo entre múltiples procesos, aprovechando al máximo los núcleos del CPU.

### Comunicación
Ambos servidores se comunican a través de sockets TCP con un protocolo de longitud prefijada:
- 4 bytes para la longitud del mensaje (big-endian)
- N bytes para el mensaje serializado en JSON
- El Servidor A actúa como cliente del Servidor B
- Comunicación asíncrona para no bloquear el event loop

## Tecnologías Utilizadas

- **`aiohttp`**: Framework base para el servidor web asíncrono (Servidor A).
- **`asyncio`**: Utilizado para gestionar el event loop y las operaciones de red no bloqueantes en el Servidor A.
- **`multiprocessing`**: Permite la ejecución de tareas en paralelo en el Servidor B, evitando que las operaciones CPU-bound bloqueen el sistema.
- **`socketserver`**: Proporciona la estructura para el servidor TCP del Servidor B.
- **`BeautifulSoup4`**: Librería principal para el parseo de HTML y la extracción de datos en el Servidor A.
- **`Selenium`**: Herramienta de automatización de navegadores utilizada en el Servidor B para:
    - Tomar capturas de pantalla de las páginas web.
    - Realizar análisis de rendimiento de carga usando Navigation Timing API.
- **`Pillow`**: Librería para el procesamiento de imágenes, utilizada para crear los thumbnails en el Servidor B.
- **`requests`**: Utilizado en el procesamiento de imágenes y en `client.py`.

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo.

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd TP2
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar ChromeDriver:**
    - Descarga ChromeDriver compatible con tu versión de Chrome desde https://chromedriver.chromium.org/
    - Asegúrate de que esté en tu PATH o especifica la ruta en el código
    - Alternativamente, instala con: `pip install webdriver-manager`

## Antes de Ejecutar

- Asegúrate de haber activado tu entorno virtual (`venv`)
- Instala todas las dependencias (`pip install -r requirements.txt`)
- Verifica que ChromeDriver esté instalado y accesible
- El sistema creará automáticamente los directorios necesarios (`screenshots/`, `results/`)

## Ejecución

El sistema requiere que ambos servidores se ejecuten de forma simultánea en terminales separadas.

### 1. Iniciar Servidor de Procesamiento (Servidor B)
En una primera terminal, ejecuta:
```bash
python3 server_processing.py -i 0.0.0.0 -p 9000 -n 4
```

**Parámetros:**
- `-i, --ip`: Dirección de escucha (0.0.0.0 para todas las interfaces)
- `-p, --port`: Puerto de escucha
- `-n, --processes`: Número de procesos en el pool (default: número de CPUs)

### 2. Iniciar Servidor de Scraping (Servidor A)
En una segunda terminal, ejecuta:
```bash
python3 server_scraping.py -i 0.0.0.0 -p 8000 -w 4 --processor-host 0.0.0.0 --processor-port 9000
```

**Parámetros:**
- `-i, --ip`: Dirección de escucha (soporta IPv4 e IPv6)
- `-p, --port`: Puerto de escucha
- `-w, --workers`: Número de workers (default: 4)
- `--processor-host`: Dirección del servidor de procesamiento
- `--processor-port`: Puerto del servidor de procesamiento

Ambos servidores quedarán corriendo y listos para recibir peticiones.

## Uso y Pruebas

Una vez que los servidores están en ejecución, puedes interactuar con el sistema de las siguientes maneras.

### Usando `curl`
Para analizar una única URL, puedes usar `curl`. Se recomienda guardar la salida en un archivo, ya que el JSON puede ser muy grande.
```bash
curl "http://127.0.0.1:8000/scrape?url=https://www.python.org"
```

### Usando el Cliente de Pruebas (`client.py`)
Para probar la robustez del sistema con múltiples URLs, puedes usar el script `client.py`.

1.  **Edita `urls.txt`**: Añade o quita las URLs que desees probar en este archivo, una por línea.
2.  **Ejecuta el cliente**: En una tercera terminal, simplemente ejecuta:
    ```bash
    python3 client.py
    ```
    
    O con parámetros personalizados:
    ```bash
    python3 client.py --host 127.0.0.1 --port 8000 --file urls.txt
    ```

El script procesará cada URL, mostrará un resumen del éxito o fallo de cada una y guardará los resultados JSON detallados en el directorio `results/` y los screenshot en `screenshots/`.

Es importante aclarar que, por diseño, las últimas tres peticiones en el archivo `urls.txt` que trae por defecto el repo, son direccion invalidas queriendo, para que falle, demostrando el correcto manejo de excepciones del sistema.

## Testing

Para asegurar la correcta funcionalidad y robustez del sistema, se han implementado pruebas unitarias y de integración utilizando `pytest`.

### Requisitos para las Pruebas

Asegúrate de tener instaladas las dependencias de desarrollo necesarias:
```bash
pip install -r requirements.txt
```

### Ejecución de las Pruebas

Para ejecutar todas las pruebas:

```bash
python3 -m pytest
```

Para ver más detalles:
```bash
python3 -m pytest -v
```

Para ejecutar las pruebas de un módulo específico:

**Pruebas del Servidor de Scraping:**
```bash
python3 -m pytest tests/test_scraper.py -v
```

**Pruebas del Servidor de Procesamiento:**
```bash
python3 -m pytest tests/test_processor.py -v
```

## Características Implementadas

### Funcionalidad Obligatoria ✅
- [x] Servidor asíncrono con asyncio y aiohttp
- [x] Servidor de procesamiento con multiprocessing
- [x] 4+ funciones principales (scraping, metadatos, screenshot, rendimiento)
- [x] Soporte IPv4 e IPv6
- [x] Comunicación mediante sockets TCP
- [x] Timeout de 30 segundos por página
- [x] Manejo robusto de errores
- [x] Interfaz CLI con argparse
- [x] Formato de respuesta JSON estructurado

### Características Adicionales ⭐
- [x] Rate limiting por dominio (10 requests/minuto)
- [x] Procesamiento de imágenes con thumbnails
- [x] Análisis de rendimiento con métricas detalladas
- [x] Paths relativos y multiplataforma
- [x] Tests unitarios con pytest
- [x] Logging detallado

## Estructura del Proyecto

```
TP2/
├── server_scraping.py          # Servidor asyncio (Parte A)
├── server_processing.py        # Servidor multiprocessing (Parte B)
├── client.py                   # Cliente de prueba
├── scraper/
│   ├── __init__.py
│   ├── html_parser.py          # Funciones de parsing HTML
│   ├── metadata_extractor.py  # Extracción de metadatos
│   └── async_http.py           # Cliente HTTP asíncrono
├── processor/
│   ├── __init__.py
│   ├── screenshot.py           # Generación de screenshots
│   ├── performance.py          # Análisis de rendimiento
│   └── image_processor.py      # Procesamiento de imágenes
├── common/
│   ├── __init__.py
│   ├── protocol.py             # Protocolo de comunicación
│   └── serialization.py        # Serialización de datos
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py
│   └── test_processor.py
├── requirements.txt
├── urls.txt                    # URLs de prueba
├── .gitignore
└── README.md
```

## Formato de Respuesta

El servidor devuelve un JSON con la siguiente estructura:

```json
{
  "url": "https://ejemplo.com",
  "timestamp": "2025-11-01T15:30:00Z",
  "scraping_data": {
    "title": "Título de la página",
    "links": ["url1", "url2", "..."],
    "meta_tags": {
      "description": "...",
      "keywords": "...",
      "og:title": "..."
    },
    "structure": {
      "h1": 2,
      "h2": 5,
      "h3": 10,
      "h4": 0,
      "h5": 0,
      "h6": 0
    },
    "images_count": 15,
    "image_urls": ["url1", "url2", "..."]
  },
  "processing_data": {
    "screenshot": "base64_encoded_image",
    "performance": {
      "load_time_ms": 1250,
      "total_size_kb": 2048,
      "num_requests": 45
    },
    "thumbnails": ["base64_thumb1", "base64_thumb2"],
    "status": "success"
  },
  "status": "success"
}
```

## Manejo de Errores

El sistema maneja robustamente los siguientes errores:

- **URLs inválidas o inaccesibles**: Retorna código 500 con descripción del error
- **Timeouts**: Límite de 30 segundos por página (configurable)
- **Errores de comunicación entre servidores**: Reintentos automáticos
- **Recursos no disponibles**: Las imágenes o recursos faltantes no detienen el proceso
- **Límites de memoria**: Solo procesa las primeras 20 imágenes y genera thumbnails de las 3 principales
- **Rate limiting**: Evita sobrecargar dominios (10 requests/minuto)

## Troubleshooting

### El Servidor B no responde
- Verifica que ChromeDriver esté instalado correctamente
- Asegúrate de que el puerto 9000 no esté en uso
- Revisa los logs del servidor de procesamiento

### Timeouts constantes
- Aumenta el timeout en `async_http.py` si la red es lenta
- Verifica tu conexión a Internet
- Algunos sitios pueden bloquear scrapers

### Problemas con screenshots
- Verifica que Chrome/Chromium esté instalado
- En servidores sin GUI, asegúrate de usar modo headless
- Revisa permisos del directorio `screenshots/`