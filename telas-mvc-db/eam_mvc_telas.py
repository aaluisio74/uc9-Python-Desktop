import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


# ==============================================================================
# MODEL: Banco de Dados SQLite & Regras de Negócio
# ==============================================================================
class AtivoModel:
    def __init__(self, db_name="eam_mvc_telas_sistema.db"):
        self.db_name = db_name
        self.inicializar_banco()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def inicializar_banco(self):
        """Cria a tabela e insere dados de amostragem inicial caso vazia."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ativos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        status TEXT NOT NULL CHECK(status IN ('Em Operacao', 'Em Manutencao', 'Falha Critica'))
                    )
                """)
                cursor.execute("SELECT COUNT(*) FROM ativos")
                if cursor.fetchone()[0] == 0:
                    dados_iniciais = [
                        ("Torno CNC - Unidade 01", "Usinagem", "Em Operacao"),
                        ("Prensa Hidráulica 50T", "Estamparia", "Em Operacao"),
                        ("Compressor Industrial B2", "Utilidades", "Em Manutencao"),
                        ("Gerador de Emergência G1", "Elétrica", "Falha Critica"),
                        ("Robô Soldador Kuka", "Automação", "Em Operacao")
                    ]
                    cursor.executemany(
                        "INSERT INTO ativos (nome, categoria, status) VALUES (?, ?, ?)", 
                        dados_iniciais
                    )
                    conn.commit()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de Banco de Dados", f"Falha na inicialização: {erro}")

    def obter_kpis(self):
        """Consulta as contagens agregadas para o Dashboard."""
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
            messagebox.showerror("Erro SQL", f"Erro ao calcular KPIs: {erro}")
            return {"total": "0", "operacao": "0", "manutencao": "0", "criticos": "0"}

    def listar_todos(self):
        """Retorna todos os registros cadastrados."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, categoria, status FROM ativos ORDER BY id DESC")
                return cursor.fetchall()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro SQL", f"Erro ao consultar ativos: {erro}")
            return []

    def inserir(self, nome, categoria, status):
        """Insere um novo ativo."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO ativos (nome, categoria, status) VALUES (?, ?, ?)",
                    (nome, categoria, status)
                )
                conn.commit()
                return True
        except sqlite3.Error as erro:
            messagebox.showerror("Erro SQL", f"Erro ao cadastrar: {erro}")
            return False

    def atualizar(self, id_ativo, nome, categoria, status):
        """Atualiza os dados de um ativo existente."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE ativos SET nome = ?, categoria = ?, status = ? WHERE id = ?",
                    (nome, categoria, status, id_ativo)
                )
                conn.commit()
                return True
        except sqlite3.Error as erro:
            messagebox.showerror("Erro SQL", f"Erro ao atualizar: {erro}")
            return False

    def excluir(self, id_ativo):
        """Exclui um ativo do banco de dados pelo ID."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ativos WHERE id = ?", (id_ativo,))
                conn.commit()
                return True
        except sqlite3.Error as erro:
            messagebox.showerror("Erro SQL", f"Erro ao excluir: {erro}")
            return False


