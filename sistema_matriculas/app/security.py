# PARTE 1 — Importações de segurança
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import obter_sessao
from .models import Usuario


# PARTE 2 — Configurações de autenticação
# A chave deve ser fornecida pelo ambiente, nunca publicada no Git.
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
TEMPO_TOKEN_MINUTOS = 30

hash_senhas = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# PARTE 3 — Criar e verificar hashes de senhas
def gerar_hash(senha: str) -> str:
    return hash_senhas.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return hash_senhas.verify(senha, senha_hash)


# PARTE 4 — Gerar token de acesso
def criar_token(username: str) -> str:
    agora = datetime.now(timezone.utc)

    payload = {
        "sub": username,
        "iat": agora,
        "exp": agora + timedelta(
            minutes=TEMPO_TOKEN_MINUTOS
        ),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# PARTE 5 — Recuperar o usuário autenticado
def usuario_atual(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(obter_sessao)],
):
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username = payload.get("sub")

        if not isinstance(username, str) or not username:
            raise erro

    except (InvalidTokenError, ValueError):
        raise erro

    usuario = db.scalars(
        select(Usuario).where(
            Usuario.username == username
        )
    ).first()

    if usuario is None:
        raise erro

    return usuario


# PARTE 6 — Verificar o papel do usuário
def exigir_admin(
    usuario: Annotated[Usuario, Depends(usuario_atual)],
):
    if usuario.papel != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente.",
        )

    return usuario
