import sqlite3

# 1. Conectar ao banco de dados.
# O arquivo será criado automaticamente se não existir.
conexao = sqlite3.connect("escola.db")
cursor = conexao.cursor()

try:
    # 2. Criar a tabela, caso ainda não exista.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            curso TEXT NOT NULL
        )
    """)

    # 3. Dados recebidos para importação.
    alunos = [
        ("Abraão", 16, "Informática"),
        ("Isaque", 17, "Informática"),
        ("Jacó", 16, "Administração"),
        ("Judá", 18, "Informática"),
        ("Farés", 17, "Administração"),
        ("Esrom", 16, "Administração"),
        ("Arão", 18, "Informática"),
        ("Aminadabe", 17, "Administração"),
        ("Naassom", 16, "Administração"),
        ("Salmon", 16, "Informática"),
        ("Boaz", 17, "Informática"),
        ("Obede", 16, "Administração"),
        ("Jessé", 18, "Informática"),
        ("Davi", 17, "Administração")
    ]

    # 4. Validar os registros antes da gravação.
    alunos_validos = []

    for nome, idade, curso in alunos:
        if (
            nome.strip()
            and isinstance(idade, int)
            and 14 <= idade <= 100
            and curso.strip()
        ):
            alunos_validos.append(
                (nome.strip(), idade, curso.strip())
            )

    # 5. Inserir vários registros em lote.
    cursor.executemany("""
        INSERT INTO alunos (nome, idade, curso)
        VALUES (?, ?, ?)
    """, alunos_validos)

    # 6. Confirmar a transação.
    conexao.commit()

    print(f"Alunos importados: {len(alunos_validos)}")

    # 7. Consultar os dados cadastrados.
    cursor.execute("""
        SELECT id, nome, idade, curso
        FROM alunos
        ORDER BY id
    """)

    print("\nAlunos cadastrados:")

    for aluno in cursor.fetchall():
        print(aluno)

except Exception as erro:
    # Desfazer as alterações pendentes em caso de falha.
    conexao.rollback()
    print(f"Erro na importação: {erro}")

finally:
    # 8. Encerrar a conexão.
    conexao.close()
