
# ============================================================
# ARQUIVO: tests/test_schemas.py
# RESPONSABILIDADE: testar validações Pydantic
# ============================================================

import pytest

from pydantic import ValidationError

from app.schemas import (
    EstudanteEntrada,
    CursoEntrada,
    DisciplinaEntrada,
    MatriculaEntrada
)


# TESTE 01 — Estudante válido
def test_estudante_valido():

    estudante = EstudanteEntrada(
        nome="Maria Silva",
        email="maria@example.com"
    )

    assert estudante.nome == "Maria Silva"


# TESTE 02 — E-mail inválido
def test_estudante_email_invalido():

    with pytest.raises(ValidationError):

        EstudanteEntrada(
            nome="Maria Silva",
            email="email_invalido"
        )


# TESTE 03 — Nome de curso muito curto
def test_curso_nome_invalido():

    with pytest.raises(ValidationError):

        CursoEntrada(nome="A")


# TESTE 04 — Carga horária inválida
def test_disciplina_carga_invalida():

    with pytest.raises(ValidationError):

        DisciplinaEntrada(
            nome="Python",
            carga_horaria=0,
            curso_id=1
        )


# TESTE 05 — Carga horária acima do limite
def test_disciplina_carga_acima_limite():

    with pytest.raises(ValidationError):

        DisciplinaEntrada(
            nome="Python",
            carga_horaria=3000,
            curso_id=1
        )


# TESTE 06 — Curso inexistente como identificador válido
# O schema valida o formato do ID, não a existência no banco.
def test_disciplina_id_positivo():

    disciplina = DisciplinaEntrada(
        nome="Python",
        carga_horaria=80,
        curso_id=1
    )

    assert disciplina.curso_id == 1


# TESTE 07 — Identificador de estudante inválido
def test_matricula_estudante_invalido():

    with pytest.raises(ValidationError):

        MatriculaEntrada(
            estudante_id=0,
            disciplina_id=1
        )


# TESTE 08 — Identificador de disciplina inválido
def test_matricula_disciplina_invalida():

    with pytest.raises(ValidationError):

        MatriculaEntrada(
            estudante_id=1,
            disciplina_id=-1
        )
