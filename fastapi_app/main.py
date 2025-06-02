from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()

security = HTTPBasic()

USUARIO = "admin"
PASSWORD = "secreto"

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, USUARIO)
    correct_pass = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def publico():
    return {"mensaje": "Ruta pública: no requiere autenticación."}

@app.get("/privado")
def privado(usuario: str = Depends(autenticar)):
    return {"mensaje": f"Ruta protegida. Bienvenido, {usuario}"}
