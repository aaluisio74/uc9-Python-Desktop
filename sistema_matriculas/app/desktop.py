
# ============================================================
# PARTE 1 — IMPORTAÇÕES
# tkinter: componentes da interface gráfica
# requests: comunicação HTTP com a API
# ============================================================
import tkinter as tk
from tkinter import ttk, messagebox

import requests


# ============================================================
# PARTE 2 — CONFIGURAÇÃO DO CLIENTE DESKTOP
# A API deve estar em execução antes de abrir esta tela.
# ============================================================
API_URL = "http://127.0.0.1:8000"


# ============================================================
# PARTE 3 — CLASSE PRINCIPAL DA APLICAÇÃO DESKTOP
# Responsável pela janela, autenticação e interação com a API.
# ============================================================
class SistemaMatriculasDesktop:

    # PARTE 3.1 — Inicialização da janela
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema de Matrículas")
        self.janela.geometry("850x550")

        # Token recebido após o login.
        self.token = None

        # Guarda o ID do estudante selecionado.
        self.estudante_id = None

        # Cabeçalho usado nas requisições protegidas.
        self.headers = {}

        # Monta a tela de login.
        self.montar_tela_login()

    # ========================================================
    # PARTE 4 — TELA DE LOGIN
    # Recebe usuário e senha.
    # ========================================================
    def montar_tela_login(self):
        self.limpar_tela()

        quadro = ttk.Frame(self.janela, padding=20)
        quadro.pack(expand=True)

        ttk.Label(
            quadro, text="Acesso ao Sistema",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        ttk.Label(quadro, text="Usuário").pack(anchor="w")
        self.campo_usuario = ttk.Entry(quadro, width=35)
        self.campo_usuario.pack(pady=5)

        ttk.Label(quadro, text="Senha").pack(anchor="w")
        self.campo_senha = ttk.Entry(
            quadro, width=35, show="*"
        )
        self.campo_senha.pack(pady=5)

        ttk.Button(
            quadro,
            text="Entrar",
            command=self.fazer_login,
        ).pack(pady=12)

    # ========================================================
    # PARTE 5 — AUTENTICAÇÃO
    # Envia as credenciais à API e recebe o token.
    # ========================================================
    def fazer_login(self):
        try:
            resposta = requests.post(
                f"{API_URL}/token",
                data={
                    "username": self.campo_usuario.get(),
                    "password": self.campo_senha.get(),
                },
                timeout=5,
            )

            if resposta.status_code != 200:
                messagebox.showerror(
                    "Acesso negado",
                    "Usuário ou senha inválidos."
                )
                return

            self.token = resposta.json()["access_token"]
            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }

            # Após o login, abre a tela principal.
            self.montar_tela_principal()

        except requests.RequestException:
            messagebox.showerror(
                "Erro de conexão",
                "Não foi possível conectar à API."
            )

    # ========================================================
    # PARTE 6 — TELA PRINCIPAL
    # Exibe formulário, lista e botões de operação.
    # ========================================================
    def montar_tela_principal(self):
        self.limpar_tela()

        quadro = ttk.Frame(self.janela, padding=12)
        quadro.pack(fill="both", expand=True)

        ttk.Label(
            quadro,
            text="Cadastro de Estudantes",
            font=("Arial", 16, "bold"),
        ).pack(pady=8)

        formulario = ttk.Frame(quadro)
        formulario.pack(fill="x", pady=8)

        ttk.Label(formulario, text="Nome").grid(
            row=0, column=0, sticky="w"
        )
        self.campo_nome = ttk.Entry(formulario, width=35)
        self.campo_nome.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(formulario, text="E-mail").grid(
            row=1, column=0, sticky="w"
        )
        self.campo_email = ttk.Entry(formulario, width=35)
        self.campo_email.grid(row=1, column=1, padx=5, pady=4)

        # Lista que apresenta os estudantes cadastrados.
        self.lista = ttk.Treeview(
            quadro,
            columns=("id", "nome", "email"),
            show="headings",
            height=12,
        )
        self.lista.heading("id", text="ID")
        self.lista.heading("nome", text="Nome")
        self.lista.heading("email", text="E-mail")
        self.lista.pack(fill="both", expand=True, pady=8)

        # Guarda o ID do registro selecionado.
        self.lista.bind(
            "<<TreeviewSelect>>",
            self.selecionar_estudante,
        )

        # Botões de operações CRUD.
        botoes = ttk.Frame(quadro)
        botoes.pack(fill="x", pady=5)

        ttk.Button(
            botoes, text="Cadastrar",
            command=self.cadastrar_estudante,
        ).pack(side="left", padx=3)

        ttk.Button(
            botoes, text="Atualizar",
            command=self.atualizar_estudante,
        ).pack(side="left", padx=3)

        ttk.Button(
            botoes, text="Excluir",
            command=self.excluir_estudante,
        ).pack(side="left", padx=3)

        ttk.Button(
            botoes, text="Atualizar lista",
            command=self.carregar_estudantes,
        ).pack(side="left", padx=3)

        # Consulta os registros após montar a interface.
        self.carregar_estudantes()

    # ========================================================
    # PARTE 7 — READ: LISTAR ESTUDANTES PELA API
    # ========================================================
    def carregar_estudantes(self):
        try:
            resposta = requests.get(
                f"{API_URL}/estudantes",
                headers=self.headers,
                timeout=5,
            )
            resposta.raise_for_status()

            # Limpa a lista antes de inserir os novos dados.
            for item in self.lista.get_children():
                self.lista.delete(item)

            # Preenche a lista com os registros retornados.
            for estudante in resposta.json():
                self.lista.insert(
                    "",
                    "end",
                    values=(
                        estudante["id"],
                        estudante["nome"],
                        estudante["email"],
                    ),
                )

        except requests.RequestException:
            messagebox.showerror(
                "Erro",
                "Não foi possível carregar os estudantes."
            )

    # ========================================================
    # PARTE 8 — SELECIONAR UM REGISTRO
    # Copia os dados selecionados para o formulário.
    # ========================================================
    def selecionar_estudante(self, evento=None):
        selecao = self.lista.selection()

        if not selecao:
            return

        valores = self.lista.item(selecao[0], "values")

        self.estudante_id = int(valores[0])
        self.campo_nome.delete(0, tk.END)
        self.campo_nome.insert(0, valores[1])

        self.campo_email.delete(0, tk.END)
        self.campo_email.insert(0, valores[2])

    # ========================================================
    # PARTE 9 — CREATE: CADASTRAR ESTUDANTE
    # ========================================================
    def cadastrar_estudante(self):
        dados = {
            "nome": self.campo_nome.get().strip(),
            "email": self.campo_email.get().strip(),
        }

        if not dados["nome"] or not dados["email"]:
            messagebox.showwarning(
                "Validação",
                "Preencha o nome e o e-mail."
            )
            return

        try:
            resposta = requests.post(
                f"{API_URL}/estudantes",
                json=dados,
                headers=self.headers,
                timeout=5,
            )

            if resposta.status_code == 201:
                messagebox.showinfo(
                    "Sucesso", "Estudante cadastrado."
                )
                self.carregar_estudantes()
                self.limpar_formulario()
            else:
                messagebox.showerror(
                    "Falha",
                    resposta.json().get(
                        "detail", "Não foi possível cadastrar."
                    ),
                )

        except requests.RequestException:
            messagebox.showerror(
                "Erro", "Falha de comunicação com a API."
            )

    # ========================================================
    # PARTE 10 — UPDATE: ATUALIZAR ESTUDANTE
    # ========================================================
    def atualizar_estudante(self):
        if self.estudante_id is None:
            messagebox.showwarning(
                "Seleção",
                "Selecione um estudante na lista."
            )
            return

        dados = {
            "nome": self.campo_nome.get().strip(),
            "email": self.campo_email.get().strip(),
        }

        try:
            resposta = requests.put(
                f"{API_URL}/estudantes/{self.estudante_id}",
                json=dados,
                headers=self.headers,
                timeout=5,
            )

            if resposta.status_code == 200:
                messagebox.showinfo(
                    "Sucesso", "Estudante atualizado."
                )
                self.carregar_estudantes()
                self.limpar_formulario()
            else:
                messagebox.showerror(
                    "Falha",
                    resposta.json().get(
                        "detail", "Não foi possível atualizar."
                    ),
                )

        except requests.RequestException:
            messagebox.showerror(
                "Erro", "Falha de comunicação com a API."
            )

    # ========================================================
    # PARTE 11 — DELETE: EXCLUIR ESTUDANTE
    # ========================================================
    def excluir_estudante(self):
        if self.estudante_id is None:
            messagebox.showwarning(
                "Seleção",
                "Selecione um estudante na lista."
            )
            return

        # Solicita confirmação antes da exclusão.
        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja excluir o estudante selecionado?"
        )

        if not confirmar:
            return

        try:
            resposta = requests.delete(
                f"{API_URL}/estudantes/{self.estudante_id}",
                headers=self.headers,
                timeout=5,
            )

            if resposta.status_code == 200:
                messagebox.showinfo(
                    "Sucesso", "Estudante excluído."
                )
                self.carregar_estudantes()
                self.limpar_formulario()
            else:
                messagebox.showerror(
                    "Falha",
                    resposta.json().get(
                        "detail", "Não foi possível excluir."
                    ),
                )

        except requests.RequestException:
            messagebox.showerror(
                "Erro", "Falha de comunicação com a API."
            )

    # ========================================================
    # PARTE 12 — LIMPAR O FORMULÁRIO
    # ========================================================
    def limpar_formulario(self):
        self.estudante_id = None
        self.campo_nome.delete(0, tk.END)
        self.campo_email.delete(0, tk.END)

    # ========================================================
    # PARTE 13 — RECONSTRUIR A TELA
    # Remove os componentes existentes.
    # ========================================================
    def limpar_tela(self):
        for componente in self.janela.winfo_children():
            componente.destroy()


# ============================================================
# PARTE 14 — PONTO DE ENTRADA DO PROGRAMA DESKTOP
# Cria a janela e inicia o loop de eventos do Tkinter.
# ============================================================
if __name__ == "__main__":
    janela = tk.Tk()
    aplicacao = SistemaMatriculasDesktop(janela)
    janela.mainloop()
