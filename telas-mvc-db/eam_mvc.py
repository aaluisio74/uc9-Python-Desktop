import sqlite3
import tkinter as tk
from tkinter import messagebox


# ==============================================================================
# MODEL: Responsável pelos Dados e Regras do SQLite
# ==============================================================================
class AtivoModel:
    def __init__(self, db_name="eam_mvc_ativos.db"):
        self.db_name = db_name
        self.inicializar_banco()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def inicializar_banco(self):
        """Cria a tabela de ativos e insere dados iniciais caso esteja vazia."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ativos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        status TEXT NOT NULL CHECK(status IN ('Em Operacao', 'Em Manutencao', 'Falha Critica'))
                    )
                """)

                # Verifica se a tabela já contém registros
                cursor.execute("SELECT COUNT(*) FROM ativos")
                total = cursor.fetchone()[0]

                # Popula o banco com a amostragem inicial do enunciado se estiver vazio
                if total == 0:
                    dados_iniciais = (
                        [("Equipamento Operacional", "Em Operacao")] * 1180 +
                        [("Equipamento em Manutenção", "Em Manutencao")] * 54 +
                        [("Equipamento com Falha", "Falha Critica")] * 14
                    )
                    cursor.executemany(
                        "INSERT INTO ativos (nome, status) VALUES (?, ?)", dados_iniciais
                    )
                    conn.commit()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao inicializar o banco: {erro}")

    def obter_metricas_kpi(self):
        """Consulta os indicadores (KPIs) diretamente via SQL no banco SQLite."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM ativos")
                total = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM ativos WHERE status = 'Em Operacao'")
                operacao = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM ativos WHERE status = 'Em Manutencao'")
                manutencao = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM ativos WHERE status = 'Falha Critica'")
                criticos = cursor.fetchone()[0]

                return {
                    "total": f"{total:,}",
                    "operacao": f"{operacao:,}",
                    "manutencao": f"{manutencao:,}",
                    "criticos": f"{criticos:,}"
                }
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de Consulta", f"Falha ao consultar indicadores: {erro}")
            return {"total": "0", "operacao": "0", "manutencao": "0", "criticos": "0"}


# ==============================================================================
# VIEW: Responsável pela Interface Gráfica (Tkinter)
# ==============================================================================
class DashboardView:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Controle - Gestão de Ativos Corporativos (EAM)")
        self.root.configure(bg="#0f172a")  # Dark Slate Corporativo
        self.root.resizable(False, False)

        # Centralização da janela
        largura_j, altura_j = 500, 350
        largura_s = self.root.winfo_screenwidth()
        altura_s = self.root.winfo_screenheight()
        pos_x = (largura_s - largura_j) // 2
        pos_y = (altura_s - altura_j) // 2
        self.root.geometry(f"{largura_j}x{altura_j}+{pos_x}+{pos_y}")

        self.kpi_labels = {}
        self.criar_interface()

    def criar_interface(self):
        # Cabeçalho do Dashboard
        header = tk.Frame(self.root, bg="#1e293b", height=60)
        header.pack(fill="x", side="top")
        
        lbl_titulo = tk.Label(
            header,
            text="SISTEMA DE GESTÃO DE ATIVOS & EQUIPAMENTOS",
            font=("Segoe UI", 12, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        lbl_titulo.pack(pady=15)

        # Container de Métricas (KPIs)
        frame_kpi = tk.Frame(self.root, bg="#0f172a")
        frame_kpi.pack(expand=True, fill="both", padx=30, pady=20)
        
        frame_kpi.grid_columnconfigure(0, weight=1)
        frame_kpi.grid_columnconfigure(1, weight=1)

        # Criação dos Cartões de KPIs
        self.kpi_labels["total"] = self._criar_kpi_card(frame_kpi, "Total de Ativos", "#38bdf8", 0, 0)
        self.kpi_labels["operacao"] = self._criar_kpi_card(frame_kpi, "Em Operação", "#4ade80", 0, 1)
        self.kpi_labels["manutencao"] = self._criar_kpi_card(frame_kpi, "Em Manutenção", "#fbbf24", 1, 0)
        self.kpi_labels["criticos"] = self._criar_kpi_card(frame_kpi, "Falhas Críticas", "#f87171", 1, 1)

        # Rodapé de Status do Sistema
        self.footer = tk.Label(
            self.root,
            text="Status do Sistema: Operacional | Úm. Sincronização: Banco SQLite Ativo",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0f172a"
        )
        self.footer.pack(side="bottom", pady=10)

    def _criar_kpi_card(self, parent, titulo, cor_valor, row, col):
        card = tk.Frame(parent, bg="#1e293b", bd=1, relief="solid")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        tk.Label(card, text=titulo, font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(pady=(10, 2))
        
        lbl_valor = tk.Label(card, text="-", font=("Segoe UI", 16, "bold"), fg=cor_valor, bg="#1e293b")
        lbl_valor.pack(pady=(0, 10))
        
        return lbl_valor

    def atualizar_kpis(self, metricas):
        """Atualiza os valores dos rótulos dos KPIs na View."""
        self.kpi_labels["total"].config(text=metricas["total"])
        self.kpi_labels["operacao"].config(text=metricas["operacao"])
        self.kpi_labels["manutencao"].config(text=metricas["manutencao"])
        self.kpi_labels["criticos"].config(text=metricas["criticos"])


# ==============================================================================
# CONTROLLER: Orquestra a comunicação entre a View e o Model
# ==============================================================================
class DashboardController:
    def __init__(self, root):
        self.model = AtivoModel()
        self.view = DashboardView(root)
        self.carregar_dados()

    def carregar_dados(self):
        """Obtém as métricas do banco de dados e repassa para a View."""
        metricas = self.model.obter_metricas_kpi()
        self.view.atualizar_kpis(metricas)


# ==============================================================================
# EXECUÇÃO DA APLICAÇÃO
# ==============================================================================
if __name__ == "__main__":
    janela = tk.Tk()
    app = DashboardController(janela)
    janela.mainloop()
