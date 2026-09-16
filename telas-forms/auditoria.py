import customtkinter as ctk

# Configuração de Aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppTransacoes(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ERP Financial - Livro Razão e Audit Trail")
        self.geometry("700x480")

        # Cabeçalho do Módulo
        self.lbl_title = ctk.CTkLabel(
            self, text="REGISTRO DE TRANSAÇÕES FINANCEIRAS (LEDGER)", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_title.pack(pady=15)

        # Barra de Pesquisa e Filtros
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(fill="x", padx=20, pady=5)

        self.entry_busca = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar por descrição ou ID...", width=320)
        self.entry_busca.pack(side="left", padx=10, pady=10)

        self.btn_filtrar = ctk.CTkButton(self.frame_busca, text="Filtrar Transações", command=self.filtrar_dados)
        self.btn_filtrar.pack(side="left", padx=5, pady=10)

        # Tabela / Grid Scrollável
        self.grid_container = ctk.CTkScrollableFrame(self, label_text="Histórico de Lançamentos")
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Dados Simulados
        self.transacoes = [
            ("TRX-9012", "16/09/2026", "Pagamento Fornecedor A", "R$ -14.500,00", "Concluído", "#22c55e"),
            ("TRX-9013", "16/09/2026", "Recebimento Cliente X", "R$ +32.100,00", "Concluído", "#22c55e"),
            ("TRX-9014", "16/09/2026", "Tarifa Operacional B3", "R$ -850,00", "Pendente", "#f59e0b"),
            ("TRX-9015", "15/09/2026", "Aporte de Capital", "R$ +100.000,00", "Concluído", "#22c55e"),
            ("TRX-9016", "15/09/2026", "Reembolso Corporativo", "R$ -1.250,00", "Estornado", "#ef4444"),
        ]

        self.carregar_tabela(self.transacoes)

        # Rodapé de Saldo Consolidação
        self.lbl_saldo = ctk.CTkLabel(
            self, text="Saldo Consolidado do Período: R$ +115.500,00", 
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#22c55e"
        )
        self.lbl_saldo.pack(pady=10)

    def carregar_tabela(self, lista):
        # Limpar linhas existentes
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # Cabeçalhos das Colunas
        headers = ["ID Transação", "Data", "Descrição", "Valor", "Status"]
        for col, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.grid_container, text=h, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Inserção das Linhas
        for row, (trx_id, data, desc, valor, status, cor) in enumerate(lista, start=1):
            ctk.CTkLabel(self.grid_container, text=trx_id).grid(row=row, column=0, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=data).grid(row=row, column=1, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=desc).grid(row=row, column=2, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=valor, text_color=cor, font=ctk.CTkFont(weight="bold")).grid(row=row, column=3, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=status, text_color=cor).grid(row=row, column=4, padx=10, pady=4, sticky="w")

    def filtrar_dados(self):
        termo = self.entry_busca.get().lower()
        filtrados = [t for t in self.transacoes if termo in t[0].lower() or termo in t[2].lower()]
        self.carregar_tabela(filtrados)

if __name__ == "__main__":
    app = AppTransacoes()
    app.mainloop()
