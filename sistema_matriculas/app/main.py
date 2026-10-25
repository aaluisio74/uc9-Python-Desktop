# PARTE 1 — Importações
from typing import Annotated

from fastapi import (
    Depends, FastAPI, HTTPException, status
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import obter_sessao
from .models import Estudante, Usuario
from .schemas import EstudanteEntrada, EstudanteSaida
from .security import (
    verificar_senha, criar_token,
    usuario_atual, exigir_admin
)


# PARTE 2 — Criar a aplicação
app = FastAPI(
    title="Sistema de Matrículas",
    version="1.0.0",
)

SessaoDB = Annotated[Session, Depends(obter_sessao)]


# PARTE 3 — Endpoint de autenticação
@app.post("/token")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessaoDB,
):
    usuario = db.scalars(
        select(Usuario).where(
            Usuario.username == form.username
        )
    ).first()

    if (
        usuario is None
        or not verificar_senha(
            form.password, usuario.senha_hash
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": criar_token(usuario.username),
        "token_type": "bearer",
    }


# PARTE 4 — Consultar o próprio usuário
@app.get("/usuarios/me")
def meu_usuario(
    usuario: Annotated[Usuario, Depends(usuario_atual)],
):
    return {
        "id": usuario.id,
        "username": usuario.username,
        "papel": usuario.papel,
    }


# PARTE 5 — CREATE: cadastrar estudante
@app.post(
    "/estudantes",
    response_model=EstudanteSaida,
    status_code=status.HTTP_201_CREATED,
)
def criar_estudante(
    dados: EstudanteEntrada,
    db: SessaoDB,
    admin: Annotated[Usuario, Depends(exigir_admin)],
):
    estudante = Estudante(
        nome=dados.nome.strip(),
        email=str(dados.email).lower(),
    )

    db.add(estudante)

    try:
        db.commit()
        db.refresh(estudante)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado ou dados incompatíveis.",
        )

    return estudante


# PARTE 6 — READ: listar estudantes
@app.get("/estudantes", response_model=list[EstudanteSaida])
def listar_estudantes(
    db: SessaoDB,
    usuario: Annotated[Usuario, Depends(usuario_atual)],
    limite: int = 50,
    deslocamento: int = 0,
):
    if not 1 <= limite <= 100 or deslocamento < 0:
        raise HTTPException(
            status_code=422,
            detail="Parâmetros de paginação inválidos.",
        )

    consulta = (
        select(Estudante)
        .order_by(Estudante.id)
        .limit(limite)
        .offset(deslocamento)
    )

    return db.scalars(consulta).all()


# PARTE 7 — READ: consultar um estudante
@app.get(
    "/estudantes/{estudante_id}",
    response_model=EstudanteSaida,
)
def buscar_estudante(
    estudante_id: int,
    db: SessaoDB,
    usuario: Annotated[Usuario, Depends(usuario_atual)],
):
    estudante = db.get(Estudante, estudante_id)

    if estudante is None:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado.",
        )

    return estudante


# PARTE 8 — UPDATE: atualizar estudante
@app.put(
    "/estudantes/{estudante_id}",
    response_model=EstudanteSaida,
)
def atualizar_estudante(
    estudante_id: int,
    dados: EstudanteEntrada,
    db: SessaoDB,
    admin: Annotated[Usuario, Depends(exigir_admin)],
):
    estudante = db.get(Estudante, estudante_id)

    if estudante is None:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado.",
        )

    estudante.nome = dados.nome.strip()
    estudante.email = str(dados.email).lower()

    try:
        db.commit()
        db.refresh(estudante)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado ou dados incompatíveis.",
        )

    return estudante


# PARTE 9 — DELETE: excluir estudante
@app.delete("/estudantes/{estudante_id}")
def excluir_estudante(
    estudante_id: int,
    db: SessaoDB,
    admin: Annotated[Usuario, Depends(exigir_admin)],
):
    estudante = db.get(Estudante, estudante_id)

    if estudante is None:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado.",
        )

    # Não excluir se houver matrículas relacionadas.
    if estudante.matriculas:
        raise HTTPException(
            status_code=409,
            detail="Cancele ou resolva as matrículas antes da exclusão.",
        )

    db.delete(estudante)
    db.commit()

    return {"mensagem": "Estudante excluído."}
