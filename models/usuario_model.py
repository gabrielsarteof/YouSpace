from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    data_nascimento: Optional[date] = None
    data_criacao: Optional[date] = None
    nome_perfil: Optional[str] = None
    foto_perfil: Optional[bool] = None
    bio_perfil: Optional[str] = None
    genero: Optional[str] = None
    status: Optional[str] = None
    
