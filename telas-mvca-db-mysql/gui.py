import tkinter as tk
from tkinter import messagebox
import banco  # Importa o arquivo banco.py que você criou

class AplicaçãoLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Acesso")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        # Container principal para alternar telas
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Inicia abrindo a tela de Login
        self.criar_tela_login()

    def limpar_container(self):
        """Remove todos os widgets da tela atual para desenhar a próxima."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- TELA 1: LOGIN ---
    def criar_tela_login(self):
        self.limpar_container()

        tk.Label(self.container, text="Acesso ao Sistema", font=("Arial", 14, "bold")).pack(pady=15)

        tk.Label(self.container, text="Usuário:").pack(anchor="w", padx=30)
        self.ent_user_login = tk.Entry(self.container, width=30)
        self.ent_user_login.pack(padx=30, pady=5)

        tk.Label(self.container, text="Senha:").pack(anchor="w", padx=30)
        self.ent_pass_login = tk.Entry(self.container, show="*", width=30)
        self.ent_pass_login.pack(padx=30, pady=5)

        btn_login = tk.Button(self.container, text="LOGIN", bg="#4CAF50", fg="white", width=15, command=self.executar_login)
        btn_login.pack(pady=15)

    def executar_login(self):
        user = self.ent_user_login.get()
        senha = self.ent_pass_login.get()

        if not user or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        # Chama a função importada do banco.py
        if banco.validar_login(user, senha):
            messagebox.showinfo("Sucesso", "Login realizado!")
            self.criar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    # --- TELA 2: PRINCIPAL (CADASTRO E SAIR) ---
    def criar_tela_principal(self):
        self.limpar_container()

        tk.Label(self.container, text="Painel Principal", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.container, text="Novo Usuário:").pack(anchor="w", padx=30)
        self.ent_user_cad = tk.Entry(self.container, width=30)
        self.ent_user_cad.pack(padx=30, pady=2)

        tk.Label(self.container, text="Nova Senha:").pack(anchor="w", padx=30)
        self.ent_pass_cad = tk.Entry(self.container, show="*", width=30)
        self.ent_pass_cad.pack(padx=30, pady=2)

        # Frame para organizar os botões lado a lado
        frame_botoes = tk.Frame(self.container)
        frame_botoes.pack(pady=15)

        btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", bg="#2196F3", fg="white", width=10, command=self.executar_cadastro)
        btn_cadastrar.pack(side="left", padx=5)

        btn_sair = tk.Button(frame_botoes, text="Sair", bg="#f44336", fg="white", width=10, command=self.criar_tela_login)
        btn_sair.pack(side="left", padx=5)

    def executar_cadastro(self):
        user = self.ent_user_cad.get()
        senha = self.ent_pass_cad.get()

        if not user or not senha:
            messagebox.showwarning("Aviso", "Preencha ambos os campos para cadastrar.")
            return

        # Chama a função importada do banco.py
        sucesso, mensagem = banco.cadastrar_usuario(user, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.ent_user_cad.delete(0, tk.END)
            self.ent_pass_cad.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", mensagem)

# --- EXECUÇÃO DO PROGRAMA ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicaçãoLogin(root)
    root.mainloop()
    