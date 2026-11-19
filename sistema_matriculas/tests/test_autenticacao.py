
# ============================================================
# ARQUIVO: tests/test_autenticacao.py
# RESPONSABILIDADE: testar autenticação JWT
# ============================================================


# TESTE 01 — Login correto
def test_login_sucesso(cliente, usuario_admin):

    resposta = cliente.post(
        "/token",
        data={
            "username": "admin_teste",
            "password": "SenhaAdmin123!"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"


# TESTE 02 — Usuário inexistente
def test_login_usuario_inexistente(cliente):

    resposta = cliente.post(
        "/token",
        data={
            "username": "nao_existe",
            "password": "Senha123!"
        }
    )

    assert resposta.status_code == 401


# TESTE 03 — Senha incorreta
def test_login_senha_incorreta(cliente, usuario_admin):

    resposta = cliente.post(
        "/token",
        data={
            "username": "admin_teste",
            "password": "senha_errada"
        }
    )

    assert resposta.status_code == 401


# TESTE 04 — Consultar usuário autenticado
def test_consultar_usuario_atual(
    cliente,
    headers_admin
):

    resposta = cliente.get(
        "/usuarios/me",
        headers=headers_admin
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["username"] == "admin_teste"
    assert dados["papel"] == "admin"


# TESTE 05 — Acessar sem token
def test_acesso_sem_token(cliente):

    resposta = cliente.get("/usuarios/me")

    assert resposta.status_code == 401


# TESTE 06 — Token inválido
def test_acesso_com_token_invalido(cliente):

    resposta = cliente.get(
        "/usuarios/me",
        headers={
            "Authorization": "Bearer token_invalido"
        }
    )

    assert resposta.status_code == 401


# TESTE 07 — Usuário de consulta autenticado
def test_login_usuario_consulta(
    cliente,
    headers_consulta
):

    resposta = cliente.get(
        "/usuarios/me",
        headers=headers_consulta
    )

    assert resposta.status_code == 200

    assert resposta.json()["papel"] == "consulta"
