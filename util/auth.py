import os
import bcrypt
from fastapi.responses import RedirectResponse
import jwt
from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException, Request, status
from dtos.usuario_autenticado import UsuarioAutenticado

NOME_COOKIE_AUTH = "jwt-token"

async def obter_usuario_logado(request: Request) -> dict:
    try:
        token = request.cookies[NOME_COOKIE_AUTH]
        if token.strip() == "":
            return None
        dados = validar_token(token)
        usuario = UsuarioAutenticado(
            id = dados["id"],
            nome = dados["nome"],
            email = dados["email"],
            nome_perfil = dados["nome_perfil"], 
            foto_perfil = dados["foto_perfil"])
        if "mensagem" in dados.keys():
            usuario.mensagem = dados["mensagem"]
        return usuario
    except KeyError:
        return None

async def checar_autenticacao(request: Request, call_next):
    usuario = await obter_usuario_logado(request)
    request.state.usuario = usuario
    response = await call_next(request)
    if response.status_code == status.HTTP_307_TEMPORARY_REDIRECT:
        return response
    return response

async def checar_autorizacao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/usuario")
    if (area_do_usuario) and (not usuario):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False
    

def criar_token(id: int, nome: str, email: str, nome_perfil: str, foto_perfil: bool) -> str:
    payload = {
        "id" : id,
        "nome": nome,
        "email": email,
        "nome_perfil" : nome_perfil,
        "foto_perfil": foto_perfil,
        "exp": datetime.now() + timedelta(days=1)
    }
    return jwt.encode(payload, 
        os.getenv("JWT_SECRET"),
        os.getenv("JWT_ALGORITHM"))


def validar_token(token: str) -> dict:
    try:
        return jwt.decode(token, 
            os.getenv("JWT_SECRET"),
            os.getenv("JWT_ALGORITHM"))
    except jwt.ExpiredSignatureError:
        return { "id": None, "nome": None, "nome_perfil": None, "email": None, "perfil": 0, "mensagem": "Token expirado" }
    except jwt.InvalidTokenError:
        return { "id": None, "nome": None, "nome_perfil": None, "email": None, "perfil": 0, "mensagem": "Token inválido" }
    except Exception as e:
        return { "id": None, "nome": None, "nome_perfil": None, "email": None, "perfil": 0, "mensagem": f"Erro: {e}" }
    

def criar_cookie_auth(response, token):
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response


def configurar_swagger_auth(app):
    app.openapi_schema = app.openapi()
    app.openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema["security"] = [{"BearerAuth": []}]