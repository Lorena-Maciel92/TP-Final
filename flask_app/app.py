from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Cargar API_KEY desde .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

# Lista de IPs permitidas
ALLOWED_IPS = ["127.0.0.1"]

# Middleware antes de cada request
@app.before_request
def validar_ip():
    ip_cliente = request.remote_addr
    if ip_cliente not in ALLOWED_IPS:
        return jsonify({"error": f"IP {ip_cliente} no autorizada"}), 403

# Ruta protegida por API Key
@app.route("/protegido")
def protegido():
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "API Key incorrecta"}), 401
    return jsonify({"mensaje": "Acceso permitido"})

if __name__ == "__main__":
    app.run(debug=True)
