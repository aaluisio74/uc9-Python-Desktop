# ARQUIVO PARA CRIAR AS TABELAS
from .database import Base, engine
from . import models

# Cria as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)

print("Banco de dados e tabelas verificados com sucesso!")