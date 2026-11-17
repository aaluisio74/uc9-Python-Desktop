# PARTE 1 — Importações dos testes
from fastapi.testclient import TestClient

from app.main import app


# PARTE 2 — Cliente HTTP de testes
# Este exemplo verifica o bloqueio de acesso sem autenticação.
client = TestClient(app)


# PARTE 3 — Teste de segurança
def test_listar_estudantes_sem_token():
    resposta = client.get("/estudantes")

    assert resposta.status_code == 401
    
# PARTE 1 — TESTAR proteção da API

def test_acesso_sem_autenticacao(ambiente_teste):

    resposta = ambiente_teste.get("/estudantes")

    assert resposta.status_code == 401


# PARTE 2 — TESTAR login com dados inválidos

def test_login_com_credenciais_invalidas(ambiente_teste):

    resposta = ambiente_teste.post(
        "/token",
        data={
            "username": "usuario_inexistente",
            "password": "senha_incorreta"
        }
    )

    assert resposta.status_code == 401
