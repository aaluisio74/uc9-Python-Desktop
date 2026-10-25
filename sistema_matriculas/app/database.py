# ARQUIVO QUE DEFINE A CONEXÃO COM O BANCO E A CLASSE BASE, QUE SERÁ USADA PELOS MODELOS.
# PARTE 1 — Importações do SQLAlchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# PARTE 2 — Configuração da URL do banco
# SQLite é usado inicialmente para facilitar a atividade.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./matriculas.db"
)

# PARTE 3 — Configuração do mecanismo de conexão
# check_same_thread=False é necessário para este exemplo
# com SQLite e uso por diferentes contextos da aplicação.
opcoes = {}
if DATABASE_URL.startswith("sqlite"):
    opcoes["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    **opcoes,
)

# PARTE 4 — Fábrica de sessões
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

# PARTE 5 — Classe-base para os modelos ORM
class Base(DeclarativeBase):
    pass

# PARTE 6 — Dependência para fornecer uma sessão
def obter_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
