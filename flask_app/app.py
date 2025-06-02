from flask import Flask, request, Response
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

USUARIO = "admin"
PASSWORD = "secreto"

def autenticar():
    mensaje = {'mensaje': "Autenticación requerida."}
    return Response(str(mensaje), 401, {"WWW-Authenticate": "Basic realm='Login Required'"})

def verificar_auth(usuario, password):
    return usuario == USUARIO and password == PASSWORD

def requiere_auth(f):
    def decorador(*args, **kwargs):
        auth = request.authorization
        if not auth or not verificar_auth(auth.username, auth.password):
            return autenticar()
        return f(*args, **kwargs)
    decorador.__name__ = f.__name__
    return decorador

@app.route("/")
def publico():
    """
    Ruta pública sin autenticación.
    ---
    responses:
      200:
        description: Éxito
    """
    return "Ruta pública: no requiere autenticación."

@app.route("/privado")
@requiere_auth
def privado():
    """
    Ruta protegida por autenticación básica.
    ---
    security:
      - BasicAuth: []
    responses:
      200:
        description: Acceso autorizado
      401:
        description: No autorizado
    """
    return "Ruta protegida: acceso autorizado."

if __name__ == "__main__":
    app.run(debug=True)
