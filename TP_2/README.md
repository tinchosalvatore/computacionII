# TP2 - Sistema de Scraping y Análisis Web Distribuido

Este proyecto implementa un sistema distribuido para el scraping y análisis de páginas web. El sistema está compuesto por dos servidores que trabajan de forma coordinada para procesar solicitudes de manera eficiente, separando las tareas de red (I/O-bound) de las tareas de procesamiento intensivo (CPU-bound).

## Arquitectura del Sistema

La arquitectura se basa en un modelo de dos servidores desacoplados con responsabilidades bien definidas:

### Servidor A: Frontend de Scraping (`server_scraping.py`)
- **Rol**: Actúa como el punto de entrada para el cliente. Recibe peticiones HTTP con la URL a analizar.
- **Tareas**: Realiza un scraping inicial y ligero de la página para extraer información como el título, links, meta tags, etc. Coordina con el Servidor B para análisis más pesados.
- **Tecnología**: Construido con `asyncio` y `aiohttp` para manejar un gran número de conexiones concurrentes de forma no bloqueante, ideal para tareas de red.

### Servidor B: Backend de Procesamiento (`server_processing.py`)
- **Rol**: Funciona como un "worker" de tareas pesadas. No tiene contacto directo con el cliente.
- **Tareas**: Ejecuta operaciones que consumen CPU, como la renderización de páginas para tomar capturas de pantalla, el análisis de rendimiento de carga y el procesamiento de imágenes.
- **Tecnología**: Construido con `socketserver` y `multiprocessing`. Utiliza un `ProcessPoolExecutor` para distribuir el trabajo entre múltiples procesos, aprovechando al máximo los núcleos del CPU.

### Comunicación
Ambos servidores se comunican a través de sockets TCP. El Servidor A actúa como cliente del Servidor B, enviándole una tarea (la URL a procesar y las URLs de sus imágenes) y esperando de forma asíncrona una respuesta consolidada con todos los análisis realizados.

## Tecnologías Utilizadas

- **`aiohttp`**: Framework base para el servidor web asíncrono (Servidor A).
- **`asyncio`**: Utilizado para gestionar el event loop y las operaciones de red no bloqueantes en el Servidor A.
- **`multiprocessing`**: Permite la ejecución de tareas en paralelo en el Servidor B, evitando que las operaciones CPU-bound bloqueen el sistema.
- **`socketserver`**: Proporciona la estructura para el servidor TCP del Servidor B.
- **`BeautifulSoup4`**: Librería principal para el parseo de HTML y la extracción de datos en el Servidor A.
- **`Playwright`**: Herramienta de automatización de navegadores utilizada en el Servidor B para:
    - Tomar capturas de pantalla de las páginas web.
    - Realizar análisis de rendimiento mediante la grabación de archivos HAR.
- **`Pillow`**: Librería para el procesamiento de imágenes, utilizada para crear los thumbnails en el Servidor B.
- **`requests`**: Utilizado en el `client.py` para realizar peticiones HTTP de prueba al sistema.

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
    source venv/bin/activate
    ```

3.  **Instalar dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar los navegadores para Playwright:**
    Este comando descarga las versiones de los navegadores que Playwright necesita para operar.
    ```bash
    playwright install
    ```

## Ejecución

El sistema requiere que ambos servidores se ejecuten de forma simultánea en terminales separadas.

### 1. Iniciar Servidor de Procesamiento (Servidor B)
En una primera terminal, ejecuta:
```bash
# Ejemplo: Escuchar en localhost, puerto 9000, con 4 procesos
python3 server_processing.py -i 127.0.0.1 -p 9000 -n 4
```

### 2. Iniciar Servidor de Scraping (Servidor A)
En una segunda terminal, ejecuta, asegurándote de apuntar al host y puerto del Servidor B:
```bash
# Ejemplo: Escuchar en localhost, puerto 8000 y conectar al Servidor B en el puerto 9000
python3 server_scraping.py -i 127.0.0.1 -p 8000 --processor-host 127.0.0.1 --processor-port 9000
```

Ambos servidores quedarán corriendo y listos para recibir peticiones.

## Uso y Pruebas

Una vez que los servidores están en ejecución, puedes interactuar con el sistema de las siguientes maneras.

### Usando `curl`
Para analizar una única URL, puedes usar `curl`. Se recomienda guardar la salida en un archivo, ya que el JSON puede ser muy grande.
```bash
curl "http://127.0.0.1:8000/scrape?url=https://www.python.org" > response.json
```

### Usando el Cliente de Pruebas (`client.py`)
Para probar la robustez del sistema con múltiples URLs, puedes usar el script `client.py`.

1.  **Edita `urls.txt`**: Añade o quita las URLs que desees probar en este archivo, una por línea.
2.  **Ejecuta el cliente**: En una tercera terminal, simplemente ejecuta:
    ```bash
    python3 client.py
    ```
El script procesará cada URL, mostrará un resumen del éxito o fallo de cada una y guardará los resultados JSON detallados en el directorio `results/`.
