import customtkinter as ctk

# Configuração de Aparência Padrão
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class AppOrdensServico(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Identificação da Janela
        self.title("Field Service - Gestão e Controle de Ordens de Serviço")

        # Dimensões e Centralização da Tela (Center Screen)
        largura = 820
        altura = 600
        self.centralizar_janela(largura, altura)

        # Contador de ID e Base de Dados Inicial Simulada
        self.contador_id = 105
        self.ordens = [
            (
                "OS-2026-101",
                "Banco Alpha S/A",
                "Manutenção de Servidores Racks",
                "Alta",
                "R$ 4.500,00",
                "Em Execução",
                "#3b82f6",
                4500.00,
            ),
            (
                "OS-2026-102",
                "Varejo Express Ltda",
                "Troca de Nobreaks no PDV",
                "Média",
                "R$ 1.200,00",
                "Em Aberto",
                "#f59e0b",
                1200.00,
            ),
            (
                "OS-2026-103",
                "Indústrias Metalúrgicas",
                "Instalação de Fibra Óptica",
                "Crítica",
                "R$ 8.900,00",
                "Em Aberto",
                "#f59e0b",
                8900.00,
            ),
            (
                "OS-2026-104",
                "Tech Startups Hub",
                "Auditoria de Infraestrutura de Rede",
                "Baixa",
                "R$ 2.300,00",
                "Concluída",
                "#22c55e",
                2300.00,
            ),
        ]

        # Título do Módulo
        self.lbl_title = ctk.CTkLabel(
            self,
            text="GESTÃO DE ORDENS DE SERVIÇO E MANUTENÇÃO (FIELD SERVICE)",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.lbl_title.pack(pady=(15, 10))

        # --- SEÇÃO 1: FORMULÁRIO DE ABERTURA DE O.S. ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(fill="x", padx=20, pady=5)

        self.lbl_form_title = ctk.CTkLabel(
            self.frame_form,
            text="Abertura de Nova Ordem de Serviço",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_form_title.grid(
            row=0, column=0, columnspan=4, padx=10, pady=(8, 4), sticky="w"
        )

        self.entry_cliente = ctk.CTkEntry(
            self.frame_form, placeholder_text="Cliente / Razão Social", width=220
        )
        self.entry_cliente.grid(row=1, column=0, padx=8, pady=8)

        self.entry_descricao = ctk.CTkEntry(
            self.frame_form, placeholder_text="Descrição do Serviço", width=260
        )
        self.entry_descricao.grid(row=1, column=1, padx=8, pady=8)

        self.entry_valor = ctk.CTkEntry(
            self.frame_form, placeholder_text="Custo Estimado (R$)", width=130
        )
        self.entry_valor.grid(row=1, column=2, padx=8, pady=8)

        self.opt_prioridade = ctk.CTkOptionMenu(
            self.frame_form,
            values=["Baixa", "Média", "Alta", "Crítica"],
            width=110,
        )
        self.opt_prioridade.grid(row=1, column=3, padx=8, pady=8)
        self.opt_prioridade.set("Média")

        self.btn_abrir_os = ctk.CTkButton(
            self.frame_form,
            text="Abrir Nova Ordem de Serviço",
            command=self.cadastrar_os,
        )
        self.btn_abrir_os.grid(
            row=2, column=0, columnspan=4, padx=10, pady=(0, 10)
        )

        # --- SEÇÃO 2: BARRA DE PESQUISA / FILTRO ---
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(fill="x", padx=20, pady=10)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Buscar por Cliente, ID da O.S. ou Serviço...",
            width=500,
        )
        self.entry_busca.pack(side="left", padx=10, pady=10)

        self.btn_filtrar = ctk.CTkButton(
            self.frame_busca,
            text="Filtrar O.S.",
            width=130,
            command=self.filtrar_dados,
        )
        self.btn_filtrar.pack(side="left", padx=5, pady=10)

        # --- SEÇÃO 3: TABELA / GRID SCROLLÁVEL ---
        self.grid_container = ctk.CTkScrollableFrame(
            self, label_text="Painel de Ordens de Serviço Ativas"
        )
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Carregar Tabela Inicial
        self.carregar_tabela(self.ordens)

        # --- SEÇÃO 4: RODAPÉ DE RESUMO FINANCEIRO ---
        self.lbl_total_orcamento = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3b82f6",
        )
        self.lbl_total_orcamento.pack(pady=10)
        self.atualizar_resumo_financeiro()

    def centralizar_janela(self, largura, altura):
        """Calcula e posiciona a janela centralizada na tela do monitor (Center Screen)."""
        self.update_idletasks()

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def carregar_tabela(self, lista):
        """Renderiza os dados dentro do container scrollável."""
        # Limpar widgets anteriores
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # Cabeçalhos
        headers = [
            "ID O.S.",
            "Cliente",
            "Serviço Solicitado",
            "Prioridade",
            "Valor Est.",
            "Status",
        ]
        for col, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.grid_container,
                text=header,
                font=ctk.CTkFont(weight="bold"),
            )
            lbl.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Inserção das Linhas
        for row, (os_id, cliente, servico, prioridade, valor_str, status, cor_status, _) in enumerate(
            lista, start=1
        ):
            ctk.CTkLabel(self.grid_container, text=os_id).grid(
                row=row, column=0, padx=10, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=cliente).grid(
                row=row, column=1, padx=10, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=servico).grid(
                row=row, column=2, padx=10, pady=4, sticky="w"
            )
            ctk.CTkLabel(self.grid_container, text=prioridade).grid(
                row=row, column=3, padx=10, pady=4, sticky="w"
            )
            ctk.CTkLabel(
                self.grid_container,
                text=valor_str,
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=row, column=4, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(
                self.grid_container,
                text=status,
                text_color=cor_status,
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=row, column=5, padx=10, pady=4, sticky="w")

    def cadastrar_os(self):
        """Lê o formulário e adiciona uma nova Ordem de Serviço à lista."""
        cliente = self.entry_cliente.get().strip()
        servico = self.entry_descricao.get().strip()
        valor_raw = self.entry_valor.get().strip()
        prioridade = self.opt_prioridade.get()

        if cliente and servico and valor_raw:
            try:
                valor_num = float(valor_raw.replace(",", "."))
                valor_str = f"R$ {valor_num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                os_id = f"OS-2026-{self.contador_id}"
                self.contador_id += 1

                # Nova OS entra como "Em Aberto" (Laranja)
                nova_os = (
                    os_id,
                    cliente,
                    servico,
                    prioridade,
                    valor_str,
                    "Em Aberto",
                    "#f59e0b",
                    valor_num,
                )
                self.ordens.append(nova_os)

                # Atualizar Tabela e Totais
                self.carregar_tabela(self.ordens)
                self.atualizar_resumo_financeiro()

                # Limpar campos
                self.entry_cliente.delete(0, "end")
                self.entry_descricao.delete(0, "end")
                self.entry_valor.delete(0, "end")

            except ValueError:
                pass  # Ignora caso o valor digitado não seja numérico válido

    def filtrar_dados(self):
        """Filtra a tabela pelo cliente, ID da OS ou serviço."""
        termo = self.entry_busca.get().lower().strip()
        filtrados = [
            o
            for o in self.ordens
            if termo in o[0].lower() or termo in o[1].lower() or termo in o[2].lower()
        ]
        self.carregar_tabela(filtrados)

    def atualizar_resumo_financeiro(self):
        """Soma o valor total das OSs e exibe no rodapé."""
        total_acumulado = sum(o[7] for o in self.ordens)
        total_str = f"R$ {total_acumulado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.lbl_total_orcamento.configure(
            text=f"Total em Serviços Orçados/Abertos: {total_str} ({len(self.ordens)} Ordens Registradas)"
        )


if __name__ == "__main__":
    app = AppOrdensServico()
    app.mainloop()
