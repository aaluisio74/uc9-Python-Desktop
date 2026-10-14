import tkinter as tk
from tkinter import messagebox
import sqlite3


class BibliotecaPessoal:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📚 Minha Biblioteca Pessoal")
        self.janela.geometry("900x560")
        self.janela.minsize(760, 480)

        self.criar_banco()
        self.criar_interface()
        self.atualizar_lista()

    def conectar_banco(self):
        return sqlite3.connect("biblioteca.db")

    def criar_banco(self):
        with self.conectar_banco() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT,
                    ano INTEGER,
                    status TEXT NOT NULL DEFAULT 'Não Lido'
                )
            """)

    def criar_interface(self):
        tk.Label(
            self.janela,
            text="📚 MINHA BIBLIOTECA PESSOAL",
            font=("Arial", 16, "bold"),
            fg="darkblue"
        ).pack(pady=10)

        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(fill="both", expand=True, padx=10)

        frame_form = tk.LabelFrame(
            frame_principal, text="Dados do Livro", padx=10, pady=10
        )
        frame_form.pack(side="left", fill="y", padx=5)

        tk.Label(frame_form, text="Título:").grid(
            row=0, column=0, pady=5, sticky="w"
        )
        self.entry_titulo = tk.Entry(frame_form, width=28)
        self.entry_titulo.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Autor:").grid(
            row=1, column=0, pady=5, sticky="w"
        )
        self.entry_autor = tk.Entry(frame_form, width=28)
        self.entry_autor.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Ano:").grid(
            row=2, column=0, pady=5, sticky="w"
        )
        self.entry_ano = tk.Entry(frame_form, width=28)
        self.entry_ano.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Status:").grid(
            row=3, column=0, pady=5, sticky="w"
        )
        self.status = tk.StringVar(value="Não Lido")
        frame_status = tk.Frame(frame_form)
        frame_status.grid(row=3, column=1, pady=5, sticky="w")

        tk.Radiobutton(
            frame_status, text="Lido", variable=self.status, value="Lido"
        ).pack(side="left", padx=5)
        tk.Radiobutton(
            frame_status, text="Não Lido",
            variable=self.status, value="Não Lido"
        ).pack(side="left", padx=5)

        frame_botoes_form = tk.Frame(frame_form)
        frame_botoes_form.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(
            frame_botoes_form, text="➕ Adicionar",
            command=self.adicionar_livro, bg="green", fg="white", width=12
        ).pack(side="left", padx=2)
        tk.Button(
            frame_botoes_form, text="🔄 Limpar",
            command=self.limpar_campos, bg="orange", fg="white", width=12
        ).pack(side="left", padx=2)

        frame_lista = tk.LabelFrame(
            frame_principal, text="Meus Livros", padx=10, pady=10
        )
        frame_lista.pack(side="right", fill="both", expand=True, padx=5)

        scroll_lista = tk.Scrollbar(frame_lista)
        scroll_lista.pack(side="right", fill="y")

        self.listbox_livros = tk.Listbox(
            frame_lista, height=15, font=("Arial", 10),
            yscrollcommand=scroll_lista.set, exportselection=False
        )
        self.listbox_livros.pack(side="left", fill="both", expand=True)
        scroll_lista.config(command=self.listbox_livros.yview)
        self.listbox_livros.bind("<<ListboxSelect>>", self.mostrar_detalhes)

        frame_botoes_lista = tk.Frame(self.janela)
        frame_botoes_lista.pack(pady=8)

        tk.Button(
            frame_botoes_lista, text="✅ Marcar como Lido",
            command=lambda: self.mudar_status("Lido"),
            bg="blue", fg="white", width=17
        ).pack(side="left", padx=5)
        tk.Button(
            frame_botoes_lista, text="📖 Marcar como Não Lido",
            command=lambda: self.mudar_status("Não Lido"),
            bg="purple", fg="white", width=20
        ).pack(side="left", padx=5)
        tk.Button(
            frame_botoes_lista, text="🗑️ Remover",
            command=self.remover_livro, bg="red", fg="white", width=12
        ).pack(side="left", padx=5)

        self.label_detalhes = tk.Label(
            self.janela, text="Selecione um livro para ver os detalhes.",
            font=("Arial", 10), justify="left", relief="sunken",
            padx=5, pady=5, anchor="w"
        )
        self.label_detalhes.pack(pady=5, padx=10, fill="x")

        self.label_stats = tk.Label(
            self.janela, text="", font=("Arial", 9), fg="gray"
        )
        self.label_stats.pack(pady=(0, 5))

    def adicionar_livro(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        ano_texto = self.entry_ano.get().strip()
        status = self.status.get()

        if not titulo:
            messagebox.showwarning("Aviso", "O título é obrigatório!")
            self.entry_titulo.focus()
            return

        ano = None
        if ano_texto:
            try:
                ano = int(ano_texto)
            except ValueError:
                messagebox.showwarning("Aviso", "O ano deve ser um número inteiro.")
                self.entry_ano.focus()
                return

            if ano < 1400 or ano > 2030:
                messagebox.showwarning("Aviso", "Ano inválido! Informe entre 1400 e 2030.")
                self.entry_ano.focus()
                return

        try:
            with self.conectar_banco() as conexao:
                conexao.execute(
                    "INSERT INTO livros (titulo, autor, ano, status) VALUES (?, ?, ?, ?)",
                    (titulo, autor or None, ano, status)
                )
            messagebox.showinfo("Sucesso", "Livro adicionado!")
            self.limpar_campos()
            self.atualizar_lista()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao adicionar: {erro}")

    def atualizar_lista(self):
        self.listbox_livros.delete(0, tk.END)

        try:
            with self.conectar_banco() as conexao:
                livros = conexao.execute(
                    "SELECT id, titulo, autor, ano, status FROM livros ORDER BY titulo COLLATE NOCASE"
                ).fetchall()

            self.ids_livros = []
            lidos = 0
            for livro in livros:
                livro_id, titulo, autor, ano, status = livro
                texto = titulo
                if autor:
                    texto += f" - {autor}"
                if ano:
                    texto += f" ({ano})"

                if status == "Lido":
                    texto = "✅ " + texto
                    lidos += 1
                else:
                    texto = "📌 " + texto

                self.listbox_livros.insert(tk.END, texto)
                self.ids_livros.append(livro_id)

            total = len(livros)
            self.label_stats.config(
                text=f"Total: {total} livros | Lidos: {lidos} | Não lidos: {total - lidos}"
            )
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao listar: {erro}")

    def obter_id_selecionado(self):
        selecao = self.listbox_livros.curselection()
        if not selecao:
            messagebox.showinfo("Aviso", "Selecione um livro!")
            return None
        return self.ids_livros[selecao[0]]

    def mostrar_detalhes(self, event=None):
        selecao = self.listbox_livros.curselection()
        if not selecao:
            return

        livro_id = self.ids_livros[selecao[0]]
        try:
            with self.conectar_banco() as conexao:
                livro = conexao.execute(
                    "SELECT id, titulo, autor, ano, status FROM livros WHERE id = ?",
                    (livro_id,)
                ).fetchone()

            if livro:
                _, titulo, autor, ano, status = livro
                detalhes = (
                    f"📖 Título: {titulo}\n"
                    f"✍️ Autor: {autor or 'Não informado'}\n"
                    f"📅 Ano: {ano if ano is not None else 'Não informado'}\n"
                    f"📌 Status: {status}"
                )
                self.label_detalhes.config(text=detalhes)
        except sqlite3.Error as erro:
            self.label_detalhes.config(text=f"Erro ao carregar detalhes: {erro}")

    def mudar_status(self, novo_status):
        livro_id = self.obter_id_selecionado()
        if livro_id is None:
            return

        try:
            with self.conectar_banco() as conexao:
                conexao.execute(
                    "UPDATE livros SET status = ? WHERE id = ?",
                    (novo_status, livro_id)
                )
            self.atualizar_lista()
            self.label_detalhes.config(text="")
            messagebox.showinfo("Sucesso", f"Livro marcado como {novo_status}!")
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Falha ao atualizar status: {erro}")

    def remover_livro(self):
        livro_id = self.obter_id_selecionado()
        if livro_id is None:
            return

        if not messagebox.askyesno("Confirmar", "Remover este livro da biblioteca?"):
            return

        try:
            with self.conectar_banco() as conexao:
                conexao.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
            self.atualizar_lista()
            self.limpar_campos()
            self.label_detalhes.config(text="Selecione um livro para ver os detalhes.")
            messagebox.showinfo("Sucesso", "Livro removido!")
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Falha ao remover livro: {erro}")

    def limpar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.status.set("Não Lido")
        self.entry_titulo.focus()


if __name__ == "__main__":
    janela = tk.Tk()
    app = BibliotecaPessoal(janela)
    janela.mainloop()
