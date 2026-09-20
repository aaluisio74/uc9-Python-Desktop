import tkinter as tk
from tkinter import ttk, messagebox

def centralizar_janela(janela, largura, altura):
    """
    Obtém as dimensões da tela do usuário e calcula as coordenadas X e Y
    para posicionar a janela no centro exato da tela.
    """
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    pos_x = int((largura_tela / 2) - (largura / 2))
    pos_y = int((altura_tela / 2) - (altura / 2))
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def gerar_relatorio():
    periodo = combo_periodo.get()
    tipo = var_tipo_relatorio.get()
    
    if not periodo:
        lbl_status.config(text="Erro: Selecione um período de apuração válido!", fg="#ef4444")
        messagebox.showwarning("Seleção Incompleta", "Por favor, escolha um período para o relatório.")
        return

    # Simulação de valores consolidados com base na DRE
    txt_display.config(state="normal")
    txt_display.delete("1.0", tk.END)
    
    relatorio_txt = (
        f"==========================================================\n"
        f"   RELATÓRIO FINANCEIRO: {tipo.upper()}\n"
        f"   PERÍODO DE APURAÇÃO: {periodo.upper()}\n"
        f"==========================================================\n\n"
        f"   (+) Receita Bruta de Vendas:................. R$ 1.250.000,00\n"
        f"   (-) Impostos e Deduções Gerais:.............. R$   212.500,00\n"
        f"   --------------------------------------------------------\n"
        f"   (=) Receita Líquida Operacional:............. R$ 1.037.500,00\n"
        f"   (-) Custos dos Produtos/Serviços (CPV):...... R$   480.000,00\n"
        f"   --------------------------------------------------------\n"
        f"   (=) LUCRO BRUTO OPERACIONAL:................. R$   557.500,00\n"
        f"   (-) Despesas Operacionais / Pessoal:......... R$   185.000,00\n"
        f"   ========================================================\n"
        f"   (=) RESULTADO LÍQUIDO DO PERÍODO:............ R$   372.500,00\n"
        f"   ========================================================\n"
    )
    
    txt_display.insert(tk.END, relatorio_txt)
    txt_display.config(state="disabled")
    
    lbl_status.config(text=f"Relatório '{tipo}' ({periodo}) gerado com sucesso!", fg="#10b981")

def limpar_filtros():
    combo_periodo.set("")
    var_tipo_relatorio.set("DRE Resumida")
    txt_display.config(state="normal")
    txt_display.delete("1.0", tk.END)
    txt_display.config(state="disabled")
    lbl_status.config(text="Filtros reinicializados.", fg="#64748b")

def exportar_pdf():
    if not txt_display.get("1.0", tk.END).strip():
        messagebox.showwarning("Exportação", "Gere um relatório antes de tentar exportar.")
        return
    messagebox.showinfo("Exportar PDF", "Relatório gerado e exportado com sucesso para o diretório local (DRE_Financeira.pdf).")

def sobre_sistema():
    messagebox.showinfo("Sobre o Sistema", "Módulo de Relatórios Financeiros v2.4\nDesenvolvido para Controladoria e Gestão Executiva.")

