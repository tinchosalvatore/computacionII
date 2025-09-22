"""
Ejercicio 2: API REST Básica

Implementa un servidor que simule una API REST para gestionar una lista de usuarios. Debe soportar:

    GET /users - Listar todos los usuarios
    GET /users/id - Obtener un usuario específico
    POST /users - Crear un nuevo usuario
    PUT /users/id - Actualizar un usuario existente
    DELETE /users/id - Eliminar un usuario

Los datos pueden almacenarse en memoria (lista/diccionario).

Usamos curl para probarlo despues de levantar el servidor:

GET
curl http://localhost:8000/users   --> lista todos los Usuarios
curl http://localhost:8000/users/1  --> obtiene un Usuario por su id

POST
curl -X POST http://localhost:8000/users \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Ana", "email": "ana@example.com"}'


PUT
curl -X PUT http://localhost:8000/users/1 \
     -H "Content-Type: application/json" \
     -d '{"email": "nuevo@mail.com"}'

DELETE
curl -X DELETE http://localhost:8000/users/2


"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from psutil import users

# simulacion de base de datos de usuarios
usuarios = {
    1: {"id": 1, "nombre": "Juan", "email": "juan@example.com"},
    2: {"id": 2, "nombre": "María", "email": "maria@example.com"},
    3: {"id": 3, "nombre": "Pedro", "email": "pedro@example.com"},
    4: {"id": 4, "nombre": "Luis", "email": "luis@example.com"}
}
contador_id = max(usuarios.keys()) + 1   # para autoincrementar el id en base a la cantidad de usuarios 


class MiHandler(BaseHTTPRequestHandler):   # usamos el handler personalizable, para modificar los metodos

    # el header indica que trabajaremos con json, simulando una db de Usuarios 
    def _set_headers(self, code=200, content_type="application/json"):   
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    # devuelve error en formato json
    def send_error(self, code , message):
        self._set_headers(code)  # enviamos el codigo de error
        self.wfile.write(json.dumps({"error": message}).encode())  # error generico en formato json 
        
    def do_GET(self):   # GET /users -> Lista todos los usuarios
        if self.path == "/users":
            self._set_headers()
            self.wfile.write(json.dumps(list(usuarios.values())).encode())  

        elif self.path.startswith("/users/"):   # GET /users/id -> Obtener usuario por su id
            id_usuario = int(self.path.split("/")[-1])
            
            if id_usuario in usuarios:
                self._set_headers()
                self.wfile.write(json.dumps(usuarios[id_usuario]).encode())
            else:
                self.send_error(404, "ID de Usuario invalido")

        else:
            self.send_error(404, "Ruta no encontrada")

    def do_POST(self):  # POST /users -> Crear un nuevo usuario
        if self.path == "/users":
            
            # leer el body de la peticion
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            
            # parsear el body a un objeto json
            # si el formato no es valido, lanzara un error
            try:
                data = json.loads(body)
            except json.JSONDecodeError as e:
                self.send_error(400, "Contenido del body no es un objeto json valido")
                return
            
            # A su vez, si no hay email o nombre, error
            if "email" not in data or "nombre" not in data:
                self.send_error(400, "El body debe contener 'email' y 'nombre'")
                return
            
            
            global contador_id  # lo usamos para autoincrementar el id por cada nuevo Usuario
            new_user = {
                "id": contador_id,
                "email": data["email"],
                "nombre": data["nombre"]
            }
            usuarios[contador_id] = new_user  # lo agregamos al diccionario de usuarios
            
            
            self._set_headers()
            self.wfile.write(json.dumps(new_user).encode())
            contador_id += 1  # incrementamos el contador para el proximo usuario

    def do_PUT(self):  # Actualiza un Usuario existente
        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            

            if user_id not in usuarios:
                self.send_error(404, "Usuario no encontrado")
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            
            # obtenemos el usuario por su id
            user = usuarios[user_id]
            # actualizamos los campos
            user["nombre"] = data.get("nombre", user["nombre"])
            user["email"] = data.get("email", user["email"])

            self._set_headers()
            self.wfile.write(json.dumps(user).encode())
        else:
            self.send_error(404, "Ruta no encontrada")
    def do_DELETE(self):
        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            
            if user_id in usuarios:
                eliminado = usuarios.pop(user_id)  #eliminamos del diccionario de Usuarios
                self._set_headers()
                self.wfile.write(json.dumps(eliminado).encode())
            else:
                self.send_error(404, "Usuario no encontrado")
        else:
            self.send_error(404, "Ruta no encontrada")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MiHandler)
    print("Servidor API corriendo en http://localhost:8000")
    server.serve_forever()