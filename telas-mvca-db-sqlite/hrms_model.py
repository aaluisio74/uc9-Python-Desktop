import sqlite3

class FuncionarioModel:
    def __init__(self, db_name="hrms.db"):
        self.db_name = db_name
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabela(self):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS funcionarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        matricula TEXT UNIQUE NOT NULL,
                        nome TEXT NOT NULL,
                        cargo TEXT NOT NULL,
                        departamento TEXT
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def inserir(self, matricula, nome, cargo, departamento=""):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO funcionarios (matricula, nome, cargo, departamento)
                    VALUES (?, ?, ?, ?)
                """, (matricula, nome, cargo, departamento))
                conn.commit()
                return True, "Colaborador cadastrado com sucesso no banco SQLite!"
        except sqlite3.IntegrityError:
            return False, "Erro: Matrícula já cadastrada no sistema."
        except sqlite3.Error as e:
            return False, f"Erro no Banco de Dados: {e}"

    def listar_todos(self, filtro=""):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                if filtro:
                    query = """
                        SELECT id, matricula, nome, cargo, departamento 
                        FROM funcionarios 
                        WHERE matricula LIKE ? OR nome LIKE ? OR cargo LIKE ?
                        ORDER BY nome
                    """
                    param = f"%{filtro}%"
                    cursor.execute(query, (param, param, param))
                else:
                    cursor.execute("SELECT id, matricula, nome, cargo, departamento FROM funcionarios ORDER BY nome")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar registros: {e}")
            return []

    def atualizar(self, id_reg, matricula, nome, cargo, departamento=""):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE funcionarios 
                    SET matricula = ?, nome = ?, cargo = ?, departamento = ?
                    WHERE id = ?
                """, (matricula, nome, cargo, departamento, id_reg))
                conn.commit()
                return True, "Registro atualizado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Erro: A nova matrícula já pertence a outro colaborador."
        except sqlite3.Error as e:
            return False, f"Erro ao atualizar: {e}"

    def excluir(self, id_reg):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_reg,))
                conn.commit()
                return True, "Registro excluído com sucesso!"
        except sqlite3.Error as e:
            return False, f"Erro ao excluir: {e}"
