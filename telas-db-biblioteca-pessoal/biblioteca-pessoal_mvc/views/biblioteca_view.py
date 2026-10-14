import tkinter as tk
from tkinter import messagebox

class BibliotecaView:
    """View: cria a interface e apresenta dados; não acessa o banco."""
    def __init__(self, janela):
        self.janela = janela
        janela.title("📚 Minha Biblioteca Pessoal - MVC")
        janela.geometry("900x560")
        janela.minsize(760, 480)
        self._criar_interface()

    def _criar_interface(self):
        tk.Label(self.janela, text="📚 MINHA BIBLIOTECA PESSOAL", font=("Arial", 16, "bold"), fg="darkblue").pack(pady=10)
        principal = tk.Frame(self.janela)
        principal.pack(fill="both", expand=True, padx=10)
        form = tk.LabelFrame(principal, text="Dados do Livro", padx=10, pady=10)
        form.pack(side="left", fill="y", padx=5)
        tk.Label(form, text="Título:").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_titulo = tk.Entry(form, width=28); self.entry_titulo.grid(row=0, column=1, pady=5, padx=5)
        tk.Label(form, text="Autor:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_autor = tk.Entry(form, width=28); self.entry_autor.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(form, text="Ano:").grid(row=2, column=0, pady=5, sticky="w")
        self.entry_ano = tk.Entry(form, width=28); self.entry_ano.grid(row=2, column=1, pady=5, padx=5)
        tk.Label(form, text="Status:").grid(row=3, column=0, pady=5, sticky="w")
        self.status_var = tk.StringVar(value="Não Lido")
        status_frame = tk.Frame(form); status_frame.grid(row=3, column=1, pady=5, sticky="w")
        tk.Radiobutton(status_frame, text="Lido", variable=self.status_var, value="Lido").pack(side="left", padx=5)
        tk.Radiobutton(status_frame, text="Não Lido", variable=self.status_var, value="Não Lido").pack(side="left", padx=5)
        botoes = tk.Frame(form); botoes.grid(row=4, column=0, columnspan=2, pady=15)
        self.btn_adicionar = tk.Button(botoes, text="➕ Adicionar", bg="green", fg="white", width=12); self.btn_adicionar.pack(side="left", padx=2)
        self.btn_limpar = tk.Button(botoes, text="🔄 Limpar", bg="orange", fg="white", width=12); self.btn_limpar.pack(side="left", padx=2)
        lista_frame = tk.LabelFrame(principal, text="Meus Livros", padx=10, pady=10)
        lista_frame.pack(side="right", fill="both", expand=True, padx=5)
        scroll = tk.Scrollbar(lista_frame); scroll.pack(side="right", fill="y")
        self.listbox_livros = tk.Listbox(lista_frame, height=15, font=("Arial", 10), yscrollcommand=scroll.set, exportselection=False)
        self.listbox_livros.pack(side="left", fill="both", expand=True); scroll.config(command=self.listbox_livros.yview)
        acoes = tk.Frame(self.janela); acoes.pack(pady=8)
        self.btn_lido = tk.Button(acoes, text="✅ Marcar como Lido", bg="blue", fg="white", width=17); self.btn_lido.pack(side="left", padx=5)
        self.btn_nao_lido = tk.Button(acoes, text="📖 Marcar como Não Lido", bg="purple", fg="white", width=20); self.btn_nao_lido.pack(side="left", padx=5)
        self.btn_remover = tk.Button(acoes, text="🗑️ Remover", bg="red", fg="white", width=12); self.btn_remover.pack(side="left", padx=5)
        self.label_detalhes = tk.Label(self.janela, text="Selecione um livro para ver os detalhes.", font=("Arial", 10), justify="left", relief="sunken", padx=5, pady=5, anchor="w")
        self.label_detalhes.pack(pady=5, padx=10, fill="x")
        self.label_stats = tk.Label(self.janela, text="", font=("Arial", 9), fg="gray"); self.label_stats.pack(pady=(0, 5))

    def registrar_comandos(self, adicionar, limpar, marcar_lido, marcar_nao_lido, remover, selecionar):
        self.btn_adicionar.config(command=adicionar); self.btn_limpar.config(command=limpar)
        self.btn_lido.config(command=marcar_lido); self.btn_nao_lido.config(command=marcar_nao_lido)
        self.btn_remover.config(command=remover); self.listbox_livros.bind("<<ListboxSelect>>", selecionar)

    def obter_dados_formulario(self):
        return self.entry_titulo.get().strip(), self.entry_autor.get().strip(), self.entry_ano.get().strip(), self.status_var.get()

    def limpar_formulario(self):
        for campo in (self.entry_titulo, self.entry_autor, self.entry_ano): campo.delete(0, tk.END)
        self.status_var.set("Não Lido"); self.entry_titulo.focus()

    def obter_indice_selecionado(self):
        selecao = self.listbox_livros.curselection()
        return selecao[0] if selecao else None

    def exibir_livros(self, livros):
        self.listbox_livros.delete(0, tk.END)
        for _, titulo, autor, ano, status in livros:
            texto = titulo + (f" - {autor}" if autor else "") + (f" ({ano})" if ano is not None else "")
            self.listbox_livros.insert(tk.END, ("✅ " if status == "Lido" else "📌 ") + texto)

    def exibir_detalhes(self, livro):
        if not livro:
            self.label_detalhes.config(text="Selecione um livro para ver os detalhes."); return
        _, titulo, autor, ano, status = livro
        self.label_detalhes.config(text=f"📖 Título: {titulo}\n✍️ Autor: {autor or 'Não informado'}\n📅 Ano: {ano if ano is not None else 'Não informado'}\n📌 Status: {status}")

    def exibir_estatisticas(self, livros):
        total = len(livros); lidos = sum(1 for livro in livros if livro[4] == "Lido")
        self.label_stats.config(text=f"Total: {total} livros | Lidos: {lidos} | Não lidos: {total-lidos}")

    def aviso(self, titulo, mensagem): messagebox.showwarning(titulo, mensagem)
    def informacao(self, titulo, mensagem): messagebox.showinfo(titulo, mensagem)
    def erro(self, titulo, mensagem): messagebox.showerror(titulo, mensagem)
    def confirmar(self, titulo, mensagem): return messagebox.askyesno(titulo, mensagem)
