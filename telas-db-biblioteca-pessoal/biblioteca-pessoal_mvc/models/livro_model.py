import sqlite3

class LivroModel:
    """Model: operações de persistência dos livros no SQLite."""
    def __init__(self, banco="biblioteca.db"):
        self.banco = banco
        with self.conectar() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL, autor TEXT, ano INTEGER,
                status TEXT NOT NULL DEFAULT 'Não Lido')""")

    def conectar(self):
        return sqlite3.connect(self.banco)

    def adicionar(self, titulo, autor, ano, status):
        with self.conectar() as con:
            con.execute("INSERT INTO livros (titulo, autor, ano, status) VALUES (?, ?, ?, ?)",
                        (titulo, autor or None, ano, status))

    def listar(self):
        with self.conectar() as con:
            return con.execute("SELECT id, titulo, autor, ano, status FROM livros ORDER BY titulo COLLATE NOCASE").fetchall()

    def buscar_por_id(self, livro_id):
        with self.conectar() as con:
            return con.execute("SELECT id, titulo, autor, ano, status FROM livros WHERE id = ?", (livro_id,)).fetchone()

    def atualizar_status(self, livro_id, status):
        with self.conectar() as con:
            con.execute("UPDATE livros SET status = ? WHERE id = ?", (status, livro_id))

    def remover(self, livro_id):
        with self.conectar() as con:
            con.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
