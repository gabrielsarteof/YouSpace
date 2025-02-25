from datetime import date, datetime, timedelta
import json
import uuid
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, UploadFile, File, status
import os
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha
from util.cadastro import *
from util.cookies import *
from util.mensagens import adicionar_mensagem_erro
from util.templates import obter_jinja_templates
from util.validators import *

router = APIRouter()

templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return RedirectResponse("/conecte-se", status.HTTP_303_SEE_OTHER)

@router.get("/conecte-se", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("main/pages/conecte-se.html", {"request": request})

@router.post("/login")
async def post_login(request: Request, response: Response): 
    dados = dict(await request.form())
    
    usuario = UsuarioRepo.checar_credenciais(dados["email"], dados["senha"])
    
    if usuario is None:
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Seus dados estão incorretos. Confira-os")
        return response

    token = criar_token(usuario.id, usuario.nome, usuario.email, usuario.nome_perfil, usuario.foto_perfil)

    response = RedirectResponse(f"/usuario/feed", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response

@router.get("/cadastre-se", response_class=HTMLResponse)
async def get_criar_conta(request: Request, tipo_perfil: int = None):
    return templates.TemplateResponse("main/pages/cadastre-se.html", {"request": request})

@router.post("/cadastrar")
async def post_cadastrar_paciente(request: Request, registro_profissional: UploadFile = File(None)):
    dados = dict(await request.form())
    response = RedirectResponse(f"/cadastre-se", status_code=status.HTTP_303_SEE_OTHER)
    if not is_password(dados["senha"]):
        adicionar_mensagem_erro(response, "As senhas devem ter no mínimo 6 caracteres, letras maiúsculas e minúsculas, números e caracteres especiais."),
        return response
    if not is_matching_fields(dados["senha"], dados["conf_senha"]):
        adicionar_mensagem_erro(response, "As senhas não coincidem.")
        return response
    else : dados.pop("conf_senha")
    if not is_person_fullname(dados["nome"]):
        adicionar_mensagem_erro(response, "Os nomes devem conter um primeiro nome e um sobrenome."),
        return response
    if not is_only_letters_or_space(dados["nome"]):
        adicionar_mensagem_erro(response, "Os nomes devem conter apenas letras e espaços."),
        return response
    if not is_own_name(dados["nome"]):
        adicionar_mensagem_erro(response, "Esse não é um nome próprio valido. Confira-o."),
        return response
    if not is_user_name(dados["nome_perfil"]):
        adicionar_mensagem_erro(response, "Os nomes de usuário só podem usar letras, números, sublinhados e pontos."),
        return response
    if not UsuarioRepo.is_username_unique(dados["nome_perfil"]):
        adicionar_mensagem_erro(response, "Esse nome de usuário não está disponível. Tente outro nome..")
        return response
    if not is_email(dados["email"]):
        adicionar_mensagem_erro(response, "Esse não é um email valido. Confira-o")
        return response
    if not UsuarioRepo.is_email_unique(dados["email"]):
        adicionar_mensagem_erro(response, "Outra conta está usando o mesmo email.")
        return response
    senha_hash = obter_hash_senha(dados["senha"])
    dados["senha"] = senha_hash
    agora = datetime.now()
    dados["data_criacao"] = agora.strftime('%Y-%m-%d %H:%M:%S') 
    dados["status"] = "ativo"
    usuario = Usuario(**dados)
    UsuarioRepo.inserir(usuario)
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    return response

@router.get("/esqueci_a_senha", response_class=HTMLResponse)
async def get_esqueci_a_senha(request: Request):
    return templates.TemplateResponse("main/pages/esqueci_a_senha.html", {"request": request})

@router.post("/senha_redefinada", response_class=HTMLResponse)
async def post_senha_redefinida(request: Request):
    return templates.TemplateResponse("main/pages/senha_redefinida.html", {"request": request})

@router.get("/conta_criada", response_class=HTMLResponse)
async def get_conta_criada(request: Request):
    return templates.TemplateResponse("main/pages/conta_criada.html", {"request": request})

@router.get("/sair")
async def get_sair(request: Request):
    request.state.usuario = None
    response = RedirectResponse("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax"
    )
    return response