def main():
    global combo_periodo, var_tipo_relatorio, txt_display, lbl_status

    root = tk.Tk()
    root.title("Relatórios Financeiros & DRE Executiva - Controladoria")
    
    # Configuração de dimensões e centralização (Center Screen)
    LARGURA = 580
    ALTURA = 480
    centralizar_janela(root, LARGURA, ALTURA)
    root.resizable(False, False)
    
    BG_COLOR = "#f8fafc"
    root.configure(bg=BG_COLOR)

    # -------------------------------------------------------------
    # BARRA DE MENUS
    # -------------------------------------------------------------
    barra_menu = tk.Menu(root)
    
    menu_arquivo = tk.Menu(barra_menu, tearoff=0)
    menu_arquivo.add_command(label="Exportar PDF", command=exportar_pdf)
    menu_arquivo.add_command(label="Limpar Filtros", command=limpar_filtros)
    menu_arquivo.add_separator()
    menu_arquivo.add_command(label="Sair", command=root.quit)
    barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

    menu_ajuda = tk.Menu(barra_menu, tearoff=0)
    menu_ajuda.add_command(label="Sobre o Sistema", command=sobre_sistema)
    barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

    root.config(menu=barra_menu)

    # -------------------------------------------------------------
    # CABEÇALHO INSTITUCIONAL
    # -------------------------------------------------------------
    lbl_titulo = tk.Label(
        root, 
        text="EMISSÃO DE RELATÓRIOS FINANCEIROS", 
        font=("Helvetica", 13, "bold"), 
        fg="#0f172a", 
        bg=BG_COLOR
    )
    lbl_titulo.pack(pady=(12, 2))

    lbl_subtitulo = tk.Label(
        root, 
        text="Demonstrativo do Resultado do Exercício e Balancetes", 
        font=("Helvetica", 9), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_subtitulo.pack(pady=(0, 10))

    # -------------------------------------------------------------
    # PAINEL DE FILTROS E PARÂMETROS
    # -------------------------------------------------------------
    frame_filtros = tk.LabelFrame(
        root, 
        text=" Parâmetros de Emissão ", 
        font=("Helvetica", 9, "bold"), 
        fg="#1e293b", 
        bg=BG_COLOR, 
        padx=10, 
        pady=8
    )
    frame_filtros.pack(fill="x", padx=20, pady=5)

    # Período
    tk.Label(frame_filtros, text="Período de Apuração:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=0, column=0, sticky="w", pady=4)
    periodos = ["Mês Atual", "1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre", "Anual Consolidado"]
    combo_periodo = ttk.Combobox(frame_filtros, values=periodos, font=("Helvetica", 9), width=25, state="readonly")
    combo_periodo.grid(row=0, column=1, pady=4, padx=10, sticky="w")

    # Tipo de Relatório
    tk.Label(frame_filtros, text="Tipo de Relatório:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=1, column=0, sticky="w", pady=4)
    
    frame_radio = tk.Frame(frame_filtros, bg=BG_COLOR)
    frame_radio.grid(row=1, column=1, pady=4, padx=10, sticky="w")

    var_tipo_relatorio = tk.StringVar(value="DRE Resumida")
    rb_dre = tk.Radiobutton(frame_radio, text="DRE Resumida", variable=var_tipo_relatorio, value="DRE Resumida", bg=BG_COLOR, activebackground=BG_COLOR)
    rb_fluxo = tk.Radiobutton(frame_radio, text="Fluxo de Caixa", variable=var_tipo_relatorio, value="Fluxo de Caixa", bg=BG_COLOR, activebackground=BG_COLOR)
    
    rb_dre.pack(side="left", padx=(0, 5))
    rb_fluxo.pack(side="left")

    # Botões de Ação dos Filtros
    frame_botoes = tk.Frame(frame_filtros, bg=BG_COLOR)
    frame_botoes.grid(row=2, column=0, columnspan=2, pady=8)

    btn_gerar = tk.Button(
        frame_botoes, 
        text="Gerar Relatório", 
        font=("Helvetica", 9, "bold"), 
        bg="#0284c7", 
        fg="white", 
        padx=12, 
        pady=3, 
        command=gerar_relatorio
    )
    btn_gerar.pack(side="left", padx=5)

    btn_limpar = tk.Button(
        frame_botoes, 
        text="Limpar Filtros", 
        font=("Helvetica", 9), 
        bg="#64748b", 
        fg="white", 
        padx=12, 
        pady=3, 
        command=limpar_filtros
    )
    btn_limpar.pack(side="left", padx=5)

    # -------------------------------------------------------------
    # DISPLAY DE EXIBIÇÃO DO RELATÓRIO
    # -------------------------------------------------------------
    frame_display = tk.Frame(root, bg=BG_COLOR)
    frame_display.pack(fill="both", expand=True, padx=20, pady=5)

    txt_display = tk.Text(
        frame_display, 
        font=("Courier", 8, "bold"), 
        bg="#0f172a", 
        fg="#38bdf8", 
        bd=1, 
        relief="solid", 
        wrap="none"
    )
    txt_display.pack(fill="both", expand=True)
    txt_display.config(state="disabled")

    # -------------------------------------------------------------
    # RÓTULO DE AUDITORIA / STATUS
    # -------------------------------------------------------------
    lbl_status = tk.Label(
        root, 
        text="Aguardando seleção de parâmetros...", 
        font=("Helvetica", 8, "italic"), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_status.pack(side="bottom", pady=8)

    root.mainloop()

if __name__ == "__main__":
    main()
