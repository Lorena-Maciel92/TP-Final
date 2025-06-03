from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(
    title="API Segura de Lorena Maciel",
    description="Esta API tiene protección por API Key, IP y JWT.",
    version="1.0.0",
    contact={
        "name": "Lorena Maciel",
        "email": "lorena@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)


# Configuraciones
API_KEY = os.getenv("API_KEY", "12345")
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta")
ALGORITHM = "HS256"
ALLOWED_IPS = ["127.0.0.1"]

# Middleware para IP
@app.middleware("http")
async def verificar_ip(request: Request, call_next):
    ip = request.client.host
    if ip not in ALLOWED_IPS:
        return JSONResponse(status_code=403, content={"error": f"IP {ip} no autorizada"})
    return await call_next(request)

# Ruta protegida por API Key
@app.get("/protegido-api-key", summary="Protegido por API Key", description="Requiere API Key en header")
async def protegido_api_key(request: Request):
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key incorrecta")
    return {"mensaje": "Acceso permitido"}

# Ruta para obtener JWT
@app.post("/login", summary="Iniciar sesión", description="Retorna un token si las credenciales son válidas")
def login(datos: dict):
    if datos["usuario"] == "admin" and datos["password"] == "123":
        exp = datetime.utcnow() + timedelta(minutes=30)
        token = jwt.encode({"sub": datos["usuario"], "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# Seguridad: validación del token
security = HTTPBearer()

def validar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# Ruta protegida con JWT
@app.get("/protegido-jwt", summary="Protegido con JWT", description="Requiere token JWT en header Authorization")
def ruta_protegida(payload: dict = Depends(validar_token)):
    return {"mensaje": f"Hola {payload['sub']}, acceso permitido con JWT"}
