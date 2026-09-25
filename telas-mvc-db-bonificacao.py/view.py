import tkinter as tk
from tkinter import ttk, messagebox

class JanelaHelper:
    @staticmethod
    def centralizar_janela(win, largura, altura):
        """Centraliza qualquer janela/Toplevel na tela."""
        win.update_idletasks()
        s_largura = win.winfo_screenwidth()
        s_altura = win.winfo_screenheight()
        pos_x = (s_largura - largura) // 2
        pos_y = (s_altura - altura) // 2
        win.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

class MainView(tk.Tk):
    """Janela Principal / Menu Corporativo"""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Painel Gestor - Sistema Corporativo")
        self.configure(bg="#0f172a")
        
        JanelaHelper.centralizar_janela(self, 500, 200)
        self.resizable(False, False)

        # Header
        header = tk.Frame(self, bg="#1e293b", height=50)
        header.pack(fill="x", side="top")
        tk.Label(
            header, text="PAINEL PRINCIPAL DE SISTEMAS", 
            font=("Segoe UI", 12, "bold"), fg="#f8fafc", bg="#1e293b"
        ).pack(pady=12)

        # Barra de Botões
        frame_nav = tk.Frame(self, bg="#0f172a")
        frame_nav.pack(expand=True, pady=20)

        btn_atv3 = tk.Button(
            frame_nav, text="Módulo Bonificação SQLite (Atividade 3)", 
            command=self.controller.abrir_atividade3_crud,
            bg="#059669", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5, bd=0
        )
        btn_atv3.grid(row=0, column=1, padx=10)