# ==============================================================================
# VIEW 1: Dashboard EAM (Atividade 1)
# ==============================================================================
class DashboardView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Painel de Controle - Gestão de Ativos Corporativos (EAM)")
        self.configure(bg="#0f172a")  # Dark Slate Corporativo
        self.resizable(False, False)

        # Centralização de janela (500x350)
        largura_j, altura_j = 500, 350
        pos_x = (self.winfo_screenwidth() - largura_j) // 2
        pos_y = (self.winfo_screenheight() - altura_j) // 2
        self.geometry(f"{largura_j}x{altura_j}+{pos_x}+{pos_y}")

        self.kpi_labels = {}
        self.criar_interface()
        self.atualizar_dados()

    def criar_interface(self):
        # Cabeçalho
        header = tk.Frame(self, bg="#1e293b", height=60)
        header.pack(fill="x", side="top")
        
        lbl_titulo = tk.Label(
            header,
            text="SISTEMA DE GESTÃO DE ATIVOS & EQUIPAMENTOS",
            font=("Segoe UI", 12, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        lbl_titulo.pack(pady=15)

        # Container dos KPIs
        frame_kpi = tk.Frame(self, bg="#0f172a")
        frame_kpi.pack(expand=True, fill="both", padx=30, pady=20)
        frame_kpi.grid_columnconfigure(0, weight=1)
        frame_kpi.grid_columnconfigure(1, weight=1)

        self.kpi_labels["total"] = self._criar_kpi_card(frame_kpi, "Total de Ativos", "#38bdf8", 0, 0)
        self.kpi_labels["operacao"] = self._criar_kpi_card(frame_kpi, "Em Operação", "#4ade80", 0, 1)
        self.kpi_labels["manutencao"] = self._criar_kpi_card(frame_kpi, "Em Manutenção", "#fbbf24", 1, 0)
        self.kpi_labels["criticos"] = self._criar_kpi_card(frame_kpi, "Falhas Críticas", "#f87171", 1, 1)

        # Rodapé
        footer = tk.Label(
            self,
            text="Status do Sistema: Operacional | Banco SQLite Sincronizado",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0f172a"
        )
        footer.pack(side="bottom", pady=10)

    def _criar_kpi_card(self, parent, titulo, cor_valor, row, col):
        card = tk.Frame(parent, bg="#1e293b", bd=1, relief="solid")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        tk.Label(card, text=titulo, font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(pady=(10, 2))
        lbl_valor = tk.Label(card, text="-", font=("Segoe UI", 16, "bold"), fg=cor_valor, bg="#1e293b")
        lbl_valor.pack(pady=(0, 10))
        return lbl_valor

    def atualizar_dados(self):
        metricas = self.controller.model.obter_kpis()
        self.kpi_labels["total"].config(text=metricas["total"])
        self.kpi_labels["operacao"].config(text=metricas["operacao"])
        self.kpi_labels["manutencao"].config(text=metricas["manutencao"])
        self.kpi_labels["criticos"].config(text=metricas["criticos"])


# ==============================================================================
# VIEW 2: Gestão CRUD (Entrada, Edição e Exclusão)
# ==============================================================================
class GestaoAtivosView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Gerenciamento de Ativos - SQLite")
        self.geometry("680x480")
        self.configure(bg="#f8fafc")

        self.id_selecionado = None
        self.criar_interface()
        self.carregar_tabela()

    def criar_interface(self):
        # Formulário de Entrada
        frame_form = tk.LabelFrame(self, text=" Dados do Equipamento / Ativo ", font=("Segoe UI", 10, "bold"), bg="#f8fafc", padx=10, pady=10)
        frame_form.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_form, text="Nome do Ativo:", bg="#f8fafc").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Categoria:", bg="#f8fafc").grid(row=0, column=2, sticky="w", pady=4, padx=(10, 0))
        self.entry_categoria = tk.Entry(frame_form, width=20)
        self.entry_categoria.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Status Operacional:", bg="#f8fafc").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_status = ttk.Combobox(
            frame_form, 
            values=["Em Operacao", "Em Manutencao", "Falha Critica"], 
            state="readonly",
            width=27
        )
        self.combo_status.grid(row=1, column=1, padx=5, pady=4)
        self.combo_status.current(0)

        # Botões de Ação
        frame_botoes = tk.Frame(frame_form, bg="#f8fafc")
        frame_botoes.grid(row=1, column=2, columnspan=2, sticky="e", pady=5)

        tk.Button(frame_botoes, text="Cadastrar", bg="#16a34a", fg="white", font=("Segoe UI", 9, "bold"), command=self.salvar).pack(side="left", padx=2)
        tk.Button(frame_botoes, text="Atualizar", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), command=self.atualizar).pack(side="left", padx=2)
        tk.Button(frame_botoes, text="Excluir", bg="#dc2626", fg="white", font=("Segoe UI", 9, "bold"), command=self.excluir).pack(side="left", padx=2)
        tk.Button(frame_botoes, text="Limpar", bg="#64748b", fg="white", font=("Segoe UI", 9), command=self.limpar_campos).pack(side="left", padx=2)

        # Tabela (Treeview) para exibição dos registros
        frame_tabela = tk.Frame(self, bg="#f8fafc")
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        colunas = ("id", "nome", "categoria", "status")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome do Ativo")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("status", text="Status Operacional")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nome", width=250)
        self.tree.column("categoria", width=150)
        self.tree.column("status", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.selecionar_registro)

    def carregar_tabela(self):
        """Limpa e recarrega os dados da tabela vindos do banco."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for ativo in self.controller.model.listar_todos():
            self.tree.insert("", "end", values=ativo)

    def selecionar_registro(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item[0], "values")
            self.id_selecionado = valores[0]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, valores[1])
            self.entry_categoria.delete(0, tk.END)
            self.entry_categoria.insert(0, valores[2])
            self.combo_status.set(valores[3])

    def limpar_campos(self):
        self.id_selecionado = None
        self.entry_nome.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.combo_status.current(0)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def salvar(self):
        nome = self.entry_nome.get().strip()
        cat = self.entry_categoria.get().strip()
        status = self.combo_status.get()

        if not nome or not cat:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        if self.controller.model.inserir(nome, cat, status):
            messagebox.showinfo("Sucesso", "Ativo cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_tabela()
            self.controller.notificar_atualizacao()

    def atualizar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um ativo na tabela para atualizar.")
            return

        nome = self.entry_nome.get().strip()
        cat = self.entry_categoria.get().strip()
        status = self.combo_status.get()

        if self.controller.model.atualizar(self.id_selecionado, nome, cat, status):
            messagebox.showinfo("Sucesso", "Ativo atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_tabela()
            self.controller.notificar_atualizacao()

    def excluir(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um ativo na tabela para excluir.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o ativo ID {self.id_selecionado}?"):
            if self.controller.model.excluir(self.id_selecionado):
                messagebox.showinfo("Sucesso", "Ativo excluído com sucesso!")
                self.limpar_campos()
                self.carregar_tabela()
                self.controller.notificar_atualizacao()


# ==============================================================================
# MAIN VIEW: Janela Principal com Barra de Menus
# ==============================================================================
class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Sistema Integrado EAM - Enterprise Asset Management")
        self.geometry("600x350")
        self.configure(bg="#1e293b")

        # Centralização da janela principal
        largura_j, altura_j = 600, 350
        pos_x = (self.winfo_screenwidth() - largura_j) // 2
        pos_y = (self.winfo_screenheight() - altura_j) // 2
        self.geometry(f"{largura_j}x{altura_j}+{pos_x}+{pos_y}")

        self.criar_menu()

        # Apresentação Central
        lbl_boas_vindas = tk.Label(
            self,
            text="SISTEMA CORPORATIVO DE GESTÃO DE ATIVOS",
            font=("Segoe UI", 14, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        lbl_boas_vindas.pack(pady=(100, 10))

        lbl_instrucao = tk.Label(
            self,
            text="Utilize a barra de menus superior para navegar entre\no Dashboard de Monitoramento e a Gestão de Registros.",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#1e293b"
        )
        lbl_instrucao.pack()

    def criar_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menu Módulos
        menu_modulos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Módulos", menu=menu_modulos)
        menu_modulos.add_command(label="Dashboard de Monitoramento (EAM)", command=self.controller.abrir_dashboard)
        menu_modulos.add_command(label="Gestão e Cadastro de Ativos (CRUD)", command=self.controller.abrir_gestao)
        menu_modulos.add_separator()
        menu_modulos.add_command(label="Sair", command=self.quit)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(
            label="Sobre", 
            command=lambda: messagebox.showinfo("Sobre", "Sistema EAM Corporativo v2.0\nDesenvolvido com Python, Tkinter e SQLite (Arquitetura MVC).")
        )


# ==============================================================================
# CONTROLLER: Orquestrador da Aplicação
# ==============================================================================
class AppController:
    def __init__(self):
        self.model = AtivoModel()
        self.main_view = MainView(self)
        self.win_dashboard = None
        self.win_gestao = None

    def abrir_dashboard(self):
        if self.win_dashboard is None or not self.win_dashboard.winfo_exists():
            self.win_dashboard = DashboardView(self.main_view, self)
        else:
            self.win_dashboard.lift()

    def abrir_gestao(self):
        if self.win_gestao is None or not self.win_gestao.winfo_exists():
            self.win_gestao = GestaoAtivosView(self.main_view, self)
        else:
            self.win_gestao.lift()

    def notificar_atualizacao(self):
        """Notifica e atualiza dinamicamente o Dashboard caso esteja aberto."""
        if self.win_dashboard and self.win_dashboard.winfo_exists():
            self.win_dashboard.atualizar_dados()

    def executar(self):
        self.main_view.mainloop()


# ==============================================================================
# INICIALIZAÇÃO DO PROGRAMA
# ==============================================================================
if __name__ == "__main__":
    app = AppController()
    app.executar()
    