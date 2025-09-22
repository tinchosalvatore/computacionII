"""
Crear un servidor htttp que sirva archivos estaticos desde un directorio especifico. El servidor debe:
 
- Responder a solicitudes GET
- Servir archivos HTML, CSS, JS e imágenes
- Mostrar un listado de directorio cuando se accede a una carpeta
- Devolver 404 para archivos inexistentes


python3 servidor.py
y acceder a http://localhost:8000

"""
import http.server
import socketserver

PORT = 8000
DIRECTORIO = "public"   # el directorio que contiene los archivos estaticos, desde donde seran servidos

# usamos el servidor SimpleHTTPRequestHandler ya que no necesitamos metodos propios. Pero si queremos personalizarlo
class MiHandler(http.server.SimpleHTTPRequestHandler):
    # Iniciamos el servidor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORIO, **kwargs)

    # manejo de errores
    def send_error(self, code: int, message=None, explain=None):  
        if code == 404:
            self.send_response(404)  # enviamos el codigo de error
            self.send_header("Content-type", "text/html")   # header
            self.end_headers()
            self.wfile.write(b"<h1>404 - Archivo no encontrado</h1>")   #body del mensaje de error
        
        else:  # error generico en caso de no ser 404 
            super().send_error(code, message, explain)  


with socketserver.TCPServer(("", PORT), MiHandler) as httpd:
    print(f"serivendor corriendo en el puerto local {PORT}")
    httpd.serve_forever()   # mantiene el servidor corriendo indefinidamente, hasta que se interrumpa
