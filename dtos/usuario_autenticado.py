from dataclasses import dataclass
from typing import Optional


@dataclass
class UsuarioAutenticado:
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    nome_perfil: Optional[str] = None
    foto_perfil: Optional[bool] = None
    bio_perfil: Optional[str] = None
    genero: Optional[str] = None