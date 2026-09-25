import sqlite3

class BonificacaoModel:
    def __init__(self, db_name="bonificacoes.db"):
        self.db_name = db_name
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabela(self):
        """Cria a tabela no SQLite caso ela não exista."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bonificacoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        colaborador TEXT NOT NULL,
                        salario REAL NOT NULL,
                        meta REAL NOT NULL,
                        valor_bonus REAL NOT NULL,
                        categoria TEXT NOT NULL,
                        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar banco de dados: {e}")

    @staticmethod
    def calcular_fator_e_categoria(meta):
        """Calcula a faixa e a bonificação baseada nas regras de negócio."""
        if meta < 80:
            return 0.0, "Meta Não Atingida (Sem Bônus)", "#dc2626"
        elif meta < 100:
            return 0.5, "Atingimento Parcial (Bônus 50%)", "#d97706"
        elif meta <= 120:
            return 1.0, "Meta Integral Atingida (Bônus 100%)", "#16a34a"
        elif meta <= 150:
            return 1.5, "Superação de Metas (Bônus 150%)", "#2563eb"
        else:
            return 2.0, "Performance Excepcional Executiva (Bônus 200%)", "#7c3aed"

    def inserir_registro(self, colaborador, salario, meta, valor_bonus, categoria):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bonificacoes (colaborador, salario, meta, valor_bonus, categoria)
                VALUES (?, ?, ?, ?, ?)
            """, (colaborador, salario, meta, valor_bonus, categoria))
            conn.commit()

    def listar_registros(self, filtro_nome=""):
        with self.conectar() as conn:
            cursor = conn.cursor()
            if filtro_nome:
                cursor.execute("""
                    SELECT id, colaborador, salario, meta, valor_bonus, categoria 
                    FROM bonificacoes 
                    WHERE colaborador LIKE ? 
                    ORDER BY id DESC
                """, (f"%{filtro_nome}%",))
            else:
                cursor.execute("""
                    SELECT id, colaborador, salario, meta, valor_bonus, categoria 
                    FROM bonificacoes 
                    ORDER BY id DESC
                """)
            return cursor.fetchall()

    def atualizar_registro(self, registro_id, colaborador, salario, meta, valor_bonus, categoria):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE bonificacoes 
                SET colaborador = ?, salario = ?, meta = ?, valor_bonus = ?, categoria = ?
                WHERE id = ?
            """, (colaborador, salario, meta, valor_bonus, categoria, registro_id))
            conn.commit()

    def excluir_registro(self, registro_id):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bonificacoes WHERE id = ?", (registro_id,))
            conn.commit()
