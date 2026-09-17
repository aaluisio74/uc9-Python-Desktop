import customtkinter as ctk

# Configuração de Aparência e Tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppEstoque(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventory & Warehouse - Controle de Estoque e Audit Trail")
        '''self.geometry("750x500")'''
        
        # =========================================================================
        # 1. ALTERAÇÃO AQUI: Definimos largura, altura e chamamos a centralização
        # =========================================================================
        largura = 750
        altura = 500
        self.centralizar_janela(largura, altura)
        # =========================================================================

        # Cabeçalho do Módulo
        self.lbl_title = ctk.CTkLabel(
            self, 
            text="GESTÃO E AUDITORIA DE MOVIMENTAÇÃO DE ESTOQUE", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_title.pack(pady=15)

        # Barra de Pesquisa e Filtros
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(fill="x", padx=20, pady=5)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca, 
            placeholder_text="Buscar por SKU ou descrição do produto...", 
            width=360
        )
        self.entry_busca.pack(side="left", padx=10, pady=10)

        self.btn_filtrar = ctk.CTkButton(
            self.frame_busca, 
            text="Filtrar Estoque", 
            command=self.filtrar_dados
        )
        self.btn_filtrar.pack(side="left", padx=5, pady=10)

        # Tabela / Grid Scrollável
        self.grid_container = ctk.CTkScrollableFrame(self, label_text="Movimentações e Inventário")
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Dados Simulados de Estoque
        # Formato: (SKU, Produto, Categoria, Qtd Movimentada / Atual, Tipo / Status, Cor Destaque)
        self.estoque = [
            ("SKU-1082", "Notebook Dell Latitude", "Hardware", "+15 un", "Entrada (OK)", "#22c55e"),
            ("SKU-1083", "Monitor 27' 4K LG", "Periféricos", "-8 un", "Saída (OK)", "#22c55e"),
            ("SKU-1084", "Teclado Mecânico RGB", "Periféricos", "3 un", "Estoque Baixo", "#f59e0b"),
            ("SKU-1085", "Servidor Rack 2U", "Infraestrutura", "+2 un", "Entrada (OK)", "#22c55e"),
            ("SKU-1086", "Cabo HDMI 2.1 2m", "Acessórios", "0 un", "Esgotado / Crítico", "#ef4444"),
            ("SKU-1087", "Mouse Sem Fio Logitech", "Periféricos", "-12 un", "Saída (OK)", "#22c55e"),
        ]

        self.carregar_tabela(self.estoque)

        # Rodapé de Saldo e Consolidação
        self.lbl_saldo = ctk.CTkLabel(
            self, 
            text="Total Consolidado de Itens em Estoque: 342 unidades", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            text_color="#22c55e"
        )
        self.lbl_saldo.pack(pady=10)
        
    # =========================================================================
    # 2. ALTERAÇÃO AQUI: Método criado para calcular e centralizar a janela
    # =========================================================================
    def centralizar_janela(self, largura, altura):
        self.update_idletasks()  # Atualiza os eventos de tela para obter dimensões corretas do monitor
        
        # Obtém a largura e altura da tela do monitor
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # Calcula a posição X e Y para centralizar
        pos_x = int((largura_tela / 2) - (largura / 2))
        pos_y = int((altura_tela / 2) - (altura / 2))

        # Aplica a geometria no formato: "LARGURAxALTURA+POS_X+POS_Y"
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    # =========================================================================    

    def carregar_tabela(self, lista):
        # Limpar linhas existentes
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # Cabeçalhos das Colunas
        headers = ["SKU", "Produto", "Categoria", "Quantidade", "Status / Tipo"]
        for col, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.grid_container, text=h, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=col, padx=12, pady=5, sticky="w")

        # Inserção das Linhas
        for row, (sku, produto, categoria, qtd, status, cor) in enumerate(lista, start=1):
            ctk.CTkLabel(self.grid_container, text=sku).grid(row=row, column=0, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=produto).grid(row=row, column=1, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=categoria).grid(row=row, column=2, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=qtd, text_color=cor, font=ctk.CTkFont(weight="bold")).grid(row=row, column=3, padx=12, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=status, text_color=cor).grid(row=row, column=4, padx=12, pady=4, sticky="w")

    def filtrar_dados(self):
        termo = self.entry_busca.get().lower()
        filtrados = [
            item for item in self.estoque 
            if termo in item[0].lower() or termo in item[1].lower() or termo in item[2].lower()
        ]
        self.carregar_tabela(filtrados)

if __name__ == "__main__":
    app = AppEstoque()
    app.mainloop()