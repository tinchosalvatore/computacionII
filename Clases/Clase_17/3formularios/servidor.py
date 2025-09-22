from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html

# Usa el context manager para abrir el nombre.html correspondiente
def cargar_template(nombre):
    with open(f"templates/{nombre}", "r", encoding="utf-8") as f:
        return f.read()

class MiHandler(BaseHTTPRequestHandler):
    # header aclara que vamos a trabajar con html
    def _set_headers(self, code=200, content_type="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    # Error en formato html
    def send_error(self, code, message):
        self._set_headers(code)
        self.wfile.write(f"<h1>Error {code}</h1><p>{html.escape(message)}</p>".encode())


    # Si estamos en el index mostramos el formulario
    def do_GET(self):
        if self.path == "/":
            self._set_headers()
            form_html = cargar_template("formulario.html")
            self.wfile.write(form_html.encode("utf-8"))
        else:
            self.send_error(404, "Ruta no encontrada")

    
    def do_POST(self):
        if self.path == "/submit": # /submit es el nombre de la accion en el formulario.html
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            
            # parse_qs parsea el cuerpopo de la peticion a un diccionario
            # Ejemplo: {"nombre": ["Juan"], "email": ["juan@example.com"]}
            datos = parse_qs(body)

            nombre = datos.get("nombre", ["(no especificado)"])[0]
            email = datos.get("email", ["(no especificado)"])[0]
            pais = datos.get("pais", ["(no especificado)"])[0]
            suscripcion = "Sí" if "suscripcion" in datos else "No"    
            # si la suscripcion esta en los datos del parse, es porque tiene suscripcion activa

            self._set_headers()
            confirm_html = cargar_template("confirmacion.html")
            # reemplazamos placeholders de confirmacion.html con los datos ingresados 
            confirm_html = confirm_html.replace("{{nombre}}", html.escape(nombre))
            confirm_html = confirm_html.replace("{{email}}", html.escape(email))
            confirm_html = confirm_html.replace("{{pais}}", html.escape(pais))
            confirm_html = confirm_html.replace("{{suscripcion}}", suscripcion)

            self.wfile.write(confirm_html.encode("utf-8"))
        else:
            self.send_error(404, "Ruta no encontrada")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MiHandler)
    print("Servidor corriendo en http://localhost:8000")
    server.serve_forever()