
# ============================================================
# ARQUIVO: tests/test_relacionamentos.py
# RESPONSABILIDADE: testar relacionamentos ORM
# ============================================================

from app.models import (
    Estudante,
    Curso,
    Disciplina,
    Matricula
)


# TESTE 01 — Curso possui várias disciplinas
def test_curso_e_disciplinas(db_session):

    curso = Curso(
        nome="Desenvolvimento de Sistemas"
    )

    db_session.add(curso)
    db_session.flush()

    disciplina1 = Disciplina(
        nome="Python",
        carga_horaria=80,
        curso=curso
    )

    disciplina2 = Disciplina(
        nome="Banco de Dados",
        carga_horaria=60,
        curso=curso
    )

    db_session.add_all([disciplina1, disciplina2])
    db_session.commit()

    assert len(curso.disciplinas) == 2


# TESTE 02 — Disciplina pertence a um curso
def test_disciplina_e_curso(db_session):

    curso = Curso(nome="Informática")

    disciplina = Disciplina(
        nome="Programação",
        carga_horaria=80,
        curso=curso
    )

    db_session.add(disciplina)
    db_session.commit()

    assert disciplina.curso.nome == "Informática"


# TESTE 03 — Estudante possui várias matrículas
def test_estudante_e_matriculas(db_session):

    estudante = Estudante(
        nome="Ana Souza",
        email="ana@example.com"
    )

    curso = Curso(nome="Desenvolvimento")

    disciplina1 = Disciplina(
        nome="Python",
        carga_horaria=80,
        curso=curso
    )

    disciplina2 = Disciplina(
        nome="SQL",
        carga_horaria=60,
        curso=curso
    )

    matricula1 = Matricula(
        estudante=estudante,
        disciplina=disciplina1
    )

    matricula2 = Matricula(
        estudante=estudante,
        disciplina=disciplina2
    )

    db_session.add_all([
        estudante,
        curso,
        disciplina1,
        disciplina2,
        matricula1,
        matricula2
    ])

    db_session.commit()

    assert len(estudante.matriculas) == 2


# TESTE 04 — Matrícula identifica estudante
def test_matricula_identifica_estudante(db_session):

    estudante = Estudante(
        nome="Pedro Souza",
        email="pedro@example.com"
    )

    curso = Curso(nome="Programação")

    disciplina = Disciplina(
        nome="Python",
        carga_horaria=80,
        curso=curso
    )

    matricula = Matricula(
        estudante=estudante,
        disciplina=disciplina
    )

    db_session.add(matricula)
    db_session.commit()

    assert matricula.estudante.nome == "Pedro Souza"


# TESTE 05 — Matrícula identifica disciplina
def test_matricula_identifica_disciplina(db_session):

    estudante = Estudante(
        nome="João Souza",
        email="joao@example.com"
    )

    curso = Curso(nome="Sistemas")

    disciplina = Disciplina(
        nome="Banco de Dados",
        carga_horaria=80,
        curso=curso
    )

    matricula = Matricula(
        estudante=estudante,
        disciplina=disciplina
    )

    db_session.add(matricula)
    db_session.commit()

    assert (
        matricula.disciplina.nome == "Banco de Dados"
    )
