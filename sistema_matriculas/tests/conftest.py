
# ============================================================
# ARQUIVO: tests/conftest.py
# RESPONSABILIDADE: preparar o ambiente de testes
# ============================================================

# PARTE 1 — Configuração inicial
import os

# Define uma chave exclusiva para os testes.
# Deve ocorrer antes da importação de app.security.
os.environ["JWT_SECRET_KEY"] = (
    "chave-exclusiva-para-testes-automatizados"
)

# PARTE 2 — Importações
import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.database import Base, obter_sessao
from app.main import app
from app import models

from app.models import Usuario
from app.security import gerar_hash


# PARTE 3 — Criar banco temporário
@pytest.fixture
def ambiente_teste(tmp_path):

    # Arquivo SQLite dentro de uma pasta temporária.
    caminho_banco = tmp_path / "teste_matriculas.db"

    # Criar conexão exclusiva.
    engine_teste = create_engine(
        f"sqlite:///{caminho_banco}",
        connect_args={"check_same_thread": False}
    )

    # Habilitar chaves estrangeiras no SQLite.
    @event.listens_for(engine_teste, "connect")
    def habilitar_chaves_estrangeiras(
        conexao, registro
    ):
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Criar todas as tabelas dos modelos.
    Base.metadata.create_all(bind=engine_teste)

    # Criar substituição da sessão normal.
    SessaoTeste = sessionmaker(
        bind=engine_teste,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )

    def obter_sessao_teste():
        db = SessaoTeste()
        try:
            yield db
        finally:
            db.close()

    # Substituir a dependência utilizada pela API.
    app.dependency_overrides[obter_sessao] = (
        obter_sessao_teste
    )

    yield engine_teste

    # Limpar configurações ao finalizar.
    app.dependency_overrides.clear()
    engine_teste.dispose()


# PARTE 4 — Disponibilizar uma sessão de testes
@pytest.fixture
def db_session(ambiente_teste):

    SessaoTeste = sessionmaker(
        bind=ambiente_teste,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )

    db = SessaoTeste()

    yield db

    db.close()


# PARTE 5 — Disponibilizar cliente HTTP
@pytest.fixture
def cliente(ambiente_teste):

    with TestClient(app) as test_client:
        yield test_client


# PARTE 6 — Criar usuário administrador
@pytest.fixture
def usuario_admin(db_session):

    usuario = Usuario(
        username="admin_teste",
        senha_hash=gerar_hash("SenhaAdmin123!"),
        papel="admin"
    )

    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    return usuario


# PARTE 7 — Criar usuário de consulta
@pytest.fixture
def usuario_consulta(db_session):

    usuario = Usuario(
        username="consulta_teste",
        senha_hash=gerar_hash("SenhaConsulta123!"),
        papel="consulta"
    )

    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    return usuario


# PARTE 8 — Obter token do administrador
@pytest.fixture
def token_admin(cliente, usuario_admin):

    resposta = cliente.post(
        "/token",
        data={
            "username": "admin_teste",
            "password": "SenhaAdmin123!"
        }
    )

    assert resposta.status_code == 200

    return resposta.json()["access_token"]


# PARTE 9 — Obter token do usuário de consulta
@pytest.fixture
def token_consulta(cliente, usuario_consulta):

    resposta = cliente.post(
        "/token",
        data={
            "username": "consulta_teste",
            "password": "SenhaConsulta123!"
        }
    )

    assert resposta.status_code == 200

    return resposta.json()["access_token"]


# PARTE 10 — Cabeçalhos de autenticação
@pytest.fixture
def headers_admin(token_admin):

    return {
        "Authorization": f"Bearer {token_admin}"
    }


@pytest.fixture
def headers_consulta(token_consulta):

    return {
        "Authorization": f"Bearer {token_consulta}"
    }
