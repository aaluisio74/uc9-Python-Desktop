import tkinter as tk
from tkinter import ttk, messagebox

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    largura_s = janela.winfo_screenwidth()
    altura_s = janela.winfo_screenheight()
    pos_x = (largura_s - largura) // 2
    pos_y = (altura_s - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

class JanelaPesquisaLotes(tk.Toplevel):
    """Janela para consultar, editar e excluir lotes processados"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Pesquisa de Lotes Processados")
        self.configure(bg="#f8fafc")
        self.id_selecionado = None
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)

        # Cabeçalho
        lbl_header = tk.Label(
            self, text="Consulta e Gestão de Lotes de Dados",
            font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#0f172a"
        )
        lbl_header.pack(pady=10)

        # Formulário para Edição
        frame_form = tk.Frame(self, bg="#f8fafc")
        frame_form.pack(pady=5, padx=10)

        tk.Label(frame_form, text="Volume (Registros):", font=("Segoe UI", 9, "bold"), bg="#f8fafc").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.entry_volume = tk.Entry(frame_form, width=25, font=("Segoe UI", 9))
        self.entry_volume.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Ambiente:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self.cb_ambiente = ttk.Combobox(frame_form, values=["HOMOLOG", "PROD"], width=23, state="readonly", font=("Segoe UI", 9))
        self.cb_ambiente.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Tipo de Carga:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").grid(row=2, column=0, padx=5, pady=4, sticky="e")
        self.cb_tipo = ttk.Combobox(frame_form, values=["FINANCEIRO", "NOTIFICACOES"], width=23, state="readonly", font=("Segoe UI", 9))
        self.cb_tipo.grid(row=2, column=1, padx=5, pady=4)

        # Botões de Operação
        frame_botoes = tk.Frame(self, bg="#f8fafc")
        frame_botoes.pack(pady=10)

        btn_salvar = tk.Button(frame_botoes, text="Salvar Alterações", command=self.controller.salvar_lote, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), width=15)
        btn_salvar.grid(row=0, column=0, padx=5)

        btn_excluir = tk.Button(frame_botoes, text="Excluir Lote", command=self.controller.excluir_lote, bg="#dc2626", fg="white", font=("Segoe UI", 9, "bold"), width=12)
        btn_excluir.grid(row=0, column=1, padx=5)

        btn_limpar = tk.Button(frame_botoes, text="Limpar", command=self.limpar_campos, bg="#64748b", fg="white", font=("Segoe UI", 9), width=10)
        btn_limpar.grid(row=0, column=2, padx=5)

        # Campo de Pesquisa
        frame_busca = tk.Frame(self, bg="#f8fafc")
        frame_busca.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_busca, text="Filtrar Lotes:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(side="left", padx=5)
        self.entry_busca = tk.Entry(frame_busca, font=("Segoe UI", 9))
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=5)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.controller.filtrar_lotes())

        # Tabela (Treeview)
        frame_tabela = tk.Frame(self, bg="#f8fafc")
        frame_tabela.pack(pady=10, padx=20, fill="both", expand=True)

        colunas = ("id", "volume", "ambiente", "tipo", "data_execucao")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("volume", text="Volume")
        self.tree.heading("ambiente", text="Ambiente")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("data_execucao", text="Data / Hora Execução")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("volume", width=80, anchor="center")
        self.tree.column("ambiente", width=100, anchor="center")
        self.tree.column("tipo", width=120, anchor="center")
        self.tree.column("data_execucao", width=160, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_registro)

        sb = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

        # Feedback
        self.lbl_audit = tk.Label(self, text="", font=("Segoe UI", 8, "italic"), bg="#f8fafc")
        self.lbl_audit.pack(pady=5)

        centralizar_janela(self, 650, 520)

    def selecionar_registro(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item[0], "values")
            self.id_selecionado = valores[0]
            self.entry_volume.delete(0, tk.END)
            self.entry_volume.insert(0, valores[1])
            self.cb_ambiente.set(valores[2])
            self.cb_tipo.set(valores[3])

    def limpar_campos(self):
        self.id_selecionado = None
        self.entry_volume.delete(0, tk.END)
        self.cb_ambiente.set("")
        self.cb_tipo.set("")
        self.lbl_audit.config(text="")

    def ao_fechar(self):
        self.controller.fechar_janela_lotes()

class MainView(tk.Tk):
    """Janela Principal: Central de Processamento de Lotes (Batch Jobs)"""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Central de Processamento de Lotes (BATCH)")
        self.configure(bg="#f8fafc")

        # Menu
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        menu_ops = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Operações", menu=menu_ops)
        menu_ops.add_command(label="Pesquisa de Lotes", command=self.controller.abrir_janela_lotes)
        menu_ops.add_command(label="Limpar Filtros", command=self.resetar_lote)
        menu_ops.add_separator()
        menu_ops.add_command(label="Sair da Central", command=self.controller.encerrar_sessao)

        menu_ajuda = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre o Kernel", command=self.controller.exibir_sobre)

        # Barra de Botões
        toolbar = tk.Frame(self, bg="#e2e8f0", bd=1, relief="raised")
        toolbar.pack(side="top", fill="x")

        # Conteúdo Principal
        lbl_titulo = tk.Label(
            self, text="CENTRAL DE PROCESSAMENTO DE LOTES (BATCH)",
            font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#0f172a"
        )
        lbl_titulo.pack(pady=15)

        frame_params = tk.Frame(self, bg="#f8fafc")
        frame_params.pack(pady=5)

        tk.Label(frame_params, text="Tamanho do Lote (Registros):", font=("Segoe UI", 10), bg="#f8fafc").grid(row=0, column=0, padx=10, pady=5)
        self.entry_lote = tk.Entry(frame_params, width=15, font=("Segoe UI", 10))
        self.entry_lote.grid(row=0, column=1, padx=10, pady=5)

        frame_opcoes = tk.Frame(frame_params, bg="#f8fafc")
        frame_opcoes.grid(row=1, column=0, columnspan=2, pady=15)

        self.var_ambiente = tk.StringVar(value="HOMOLOG")
        self.var_tipo = tk.StringVar(value="FINANCEIRO")

        grp_ambiente = tk.LabelFrame(frame_opcoes, text="Ambiente de Execução", font=("Segoe UI", 9, "bold"), bg="#f8fafc")
        grp_ambiente.grid(row=0, column=0, padx=15)
        tk.Radiobutton(grp_ambiente, text="Homologação (Staging)", variable=self.var_ambiente, value="HOMOLOG", bg="#f8fafc").pack(anchor="w", padx=8, pady=3)
        tk.Radiobutton(grp_ambiente, text="Produção (Live)", variable=self.var_ambiente, value="PROD", bg="#f8fafc").pack(anchor="w", padx=8, pady=3)

        grp_tipo = tk.LabelFrame(frame_opcoes, text="Tipo de Carga", font=("Segoe UI", 9, "bold"), bg="#f8fafc")
        grp_tipo.grid(row=0, column=1, padx=15)
        tk.Radiobutton(grp_tipo, text="Lote Financeiro", variable=self.var_tipo, value="FINANCEIRO", bg="#f8fafc").pack(anchor="w", padx=8, pady=3)
        tk.Radiobutton(grp_tipo, text="Disparo de Notificações", variable=self.var_tipo, value="NOTIFICACOES", bg="#f8fafc").pack(anchor="w", padx=8, pady=3)

        frame_acao = tk.Frame(self, bg="#f8fafc")
        frame_acao.pack(pady=10)

        btn_exec = tk.Button(frame_acao, text="Iniciar Processamento", command=self.controller.executar_processamento, bg="#0284c7", fg="white", font=("Segoe UI", 10, "bold"), width=20)
        btn_exec.grid(row=0, column=0, padx=5)

        btn_reset = tk.Button(frame_acao, text="Resetar Lote", command=self.resetar_lote, bg="#64748b", fg="white", font=("Segoe UI", 10), width=14)
        btn_reset.grid(row=0, column=1, padx=5)

        self.lbl_status = tk.Label(self, text="", font=("Segoe UI", 10, "bold"), bg="#f8fafc")
        self.lbl_status.pack(pady=10)

        # Centralização da janela principal após renderização dos widgets
        centralizar_janela(self, 560, 520)

    def resetar_lote(self):
        self.entry_lote.delete(0, tk.END)
        self.var_ambiente.set("HOMOLOG")
        self.var_tipo.set("FINANCEIRO")
        self.lbl_status.config(text="")
