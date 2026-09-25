import sqlite3

class AppModel:
    def __init__(self, db_name="sistema_corporativo.db"):
        self.db_name = db_name
        self.criar_tabelas()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def criar_tabelas(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Tabela referente à Atividade 2
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS colaboradores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        matricula TEXT NOT NULL UNIQUE,
                        nome TEXT NOT NULL,
                        cargo TEXT NOT NULL,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Tabela de suporte para salvar os lotes processados (Atividade 4)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS lotes_processados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        volume INTEGER NOT NULL,
                        ambiente TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

    # --- Métodos para Colaboradores ---
    def inserir_colaborador(self, matricula, nome, cargo):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO colaboradores (matricula, nome, cargo) VALUES (?, ?, ?)",
                (matricula, nome, cargo)
            )
            conn.commit()

    def atualizar_colaborador(self, colab_id, matricula, nome, cargo):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE colaboradores SET matricula = ?, nome = ?, cargo = ? WHERE id = ?",
                (matricula, nome, cargo, colab_id)
            )
            conn.commit()

    def deletar_colaborador(self, colab_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM colaboradores WHERE id = ?", (colab_id,))
            conn.commit()

    def buscar_colaboradores(self, termo_pesquisa=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if termo_pesquisa:
                query = """
                    SELECT id, matricula, nome, cargo 
                    FROM colaboradores 
                    WHERE matricula LIKE ? OR nome LIKE ? OR cargo LIKE ?
                    ORDER BY nome
                """
                param = f"%{termo_pesquisa}%"
                cursor.execute(query, (param, param, param))
            else:
                cursor.execute("SELECT id, matricula, nome, cargo FROM colaboradores ORDER BY nome")
            return cursor.fetchall()

    # --- Métodos para Central de Lotes ---
    def registrar_lote(self, volume, ambiente, tipo):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO lotes_processados (volume, ambiente, tipo) VALUES (?, ?, ?)",
                (volume, ambiente, tipo)
            )
            conn.commit()

    def buscar_lotes(self, termo_pesquisa=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if termo_pesquisa:
                query = """
                    SELECT id, volume, ambiente, tipo, data_execucao 
                    FROM lotes_processados 
                    WHERE ambiente LIKE ? OR tipo LIKE ? OR CAST(volume AS TEXT) LIKE ?
                    ORDER BY id DESC
                """
                param = f"%{termo_pesquisa}%"
                cursor.execute(query, (param, param, param))
            else:
                cursor.execute("SELECT id, volume, ambiente, tipo, data_execucao FROM lotes_processados ORDER BY id DESC")
            return cursor.fetchall()

    def atualizar_lote(self, lote_id, volume, ambiente, tipo):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE lotes_processados SET volume = ?, ambiente = ?, tipo = ? WHERE id = ?",
                (volume, ambiente, tipo, lote_id)
            )
            conn.commit()

    def deletar_lote(self, lote_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lotes_processados WHERE id = ?", (lote_id,))
            conn.commit()
