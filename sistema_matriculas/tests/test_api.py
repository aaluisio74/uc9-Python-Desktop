
# ============================================================
# ARQUIVO: tests/test_api.py
# RESPONSABILIDADE: testar os endpoints e a segurança da API
# ============================================================


# PARTE 1 — TESTAR acesso sem autenticação

def test_listar_estudantes_sem_token(cliente):

    resposta = cliente.get("/estudantes")

    assert resposta.status_code == 401


# PARTE 2 — TESTAR proteção da API

def test_acesso_sem_autenticacao(cliente):

    resposta = cliente.get("/estudantes")

    assert resposta.status_code == 401


# PARTE 3 — TESTAR login com credenciais inválidas

def test_login_com_credenciais_invalidas(cliente):

    resposta = cliente.post(
        "/token",
        data={
            "username": "usuario_inexistente",
            "password": "senha_incorreta"
        }
    )

    assert resposta.status_code == 401
