
# ============================================================
# ARQUIVO: tests/test_restricoes.py
# RESPONSABILIDADE: testar restrições SQLAlchemy
# ============================================================

import pytest

from sqlalchemy.exc import IntegrityError

from app.models import (
    Estudante,
    Curso,
    Disciplina,
    Matricula,
    Usuario
)


# TESTE 01 — E-mail único
def test_email_unico(db_session):

    estudante1 = Estudante(
        nome="Ana",
        email="ana@example.com"
    )

    estudante2 = Estudante(
        nome="Maria",
        email="ana@example.com"
    )

    db_session.add(estudante1)
    db_session.commit()

    db_session.add(estudante2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 02 — Nome do curso único
def test_nome_curso_unico(db_session):

    curso1 = Curso(nome="Informática")
    curso2 = Curso(nome="Informática")

    db_session.add(curso1)
    db_session.commit()

    db_session.add(curso2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 03 — Disciplina única dentro do curso
def test_disciplina_unica_no_curso(db_session):

    curso = Curso(nome="Desenvolvimento")
    db_session.add(curso)
    db_session.flush()

    disciplina1 = Disciplina(
        nome="Python",
        carga_horaria=80,
        curso_id=curso.id
    )

    disciplina2 = Disciplina(
        nome="Python",
        carga_horaria=100,
        curso_id=curso.id
    )

    db_session.add(disciplina1)
    db_session.commit()

    db_session.add(disciplina2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 04 — Carga horária positiva
def test_carga_horaria_invalida(db_session):

    curso = Curso(nome="Informática")

    db_session.add(curso)
    db_session.flush()

    disciplina = Disciplina(
        nome="Programação",
        carga_horaria=0,
        curso_id=curso.id
    )

    db_session.add(disciplina)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 05 — Matrícula duplicada
def test_matricula_duplicada(db_session):

    estudante = Estudante(
        nome="Carlos",
        email="carlos@example.com"
    )

    curso = Curso(nome="Sistemas")

    disciplina = Disciplina(
        nome="Banco de Dados",
        carga_horaria=80,
        curso=curso
    )

    db_session.add_all([
        estudante,
        curso,
        disciplina
    ])

    db_session.flush()

    matricula1 = Matricula(
        estudante_id=estudante.id,
        disciplina_id=disciplina.id
    )

    db_session.add(matricula1)
    db_session.commit()

    matricula2 = Matricula(
        estudante_id=estudante.id,
        disciplina_id=disciplina.id
    )

    db_session.add(matricula2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 06 — Status de matrícula inválido
def test_status_matricula_invalido(db_session):

    estudante = Estudante(
        nome="João",
        email="joao@example.com"
    )

    curso = Curso(nome="Programação")

    disciplina = Disciplina(
        nome="Python",
        carga_horaria=80,
        curso=curso
    )

    db_session.add_all([
        estudante,
        curso,
        disciplina
    ])

    db_session.flush()

    matricula = Matricula(
        estudante_id=estudante.id,
        disciplina_id=disciplina.id,
        status="pendente"
    )

    db_session.add(matricula)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 07 — Papel de usuário inválido
def test_papel_usuario_invalido(db_session):

    usuario = Usuario(
        username="usuario_invalido",
        senha_hash="hash_teste",
        papel="supervisor"
    )

    db_session.add(usuario)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 08 — Chave estrangeira inválida
def test_matricula_com_estudante_inexistente(
    db_session
):

    curso = Curso(nome="Informática")

    db_session.add(curso)
    db_session.flush()

    disciplina = Disciplina(
        nome="Python",
        carga_horaria=80,
        curso_id=curso.id
    )

    db_session.add(disciplina)
    db_session.flush()

    matricula = Matricula(
        estudante_id=99999,
        disciplina_id=disciplina.id
    )

    db_session.add(matricula)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


# TESTE 09 — Username único
def test_username_unico(db_session):

    usuario1 = Usuario(
        username="aluno",
        senha_hash="hash1",
        papel="consulta"
    )

    usuario2 = Usuario(
        username="aluno",
        senha_hash="hash2",
        papel="consulta"
    )

    db_session.add(usuario1)
    db_session.commit()

    db_session.add(usuario2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
