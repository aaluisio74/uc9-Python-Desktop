import customtkinter as ctk

# Configurações globais de aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class AppControleVendas(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("Sales Control - Registro de Vendas e Checkout")

        # Dimensões da janela
        largura = 760
        altura = 580

        # Aplica centralização na tela (Center Screen)
        self.centralizar_janela(largura, altura)

        # Contador de ID de Venda e Histórico Inicial de Vendas
        self.contador_id = 105
        self.vendas = [
            ("VEN-0101", "Notebook Corporativo", 2, "R$ 9.000,00", "PIX", 9000.00),
            ("VEN-0102", "Monitor 27' 4K", 1, "R$ 2.300,00", "Cartão de Crédito", 2300.00),
            ("VEN-0103", "Teclado Mecânico RGB", 3, "R$ 1.050,00", "PIX", 1050.00),
            ("VEN-0104", "Cadeira Ergonômica", 1, "R$ 1.850,00", "Boleto", 1850.00),
        ]

        # Título da Aplicação
        self.lbl_title = ctk.CTkLabel(
            self,
            text="SISTEMA DE CONTROLE DE VENDAS E CHECKOUT",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_title.pack(pady=(15, 10))

        # --- SEÇÃO 1: FORMULÁRIO DE LANÇAMENTO DE VENDA ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(fill="x", padx=20, pady=5)

        self.lbl_form_title = ctk.CTkLabel(
            self.frame_form,
            text="Registrar Nova Venda",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_form_title.grid(
            row=0, column=0, columnspan=3, padx=10, pady=(8, 4), sticky="w"
        )

        self.entry_produto = ctk.CTkEntry(
            self.frame_form, placeholder_text="Descrição do Produto", width=260
        )
        self.entry_produto.grid(row=1, column=0, padx=10, pady=8)

        self.entry_qtd = ctk.CTkEntry(
            self.frame_form, placeholder_text="Qtd", width=100
        )
        self.entry_qtd.grid(row=1, column=1, padx=10, pady=8)

        self.entry_valor = ctk.CTkEntry(
            self.frame_form, placeholder_text="Preço Un. (R$)", width=140
        )
        self.entry_valor.grid(row=1, column=2, padx=10, pady=8)

        self.opt_pagamento = ctk.CTkOptionMenu(
            self.frame_form,
            values=["PIX", "Cartão de Crédito", "Cartão de Débito", "Boleto"],
            width=150,
        )
        self.opt_pagamento.grid(row=1, column=3, padx=10, pady=8)

        self.btn_registrar = ctk.CTkButton(
            self.frame_form,
            text="Finalizar Venda",
            command=self.registrar_venda,
        )
        self.btn_registrar.grid(
            row=2, column=0, columnspan=4, padx=10, pady=(0, 10)
        )

        # --- SEÇÃO 2: BARRA DE FILTRO / BUSCA ---
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(fill="x", padx=20, pady=10)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Buscar por Produto ou ID da Venda...",
            width=450,
        )
        self.entry_busca.pack(side="left", padx=10, pady=10)

        self.btn_filtrar = ctk.CTkButton(
            self.frame_busca,
            text="Filtrar Vendas",
            width=130,
            command=self.filtrar_dados,
        )
        self.btn_filtrar.pack(side="left", padx=5, pady=10)

        # --- SEÇÃO 3: TABELA / GRID SCROLLÁVEL ---
        self.grid_container = ctk.CTkScrollableFrame(
            self, label_text="Histórico de Vendas Realizadas"
        )
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Carrega os dados na tabela
        self.carregar_tabela(self.vendas)

        # --- SEÇÃO 4: RODAPÉ COM TOTALIZADOR ---
        self.lbl_total_faturamento = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#22c55e",
        )
        self.lbl_total_faturamento.pack(pady=10)
        self.atualizar_faturamento()

    def centralizar_janela(self, largura, altura):
        """Calcula e aplica o posicionamento centralizado da janela na tela."""
        self.update_idletasks()

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def carregar_tabela(self, lista):
        """Preenche o grid com as linhas do histórico de vendas."""
        # Limpa elementos anteriores
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # Cabeçalho do Grid
        headers = ["ID Venda", "Produto", "Qtd", "Valor Total", "Forma Pagamento"]
        for col, h in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.grid_container, text=h, font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(row=0, column=col, padx=15, pady=5, sticky="w")

        # Linhas de Dados
        for row, (venda_id, produto, qtd, valor_str, pagto, _) in enumerate(
            lista, start=1
        ):
            ctk.CTkLabel(self.grid_container, text=venda_id).grid(
                row=row, column=0, padx=15, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=produto).grid(
                row=row, column=1, padx=15, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=str(qtd)).grid(
                row=row, column=2, padx=15, pady=4, sticky="w"
            )
            ctk.CTkLabel(
                self.grid_container,
                text=valor_str,
                text_color="#22c55e",
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=row, column=3, padx=15, pady=4, sticky="w")
            ctk.CTkLabel(self.grid_container, text=pagto).grid(
                row=row, column=4, padx=15, pady=4, sticky="w"
            )

    def registrar_venda(self):
        """Lê os valores digitados, realiza o cálculo do valor total e atualiza a interface."""
        produto = self.entry_produto.get().strip()
        qtd_raw = self.entry_qtd.get().strip()
        valor_raw = self.entry_valor.get().strip()
        pagto = self.opt_pagamento.get()

        if produto and qtd_raw.isdigit():
            try:
                qtd = int(qtd_raw)
                valor_unitario = float(valor_raw.replace(",", "."))
                valor_total_num = qtd * valor_unitario
                valor_total_str = f"R$ {valor_total_num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                venda_id = f"VEN-0{self.contador_id}"
                self.contador_id += 1

                nova_venda = (venda_id, produto, qtd, valor_total_str, pagto, valor_total_num)
                self.vendas.append(nova_venda)

                # Atualiza a tabela e recalcula o faturamento total
                self.carregar_tabela(self.vendas)
                self.atualizar_faturamento()

                # Reseta o formulário
                self.entry_produto.delete(0, "end")
                self.entry_qtd.delete(0, "end")
                self.entry_valor.delete(0, "end")

            except ValueError:
                pass  # Ignora se o preço unitário for inválido

    def filtrar_dados(self):
        """Filtra as vendas exibidas pelo nome do produto ou ID."""
        termo = self.entry_busca.get().lower().strip()
        filtrados = [
            v
            for v in self.vendas
            if termo in v[0].lower() or termo in v[1].lower()
        ]
        self.carregar_tabela(filtrados)

    def atualizar_faturamento(self):
        """Calcula o somatório total de vendas e atualiza o rodapé."""
        total = sum(venda[5] for venda in self.vendas)
        total_str = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.lbl_total_faturamento.configure(
            text=f"Faturamento Total Consolidado: {total_str}"
        )


if __name__ == "__main__":
    app = AppControleVendas()
    app.mainloop()
