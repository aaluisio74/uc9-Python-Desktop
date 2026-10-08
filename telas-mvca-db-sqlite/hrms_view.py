import tkinter as tk
from tkinter import messagebox, ttk

# ------------------------------------------------------------------------------
# Centralizar as janelas na tela.
# ------------------------------------------------------------------------------
def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

# ------------------------------------------------------------------------------
# View 1: Janela da Atividade 2 (Proposta Inicial com SQLite)
# ------------------------------------------------------------------------------
class JanelaAtividade2(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("HRMS - Atividade 2: Cadastro de Colaborador")
        #self.geometry("480x380")
        centralizar_janela(self, 480, 380)
        self.configure(bg="#f8fafc")
        self.resizable(False, False)

        # Cabeçalho
        header = tk.Label(
            self,
            text="Cadastro de Colaborador Corporativo",
            font=("Segoe UI", 13, "bold"),
            fg="#0f172a",
            bg="#f8fafc"
        )
        header.pack(pady=(15, 5))

        # Formulário
        frame_form = tk.Frame(self, bg="#f8fafc")
        frame_form.pack(pady=10, padx=20)

        # Matrícula
        tk.Label(frame_form, text="Matrícula:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.entry_matricula = tk.Entry(frame_form, width=32, font=("Segoe UI", 9), relief="solid", bd=1)
        self.entry_matricula.grid(row=0, column=1, padx=5, pady=8)

        # Nome Completo
        tk.Label(frame_form, text="Nome Completo:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.entry_nome = tk.Entry(frame_form, width=32, font=("Segoe UI", 9), relief="solid", bd=1)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=8)

        # Cargo / Função
        tk.Label(frame_form, text="Cargo / Função:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").grid(row=2, column=0, padx=5, pady=8, sticky="e")
        self.entry_cargo = tk.Entry(frame_form, width=32, font=("Segoe UI", 9), relief="solid", bd=1)
        self.entry_cargo.grid(row=2, column=1, padx=5, pady=8)

        # Botões de Ação
        frame_botoes = tk.Frame(self, bg="#f8fafc")
        frame_botoes.pack(pady=15)

        btn_salvar = tk.Button(
            frame_botoes,
            text="Salvar Colaborador",
            command=self.salvar,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10, pady=3, bd=0, cursor="hand2"
        )
        btn_salvar.grid(row=0, column=0, padx=8)

        btn_limpar = tk.Button(
            frame_botoes,
            text="Limpar Formulário",
            command=self.limpar_formulario,
            bg="#64748b",
            fg="white",
            font=("Segoe UI", 9),
            padx=10, pady=3, bd=0, cursor="hand2"
        )
        btn_limpar.grid(row=0, column=1, padx=8)

        # Feedback de Auditoria
        self.lbl_audit = tk.Label(self, text="", font=("Segoe UI", 8, "italic"), bg="#f8fafc")
        self.lbl_audit.pack(pady=10)

    def salvar(self):
        mat = self.entry_matricula.get().strip()
        nome = self.entry_nome.get().strip()
        cargo = self.entry_cargo.get().strip()

        sucesso, msg = self.controller.salvar_funcionario(mat, nome, cargo)
        
        if sucesso:
            self.lbl_audit.config(
                text=f"[REGISTRO GRAVADO NO BANCO] Matrícula: {mat} | {nome} ({cargo})",
                fg="#15803d"
            )
            #messagebox.showinfo("Sucesso", msg)
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_formulario()
        else:
            self.lbl_audit.config(text=f"[ERRO] {msg}", fg="#dc2626")
            #messagebox.showwarning("Inconsistência de Dados", msg)
            messagebox.showwarning("Inconsistência de Dados", msg, parent=self)

    def limpar_formulario(self):
        self.entry_matricula.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.lbl_audit.config(text="")


# ------------------------------------------------------------------------------
# View 2: Nova Janela de Gestão Completa (CRUD + Filtro)
# ------------------------------------------------------------------------------
class JanelaGestaoDB(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("HRMS - Módulo Avançado de Banco de Dados SQLite")
        #self.geometry("720x560")
        centralizar_janela(self, 720, 560)
        self.configure(bg="#f8fafc")
        self.id_selecionado = None

        # Título
        tk.Label(
            self, 
            text="Gestão de Registros Corporativos (SQLite)", 
            font=("Segoe UI", 13, "bold"), 
            bg="#f8fafc", fg="#0f172a"
        ).pack(pady=10)

        # Frame de Busca/Filtro
        frame_filtro = tk.LabelFrame(self, text=" Pesquisa e Filtro ", font=("Segoe UI", 9, "bold"), bg="#f8fafc")
        frame_filtro.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_filtro, text="Buscar:", bg="#f8fafc").pack(side="left", padx=5, pady=5)
        self.entry_filtro = tk.Entry(frame_filtro, width=35, font=("Segoe UI", 9))
        self.entry_filtro.pack(side="left", padx=5, pady=5)
        
        btn_filtrar = tk.Button(
            frame_filtro, text="Filtrar", command=self.carregar_dados,
            bg="#0284c7", fg="white", font=("Segoe UI", 8, "bold")
        )
        btn_filtrar.pack(side="left", padx=5, pady=5)

        btn_limpar_filtro = tk.Button(
            frame_filtro, text="Mostrar Todos", command=self.limpar_filtro,
            bg="#64748b", fg="white", font=("Segoe UI", 8)
        )
        btn_limpar_filtro.pack(side="left", padx=5, pady=5)

        # Frame do Formulário de Entrada/Edição
        frame_form = tk.LabelFrame(self, text=" Formulário do Colaborador ", font=("Segoe UI", 9, "bold"), bg="#f8fafc")
        frame_form.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_form, text="Matrícula:", bg="#f8fafc").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_mat = tk.Entry(frame_form, width=15)
        self.ent_mat.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Nome:", bg="#f8fafc").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_nome = tk.Entry(frame_form, width=30)
        self.ent_nome.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Cargo:", bg="#f8fafc").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_cargo = tk.Entry(frame_form, width=20)
        self.ent_cargo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Depto:", bg="#f8fafc").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_depto = tk.Entry(frame_form, width=20)
        self.ent_depto.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Botões de Operação CRUD
        frame_acoes = tk.Frame(self, bg="#f8fafc")
        frame_acoes.pack(pady=8)

        tk.Button(frame_acoes, text="Inserir Novo", command=self.inserir, bg="#16a34a", fg="white", font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=0, padx=5)
        tk.Button(frame_acoes, text="Atualizar/Editar", command=self.atualizar, bg="#ca8a04", fg="white", font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=1, padx=5)
        tk.Button(frame_acoes, text="Excluir", command=self.excluir, bg="#dc2626", fg="white", font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=2, padx=5)
        tk.Button(frame_acoes, text="Limpar Campos", command=self.limpar_campos, bg="#64748b", fg="white", font=("Segoe UI", 9), width=12).grid(row=0, column=3, padx=5)

        # Tabela (Treeview) para exibição dos registros
        frame_tabela = tk.Frame(self)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=10)

        colunas = ("id", "matricula", "nome", "cargo", "departamento")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=8)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("matricula", text="Matrícula")
        self.tree.heading("nome", text="Nome Completo")
        self.tree.heading("cargo", text="Cargo / Função")
        self.tree.heading("departamento", text="Departamento")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("matricula", width=100)
        self.tree.column("nome", width=220)
        self.tree.column("cargo", width=160)
        self.tree.column("departamento", width=120)

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento de seleção na tabela
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)

        # Carregar registros
        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = self.entry_filtro.get().strip()
        registros = self.controller.buscar_funcionarios(filtro)

        for reg in registros:
            self.tree.insert("", "end", values=reg)

    def limpar_filtro(self):
        self.entry_filtro.delete(0, tk.END)
        self.carregar_dados()

    def ao_selecionar(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], "values")
            self.id_selecionado = valores[0]
            
            self.limpar_campos(manter_id=True)
            self.ent_mat.insert(0, valores[1])
            self.ent_nome.insert(0, valores[2])
            self.ent_cargo.insert(0, valores[3])
            self.ent_depto.insert(0, valores[4] if valores[4] else "")

    def inserir(self):
        mat = self.ent_mat.get().strip()
        nome = self.ent_nome.get().strip()
        cargo = self.ent_cargo.get().strip()
        depto = self.ent_depto.get().strip()

        sucesso, msg = self.controller.salvar_funcionario(mat, nome, cargo, depto)
        if sucesso:
            #messagebox.showinfo("Sucesso", msg)
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            #messagebox.showwarning("Aviso", msg)
            messagebox.showwarning("Aviso", msg, parent=self)

    def atualizar(self):
        if not self.id_selecionado:
            #messagebox.showwarning("Aviso", "Selecione um registro na tabela para editar.")
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para editar.", parent=self)
            return

        mat = self.ent_mat.get().strip()
        nome = self.ent_nome.get().strip()
        cargo = self.ent_cargo.get().strip()
        depto = self.ent_depto.get().strip()

        sucesso, msg = self.controller.editar_funcionario(self.id_selecionado, mat, nome, cargo, depto)
        if sucesso:
            #messagebox.showinfo("Sucesso", msg)
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            #messagebox.showerror("Erro", msg)
            messagebox.showerror("Erro", msg, parent=self)

    def excluir(self):
        if not self.id_selecionado:
            #messagebox.showwarning("Aviso", "Selecione um registro na tabela para excluir.")
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para editar.", parent=self)
            return

        if  messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este colaborador?", parent=self):
            #messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este colaborador?"):
            sucesso, msg = self.controller.excluir_funcionario(self.id_selecionado)
            if sucesso:
                #messagebox.showinfo("Sucesso", msg)
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.limpar_campos()
                self.carregar_dados()
            else:
                #messagebox.showerror("Erro", msg)
                messagebox.showerror("Erro", msg, parent=self)

    def limpar_campos(self, manter_id=False):
        if not manter_id:
            self.id_selecionado = None
        self.ent_mat.delete(0, tk.END)
        self.ent_nome.delete(0, tk.END)
        self.ent_cargo.delete(0, tk.END)
        self.ent_depto.delete(0, tk.END)


