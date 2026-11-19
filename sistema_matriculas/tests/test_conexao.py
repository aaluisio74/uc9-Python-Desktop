
# ============================================================
# ARQUIVO: tests/test_conexao.py
# RESPONSABILIDADE: verificar banco e tabelas
# ============================================================

from sqlalchemy import inspect


def test_conexao_com_banco_temporario(ambiente_teste):

    assert ambiente_teste is not None

    assert ambiente_teste.url.database.endswith(
        "teste_matriculas.db"
    )


def test_tabelas_foram_criadas(ambiente_teste):

    inspetor = inspect(ambiente_teste)

    tabelas = inspetor.get_table_names()

    assert "estudantes" in tabelas
    assert "cursos" in tabelas
    assert "disciplinas" in tabelas
    assert "matriculas" in tabelas
    assert "usuarios" in tabelas
