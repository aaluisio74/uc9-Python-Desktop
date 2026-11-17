# PARTE 1 — Configurar variável de ambiente
# Deve acontecer antes de importar os módulos do projeto.
import os

os.environ.setdefault(
    "JWT_SECRET_KEY",
    "chave-exclusiva-para-testes-automatizados"
)

# PARTE 2 — Importações
import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, obter_sessao
from app.main import app


# PARTE 3 — Criar o ambiente de testes
@pytest.fixture
def ambiente_teste(tmp_path):

    # Cria um arquivo de banco temporário.
    caminho_banco = tmp_path / "teste_matriculas.db"

    # Cria uma conexão SQLite exclusiva para testes.
    engine_teste = create_engine(
        f"sqlite:///{caminho_banco}",
        connect_args={"check_same_thread": False}
    )

    # Cria as tabelas a partir dos modelos ORM.
    Base.metadata.create_all(bind=engine_teste)

    # Cria sessões para acessar o banco de testes.
    SessaoTeste = sessionmaker(
        bind=engine_teste,
        autoflush=False,
        autocommit=False
    )

    # Substitui a dependência de banco da aplicação.
    def obter_sessao_teste():
        db = SessaoTeste()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[obter_sessao] = obter_sessao_teste

    # Disponibiliza o cliente HTTP para os testes.
    with TestClient(app) as cliente:
        yield cliente

    # Remove a substituição da dependência.
    app.dependency_overrides.clear()

    # Fecha a conexão com o banco.
    engine_teste.dispose()
