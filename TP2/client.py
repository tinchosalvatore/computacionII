import requests
import time
import os
import argparse
from urllib.parse import quote_plus

def main():
    parser = argparse.ArgumentParser(description="Cliente de prueba para el sistema de scraping.")
    parser.add_argument("--host", default="127.0.0.1", help="Host del servidor de scraping.")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor de scraping.")
    parser.add_argument("--file", default="urls.txt", help="Archivo con la lista de URLs a procesar.")
    args = parser.parse_args()

    server_url = f"http://{args.host}:{args.port}"
    urls_file = args.file

    # Crear directorio para los resultados si no existe
    if not os.path.exists('results'):
        os.makedirs('results')

    try:
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] El archivo '{urls_file}' no fue encontrado.")
        return

    print(f"Iniciando prueba con {len(urls)} URLs contra el servidor en {server_url}\n")

    success_count = 0
    fail_count = 0

    for i, url in enumerate(urls):
        print(f"({i+1}/{len(urls)}) Procesando: {url}")
        start_time = time.time()
        
        try:
            # Codificamos la URL para que sea segura en una petición HTTP
            encoded_url = quote_plus(url)
            request_url = f"{server_url}/scrape?url={encoded_url}"
            
            response = requests.get(request_url, timeout=120) # Timeout generoso de 2 minutos
            
            duration = time.time() - start_time

            if response.status_code == 200:
                print(f"  -> ÉXITO ({response.status_code}) en {duration:.2f}s")
                success_count += 1
                # Guardar respuesta en un archivo
                safe_filename = f"result_{i+1}_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.json"
                with open(os.path.join('results', safe_filename), 'w', encoding='utf-8') as f_out:
                    f_out.write(response.text)
            else:
                print(f"  -> FALLO ({response.status_code}) en {duration:.2f}s - Respuesta: {response.text[:100]}...")
                fail_count += 1

        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            print(f"  -> ERROR de conexión en {duration:.2f}s: {e}")
            fail_count += 1
    
    print(f"\nPrueba finalizada. {success_count} éxito(s), {fail_count} fallo(s).")

if __name__ == "__main__":
    main()