# ------------------------------------------------------------------------------
# View 3: Janela Principal (Barra de Botões de Navegação)
# ------------------------------------------------------------------------------
class JanelaPrincipal(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("HRMS - Sistema de Gestão de Colaboradores Corporativos")
        #self.geometry("520x250")
        centralizar_janela(self, 520, 250)
        self.configure(bg="#0f172a")
        self.resizable(False, False)

        # Título
        tk.Label(
            self,
            text="SISTEMA DE GESTÃO DE RECURSOS HUMANOS (HRMS)",
            font=("Segoe UI", 11, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        ).pack(pady=20)

        # Barra de Botões
        frame_nav = tk.Frame(self, bg="#1e293b", bd=1, relief="solid")
        frame_nav.pack(pady=15, padx=20, fill="x")

        tk.Label(
            frame_nav,
            text="Selecione o Módulo de Operação:",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        ).pack(pady=(10, 5))

        btn_atv2 = tk.Button(
            frame_nav,
            text="Atividade 2: Cadastro Simples",
            command=self.abrir_atividade2,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10, pady=5, bd=0, cursor="hand2"
        )
        btn_atv2.pack(side="left", padx=15, pady=15, expand=True)

        btn_gestao = tk.Button(
            frame_nav,
            text="Módulo Avançado (CRUD + SQLite)",
            command=self.abrir_gestao_db,
            bg="#0284c7",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10, pady=5, bd=0, cursor="hand2"
        )
        btn_gestao.pack(side="right", padx=15, pady=15, expand=True)

        # Rodapé
        tk.Label(
            self,
            text="Padrão Arquitetural MVC | Banco de Dados SQLite Ativo",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0f172a"
        ).pack(side="bottom", pady=10)

    def abrir_atividade2(self):
        JanelaAtividade2(self, self.controller)

    def abrir_gestao_db(self):
        JanelaGestaoDB(self, self.controller)
