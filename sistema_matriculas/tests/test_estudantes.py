# ============================================================
# ARQUIVO: tests/test_estudantes.py
# RESPONSABILIDADE: testar CRUD e autorização
# ============================================================


# DADOS PADRÃO PARA TESTES
def dados_estudante():

    return {
        "nome": "Maria da Silva",
        "email": "maria@example.com"
    }


# TESTE 01 — CREATE: cadastrar estudante
def test_cadastrar_estudante(
    cliente,
    headers_admin
):

    resposta = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Maria da Silva"
    assert dados["email"] == "maria@example.com"
    assert "id" in dados


# TESTE 02 — READ: listar estudantes
def test_listar_estudantes(
    cliente,
    headers_admin
):

    cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    resposta = cliente.get(
        "/estudantes",
        headers=headers_admin
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


# TESTE 03 — READ: consultar estudante
def test_buscar_estudante(
    cliente,
    headers_admin
):

    cadastro = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    estudante_id = cadastro.json()["id"]

    resposta = cliente.get(
        f"/estudantes/{estudante_id}",
        headers=headers_admin
    )

    assert resposta.status_code == 200
    assert resposta.json()["id"] == estudante_id


# TESTE 04 — UPDATE: atualizar estudante
def test_atualizar_estudante(
    cliente,
    headers_admin
):

    cadastro = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    estudante_id = cadastro.json()["id"]

    novos_dados = {
        "nome": "Maria Souza",
        "email": "maria.souza@example.com"
    }

    resposta = cliente.put(
        f"/estudantes/{estudante_id}",
        headers=headers_admin,
        json=novos_dados
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Maria Souza"


# TESTE 05 — DELETE: excluir estudante
def test_excluir_estudante(
    cliente,
    headers_admin
):

    cadastro = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    estudante_id = cadastro.json()["id"]

    resposta = cliente.delete(
        f"/estudantes/{estudante_id}",
        headers=headers_admin
    )

    assert resposta.status_code == 200

    assert resposta.json()["mensagem"] == (
        "Estudante excluído."
    )

    consulta = cliente.get(
        f"/estudantes/{estudante_id}",
        headers=headers_admin
    )

    assert consulta.status_code == 404


# TESTE 06 — Impedir cadastro sem autenticação
def test_cadastrar_sem_autenticacao(cliente):

    resposta = cliente.post(
        "/estudantes",
        json=dados_estudante()
    )

    assert resposta.status_code == 401


# TESTE 07 — Usuário de consulta não pode cadastrar
def test_consulta_nao_pode_cadastrar(
    cliente,
    headers_consulta
):

    resposta = cliente.post(
        "/estudantes",
        headers=headers_consulta,
        json=dados_estudante()
    )

    assert resposta.status_code == 403


# TESTE 08 — Usuário de consulta não pode atualizar
def test_consulta_nao_pode_atualizar(
    cliente,
    headers_admin,
    headers_consulta
):

    cadastro = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    estudante_id = cadastro.json()["id"]

    resposta = cliente.put(
        f"/estudantes/{estudante_id}",
        headers=headers_consulta,
        json={
            "nome": "Alteração não permitida",
            "email": "alteracao@example.com"
        }
    )

    assert resposta.status_code == 403


# TESTE 09 — Usuário de consulta não pode excluir
def test_consulta_nao_pode_excluir(
    cliente,
    headers_admin,
    headers_consulta
):

    cadastro = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    estudante_id = cadastro.json()["id"]

    resposta = cliente.delete(
        f"/estudantes/{estudante_id}",
        headers=headers_consulta
    )

    assert resposta.status_code == 403


# TESTE 10 — Estudante inexistente
def test_buscar_estudante_inexistente(
    cliente,
    headers_admin
):

    resposta = cliente.get(
        "/estudantes/99999",
        headers=headers_admin
    )

    assert resposta.status_code == 404


# TESTE 11 — Atualizar estudante inexistente
def test_atualizar_estudante_inexistente(
    cliente,
    headers_admin
):

    resposta = cliente.put(
        "/estudantes/99999",
        headers=headers_admin,
        json=dados_estudante()
    )

    assert resposta.status_code == 404


# TESTE 12 — Excluir estudante inexistente
def test_excluir_estudante_inexistente(
    cliente,
    headers_admin
):

    resposta = cliente.delete(
        "/estudantes/99999",
        headers=headers_admin
    )

    assert resposta.status_code == 404


# TESTE 13 — Impedir e-mail duplicado
def test_email_duplicado(
    cliente,
    headers_admin
):

    cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    resposta = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json=dados_estudante()
    )

    assert resposta.status_code == 409


# TESTE 14 — Validar e-mail inválido
def test_email_invalido(
    cliente,
    headers_admin
):

    resposta = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json={
            "nome": "João Silva",
            "email": "email_invalido"
        }
    )

    assert resposta.status_code == 422


# TESTE 15 — Validar nome muito curto
def test_nome_invalido(
    cliente,
    headers_admin
):

    resposta = cliente.post(
        "/estudantes",
        headers=headers_admin,
        json={
            "nome": "A",
            "email": "joao@example.com"
        }
    )

    assert resposta.status_code == 422


# TESTE 16 — Validar paginação
def test_paginacao_invalida(
    cliente,
    headers_admin
):

    resposta = cliente.get(
        "/estudantes?limite=150",
        headers=headers_admin
    )

    assert resposta.status_code == 422


# TESTE 17 — Paginação válida
def test_paginacao_valida(
    cliente,
    headers_admin
):

    for numero in range(3):

        cliente.post(
            "/estudantes",
            headers=headers_admin,
            json={
                "nome": f"Estudante {numero}",
                "email": f"estudante{numero}@example.com"
            }
        )

    resposta = cliente.get(
        "/estudantes?limite=2&deslocamento=1",
        headers=headers_admin
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 2
    assert resposta.json()[0]["nome"] == "Estudante 1"


# TESTE 18 — Impedir exclusão com matrícula
def test_excluir_estudante_com_matricula(
    cliente,
    headers_admin,
    db_session
):

    from app.models import (
        Estudante, Curso, Disciplina, Matricula
    )

    estudante = Estudante(
        nome="Carlos Silva",
        email="carlos@example.com"
    )

    curso = Curso(
        nome="Informática",
        descricao="Curso de informática"
    )

    db_session.add_all([estudante, curso])
    db_session.flush()

    disciplina = Disciplina(
        nome="Programação",
        carga_horaria=80,
        curso_id=curso.id
    )

    db_session.add(disciplina)
    db_session.flush()

    matricula = Matricula(
        estudante_id=estudante.id,
        disciplina_id=disciplina.id
    )

    db_session.add(matricula)
    db_session.commit()

    resposta = cliente.delete(
        f"/estudantes/{estudante.id}",
        headers=headers_admin
    )

    assert resposta.status_code == 409
