import customtkinter as ctk
from datetime import datetime

# Configurações globais de aparência do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class AppCadastroEmpresas(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configurações básicas da janela
        self.title("Corporate ERP - Sistema de Cadastro de Empresas")

        # Define as dimensões da janela
        largura = 780
        altura = 560

        # Aplica a centralização da janela na tela (Center Screen)
        self.centralizar_janela(largura, altura)

        # Base de dados simulada inicial
        self.empresas = [
            (
                "12.345.678/0001-90",
                "TechSolutions Ltda",
                "Tecnologia",
                "10/01/2026",
                "Ativa",
                "#22c55e",
            ),
            (
                "98.765.432/0001-10",
                "Logística Brasil S/A",
                "Transportes",
                "15/02/2026",
                "Ativa",
                "#22c55e",
            ),
            (
                "45.123.890/0001-55",
                "Global Serviços Financeiros",
                "Consultoria",
                "01/03/2026",
                "Em Análise",
                "#f59e0b",
            ),
            (
                "33.987.111/0001-22",
                "Comércio de Alimentos Silva",
                "Varejo",
                "12/03/2026",
                "Inativa",
                "#ef4444",
            ),
        ]

        # Cabeçalho Principal do Módulo
        self.lbl_title = ctk.CTkLabel(
            self,
            text="SISTEMA DE CADASTRO E DIRETÓRIO DE EMPRESAS",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_title.pack(pady=(15, 10))

        # --- SEÇÃO 1: FORMULÁRIO DE CADASTRO ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(fill="x", padx=20, pady=5)

        self.lbl_form_title = ctk.CTkLabel(
            self.frame_form,
            text="Nova Empresa",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_form_title.grid(
            row=0, column=0, columnspan=3, padx=10, pady=(8, 4), sticky="w"
        )

        self.entry_razao = ctk.CTkEntry(
            self.frame_form, placeholder_text="Razão Social", width=260
        )
        self.entry_razao.grid(row=1, column=0, padx=10, pady=8)

        self.entry_cnpj = ctk.CTkEntry(
            self.frame_form, placeholder_text="CNPJ (00.000.000/0000-00)", width=200
        )
        self.entry_cnpj.grid(row=1, column=1, padx=10, pady=8)

        self.entry_segmento = ctk.CTkEntry(
            self.frame_form, placeholder_text="Segmento / Atuação", width=180
        )
        self.entry_segmento.grid(row=1, column=2, padx=10, pady=8)

        self.btn_cadastrar = ctk.CTkButton(
            self.frame_form,
            text="Cadastrar Empresa",
            command=self.cadastrar_empresa,
        )
        self.btn_cadastrar.grid(
            row=2, column=0, columnspan=3, padx=10, pady=(0, 10)
        )

        # --- SEÇÃO 2: BARRA DE FILTRO / PESQUISA ---
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(fill="x", padx=20, pady=10)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Buscar por Razão Social ou CNPJ...",
            width=450,
        )
        self.entry_busca.pack(side="left", padx=10, pady=10)

        self.btn_filtrar = ctk.CTkButton(
            self.frame_busca,
            text="Filtrar",
            width=120,
            command=self.filtrar_dados,
        )
        self.btn_filtrar.pack(side="left", padx=5, pady=10)

        # --- SEÇÃO 3: TABELA / GRID SCROLLÁVEL ---
        self.grid_container = ctk.CTkScrollableFrame(
            self, label_text="Empresas Cadastradas"
        )
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Carrega a tabela inicialmente com os dados base
        self.carregar_tabela(self.empresas)

        # --- SEÇÃO 4: RODAPÉ / INDICADOR DE TOTAL ---
        self.lbl_total = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3b82f6",
        )
        self.lbl_total.pack(pady=10)
        self.atualizar_contador(len(self.empresas))

    def centralizar_janela(self, largura, altura):
        """Calcula a posição x, y da tela para centralizar a janela do CustomTkinter."""
        # Atualiza as tarefas do sistema para obter as dimensões exatas da tela
        self.update_idletasks()

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # Cálculo das coordenadas centrais
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)

        # Define a geometria no formato: LARGURAxALTURA+POS_X+POS_Y
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def carregar_tabela(self, lista):
        """Renderiza as colunas e linhas dentro do CTkScrollableFrame."""
        # Limpar registros atuais
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # Cabeçalhos das Colunas
        headers = ["CNPJ", "Razão Social", "Segmento", "Data Cadastro", "Status"]
        for col, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.grid_container,
                text=header,
                font=ctk.CTkFont(weight="bold"),
            )
            lbl.grid(row=0, column=col, padx=12, pady=5, sticky="w")

        # Preenchimento das Linhas
        for row, (cnpj, razao, segmento, data_cad, status, cor) in enumerate(
            lista, start=1
        ):
            ctk.CTkLabel(self.grid_container, text=cnpj).grid(
                row=row, column=0, padx=12, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=razao).grid(
                row=row, column=1, padx=12, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=segmento).grid(
                row=row, column=2, padx=12, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=data_cad).grid(
                row=row, column=3, padx=12, pady=4, sticky="w"
            )
            ctk.CTkLabel(
                self.grid_container,
                text=status,
                text_color=cor,
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=row, column=4, padx=12, pady=4, sticky="w")

    def cadastrar_empresa(self):
        """Captura os valores do formulário e insere na lista de dados."""
        razao = self.entry_razao.get().strip()
        cnpj = self.entry_cnpj.get().strip()
        segmento = self.entry_segmento.get().strip()

        if razao and cnpj and segmento:
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            # Adiciona nova empresa com status padrão 'Ativa'
            nova_empresa = (
                cnpj,
                razao,
                segmento,
                data_hoje,
                "Ativa",
                "#22c55e",
            )
            self.empresas.append(nova_empresa)

            # Recarrega a tabela e atualiza o totalizador
            self.carregar_tabela(self.empresas)
            self.atualizar_contador(len(self.empresas))

            # Limpa os campos do formulário
            self.entry_razao.delete(0, "end")
            self.entry_cnpj.delete(0, "end")
            self.entry_segmento.delete(0, "end")

    def filtrar_dados(self):
        """Filtra as empresas cadastradas por CNPJ ou Razão Social."""
        termo = self.entry_busca.get().lower().strip()
        filtrados = [
            emp
            for emp in self.empresas
            if termo in emp[0].lower() or termo in emp[1].lower()
        ]
        self.carregar_tabela(filtrados)
        self.atualizar_contador(len(filtrados))

    def atualizar_contador(self, total):
        """Atualiza a mensagem no rodapé."""
        self.lbl_total.configure(
            text=f"Total de Empresas Listadas: {total} registro(s)"
        )


if __name__ == "__main__":
    app = AppCadastroEmpresas()
    app.mainloop()