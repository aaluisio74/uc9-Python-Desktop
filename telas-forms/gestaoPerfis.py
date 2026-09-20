import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AppRBAC(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Security & Compliance - Configuração de Perfis (RBAC)")
        self.geometry("580x500")

        # Título
        self.lbl_title = ctk.CTkLabel(
            self, text="MATRIZ DE PERMISSÕES E PERFIS DE ACESSO", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.lbl_title.pack(pady=15)

        # Selector de Perfil
        self.frame_perfil = ctk.CTkFrame(self)
        self.frame_perfil.pack(fill="x", padx=25, pady=5)

        self.lbl_perfil = ctk.CTkLabel(self.frame_perfil, text="Selecione o Perfil:", font=ctk.CTkFont(weight="bold"))
        self.lbl_perfil.pack(side="left", padx=15, pady=12)

        self.opt_perfil = ctk.CTkOptionMenu(
            self.frame_perfil, 
            values=["Analista Operacional", "Gerente Financeiro", "Administrador de TI"],
            command=self.carregar_permissoes_perfil
        )
        self.opt_perfil.pack(side="left", padx=10, pady=12)

        # Matriz de Checkboxes
        self.frame_matriz = ctk.CTkFrame(self)
        self.frame_matriz.pack(fill="both", expand=True, padx=25, pady=15)

        self.lbl_matriz = ctk.CTkLabel(self.frame_matriz, text="Permissões do Sistema:", font=ctk.CTkFont(weight="bold"))
        self.lbl_matriz.pack(anchor="w", padx=15, pady=(10, 5))

        self.chk_financeiro = ctk.CTkCheckBox(self.frame_matriz, text="Acesso ao Módulo Financeiro & Lançamentos")
        self.chk_financeiro.pack(anchor="w", padx=20, pady=8)

        self.chk_rh = ctk.CTkCheckBox(self.frame_matriz, text="Acesso aos Dados de RH e Folha de Pagamento")
        self.chk_rh.pack(anchor="w", padx=20, pady=8)

        self.chk_relatorios = ctk.CTkCheckBox(self.frame_matriz, text="Exportação de Relatórios Executivos")
        self.chk_relatorios.pack(anchor="w", padx=20, pady=8)

        self.chk_admin = ctk.CTkCheckBox(self.frame_matriz, text="Gestão de Usuários e Configuração de Kernel")
        self.chk_admin.pack(anchor="w", padx=20, pady=8)

        # Botão de Aplicação
        self.btn_salvar = ctk.CTkButton(self, text="Aplicar Políticas de Acesso", command=self.salvar_politicas)
        self.btn_salvar.pack(pady=10)

        # Status
        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11, weight="bold"))
        self.lbl_status.pack(pady=(0, 15))

        # Carga Inicial
        self.carregar_permissoes_perfil("Analista Operacional")

    def carregar_permissoes_perfil(self, perfil):
        # Reset
        self.chk_financeiro.deselect()
        self.chk_rh.deselect()
        self.chk_relatorios.deselect()
        self.chk_admin.deselect()

        if perfil == "Analista Operacional":
            self.chk_financeiro.select()
        elif perfil == "Gerente Financeiro":
            self.chk_financeiro.select()
            self.chk_rh.select()
            self.chk_relatorios.select()
        elif perfil == "Administrador de TI":
            self.chk_financeiro.select()
            self.chk_rh.select()
            self.chk_relatorios.select()
            self.chk_admin.select()

    def salvar_politicas(self):
        perfil = self.opt_perfil.get()
        self.lbl_status.configure(
            text=f"[POLÍTICA ATUALIZADA] Permissões do perfil '{perfil}' gravadas com sucesso.",
            text_color="#22c55e"
        )

if __name__ == "__main__":
    app = AppRBAC()
    app.mainloop()