class Atividade2Window(tk.Toplevel):
    """Janela da Atividade 2 - HRMS Simples"""
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.on_close = on_close
        self.title("HRMS - Gestão de Colaboradores e Quadro Funcional")
        self.configure(bg="#f8fafc")
        JanelaHelper.centralizar_janela(self, 480, 360)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        tk.Label(
            self, text="Cadastro de Colaborador Corporativo", 
            font=("Segoe UI", 13, "bold"), fg="#0f172a", bg="#f8fafc"
        ).pack(pady=(15, 5))

        frame_form = tk.Frame(self, bg="#f8fafc")
        frame_form.pack(pady=10, padx=20)

        tk.Label(frame_form, text="Matrícula:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").grid(row=0, column=0, pady=5, sticky="e")
        self.entry_mat = tk.Entry(frame_form, width=30)
        self.entry_mat.grid(row=0, column=1, pady=5)

        tk.Label(frame_form, text="Nome Completo:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").grid(row=1, column=0, pady=5, sticky="e")
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=1, column=1, pady=5)

        tk.Label(frame_form, text="Cargo / Função:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").grid(row=2, column=0, pady=5, sticky="e")
        self.entry_cargo = tk.Entry(frame_form, width=30)
        self.entry_cargo.grid(row=2, column=1, pady=5)

        frame_btns = tk.Frame(self, bg="#f8fafc")
        frame_btns.pack(pady=15)
        
        tk.Button(frame_btns, text="Salvar Colaborador", command=self.salvar, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(frame_btns, text="Voltar ao Menu", command=self.fechar, bg="#64748b", fg="white", font=("Segoe UI", 9)).grid(row=0, column=1, padx=5)

        self.lbl_audit = tk.Label(self, text="", font=("Segoe UI", 8, "italic"), bg="#f8fafc")
        self.lbl_audit.pack(pady=10)

    def salvar(self):
        m, n, c = self.entry_mat.get().strip(), self.entry_nome.get().strip(), self.entry_cargo.get().strip()
        if m and n and c:
            self.lbl_audit.config(text=f"[REGISTRO SALVO] Matrícula: {m} | {n} ({c})", fg="#15803d")
        else:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")

    def fechar(self):
        self.destroy()
        self.on_close()


class BonificacaoCRUDWindow(tk.Toplevel):
    """Janela Completa CRUD + Filtro SQLite (Atividade 3 Refatorada)"""
    def __init__(self, parent, controller, on_close):
        super().__init__(parent)
        self.controller = controller
        self.on_close = on_close
        self.title("Gestão de Bonificações e Metas - SQLite")
        self.configure(bg="#f1f5f9")
        
        JanelaHelper.centralizar_janela(self, 750, 560)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        # Cabeçalho
        tk.Label(
            self, text="MÓDULO DE BONIFICAÇÃO CORPORATIVA (SQLITE)", 
            font=("Segoe UI", 11, "bold"), bg="#f1f5f9", fg="#0f172a"
        ).pack(pady=8)

        # Form Entradas
        frame_form = tk.Frame(self, bg="#f1f5f9")
        frame_form.pack(pady=5)

        self.id_selecionado = None

        tk.Label(frame_form, text="Colaborador / Gestor:", bg="#f1f5f9").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.ent_nome = tk.Entry(frame_form, width=28)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Salário Base (R$):", bg="#f1f5f9").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self.ent_salario = tk.Entry(frame_form, width=28)
        self.ent_salario.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Atingimento de Metas (%):", bg="#f1f5f9").grid(row=2, column=0, padx=5, pady=4, sticky="e")
        self.ent_meta = tk.Entry(frame_form, width=28)
        self.ent_meta.grid(row=2, column=1, padx=5, pady=4)

        # Frame Botões CRUD
        frame_btn = tk.Frame(self, bg="#f1f5f9")
        frame_btn.pack(pady=8)

        tk.Button(frame_btn, text="Calcular e Salvar", command=self.controller.salvar, bg="#059669", fg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=4)
        tk.Button(frame_btn, text="Atualizar Reg.", command=self.controller.atualizar, bg="#2563eb", fg="white", font=("Segoe UI", 9)).grid(row=0, column=1, padx=4)
        tk.Button(frame_btn, text="Excluir Reg.", command=self.controller.excluir, bg="#dc2626", fg="white", font=("Segoe UI", 9)).grid(row=0, column=2, padx=4)
        tk.Button(frame_btn, text="Limpar Campos", command=self.limpar_campos, bg="#64748b", fg="white", font=("Segoe UI", 9)).grid(row=0, column=3, padx=4)

        # Filtro de Pesquisa
        frame_filtro = tk.Frame(self, bg="#f1f5f9")
        frame_filtro.pack(pady=5, fill="x", padx=15)

        tk.Label(frame_filtro, text="Filtrar por Nome:", bg="#f1f5f9", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
        self.ent_filtro = tk.Entry(frame_filtro, width=30)
        self.ent_filtro.pack(side="left", padx=5)
        tk.Button(frame_filtro, text="Pesquisar", command=self.controller.filtrar, bg="#0284c7", fg="white").pack(side="left", padx=2)
        tk.Button(frame_filtro, text="Ver Todos", command=self.controller.carregar_dados, bg="#475569", fg="white").pack(side="left", padx=2)

        # Tabela Treeview
        columns = ("id", "nome", "salario", "meta", "bonus", "categoria")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Colaborador")
        self.tree.heading("salario", text="Salário (R$)")
        self.tree.heading("meta", text="Meta (%)")
        self.tree.heading("bonus", text="Bônus (R$)")
        self.tree.heading("categoria", text="Categoria")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nome", width=150)
        self.tree.column("salario", width=90, anchor="e")
        self.tree.column("meta", width=70, anchor="center")
        self.tree.column("bonus", width=110, anchor="e")
        self.tree.column("categoria", width=220)

        self.tree.pack(pady=10, padx=15, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_item)

        # Botão Fechar
        tk.Button(self, text="Voltar ao Menu Principal", command=self.fechar, bg="#334155", fg="white", font=("Segoe UI", 9, "bold")).pack(pady=8)

    def limpar_campos(self):
        self.id_selecionado = None
        self.ent_nome.delete(0, tk.END)
        self.ent_salario.delete(0, tk.END)
        self.ent_meta.delete(0, tk.END)

    def ao_selecionar_item(self, event):
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado[0])['values']
            self.id_selecionado = item[0]
            self.ent_nome.delete(0, tk.END)
            self.ent_nome.insert(0, item[1])
            self.ent_salario.delete(0, tk.END)
            self.ent_salario.insert(0, item[2])
            self.ent_meta.delete(0, tk.END)
            self.ent_meta.insert(0, item[3])

    def fechar(self):
        self.destroy()
        self.on_close()
