import tkinter as tk
from tkinter import messagebox

# Variável global para armazenar o saldo acumulado
saldo_total = 0.0

def centralizar_janela(janela, largura, altura):
    """
    Obtém a resolução do monitor do usuário e calcula
    as coordenadas X e Y para exibir a janela exatamente no centro.
    """
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    pos_x = int((largura_tela / 2) - (largura / 2))
    pos_y = int((altura_tela / 2) - (altura / 2))
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def registrar_lancamento():
    global saldo_total
    
    descricao = entry_descricao.get().strip()
    valor_str = entry_valor.get().strip().replace(",", ".")
    tipo = var_tipo.get()
    
    # Validação de preenchimento da descrição
    if not descricao:
        lbl_status.config(text="Erro: Preencha a descrição do lançamento!", fg="#ef4444")
        messagebox.showwarning("Inconsistência", "Informe a descrição da operação.")
        return
        
    # Validação numérica do valor
    try:
        valor = float(valor_str)
        if valor <= 0:
            raise ValueError
    except ValueError:
        lbl_status.config(text="Erro: O valor deve ser um número positivo maior que zero!", fg="#ef4444")
        messagebox.showerror("Erro de Validação", "Insira um valor numérico válido maior que zero.")
        return

    # Atualização do Saldo com base no tipo de movimentação
    if tipo == "entrada":
        saldo_total += valor
        msg_sucesso = f"Receita registrada: {descricao} (+R$ {valor:,.2f})"
    else:
        saldo_total -= valor
        msg_sucesso = f"Despesa registrada: {descricao} (-R$ {valor:,.2f})"

    # Formatando e atualizando a exibição do saldo
    lbl_valor_saldo.config(text=f"R$ {saldo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Destaque de cor no saldo (Verde se positivo/zero, Vermelho se negativo)
    if saldo_total >= 0:
        lbl_valor_saldo.config(fg="#22c55e")
    else:
        lbl_valor_saldo.config(fg="#ef4444")

    # Feedback de auditoria e limpeza dos campos do formulário
    lbl_status.config(text=msg_sucesso, fg="#10b981")
    limpar_campos()

def limpar_campos():
    entry_descricao.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    var_tipo.set("entrada")
    entry_descricao.focus_set()

def main():
    global entry_descricao, entry_valor, var_tipo, lbl_valor_saldo, lbl_status

    root = tk.Tk()
    root.title("Controle Financeiro Empresarial - Fluxo de Caixa")
    
    # Dimensões e Centralização da Janela (Center Screen)
    LARGURA = 550
    ALTURA = 450
    centralizar_janela(root, LARGURA, ALTURA)
    root.resizable(False, False)
    
    # Estilização Global
    BG_COLOR = "#f8fafc"
    root.configure(bg=BG_COLOR)

    # -------------------------------------------------------------
    # CABEÇALHO INSTITUCIONAL
    # -------------------------------------------------------------
    lbl_titulo = tk.Label(
        root, 
        text="SISTEMA DE CONTROLE FINANCEIRO", 
        font=("Helvetica", 14, "bold"), 
        fg="#0f172a", 
        bg=BG_COLOR
    )
    lbl_titulo.pack(pady=(15, 2))

    lbl_subtitulo = tk.Label(
        root, 
        text="Lançamento de Fluxo de Caixa & Gestão Operacional", 
        font=("Helvetica", 9), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_subtitulo.pack(pady=(0, 10))

    # -------------------------------------------------------------
    # DISPLAY DE SALDO ATUAL
    # -------------------------------------------------------------
    frame_saldo = tk.Frame(root, bg="#1e293b", bd=1, relief="solid")
    frame_saldo.pack(fill="x", padx=30, pady=5)

    lbl_titulo_saldo = tk.Label(frame_saldo, text="SALDO OPERACIONAL ATUAL", font=("Helvetica", 9, "bold"), fg="#94a3b8", bg="#1e293b")
    lbl_titulo_saldo.pack(pady=(8, 0))

    lbl_valor_saldo = tk.Label(frame_saldo, text="R$ 0,00", font=("Helvetica", 18, "bold"), fg="#22c55e", bg="#1e293b")
    lbl_valor_saldo.pack(pady=(2, 8))

    # -------------------------------------------------------------
    # FORMULÁRIO DE ENTRADA
    # -------------------------------------------------------------
    frame_form = tk.LabelFrame(root, text=" Registrar Nova Movimentação ", font=("Helvetica", 10, "bold"), fg="#1e293b", bg=BG_COLOR, padx=15, pady=10)
    frame_form.pack(fill="x", padx=30, pady=10)

    # Descrição
    tk.Label(frame_form, text="Descrição da Operação:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=0, column=0, sticky="w", pady=5)
    entry_descricao = tk.Entry(frame_form, font=("Helvetica", 9), width=35)
    entry_descricao.grid(row=0, column=1, pady=5, padx=5)

    # Valor (R$)
    tk.Label(frame_form, text="Valor da Operação (R$):", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=1, column=0, sticky="w", pady=5)
    entry_valor = tk.Entry(frame_form, font=("Helvetica", 9), width=35)
    entry_valor.grid(row=1, column=1, pady=5, padx=5)

    # Tipo de Movimentação (Radiobuttons)
    tk.Label(frame_form, text="Tipo de Lançamento:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=2, column=0, sticky="w", pady=5)
    
    frame_radio = tk.Frame(frame_form, bg=BG_COLOR)
    frame_radio.grid(row=2, column=1, sticky="w", pady=5)

    var_tipo = tk.StringVar(value="entrada")
    rb_entrada = tk.Radiobutton(frame_radio, text="Entrada (Receita)", variable=var_tipo, value="entrada", bg=BG_COLOR, activebackground=BG_COLOR)
    rb_saida = tk.Radiobutton(frame_radio, text="Saída (Despesa)", variable=var_tipo, value="saida", bg=BG_COLOR, activebackground=BG_COLOR)
    
    rb_entrada.pack(side="left", padx=(0, 10))
    rb_saida.pack(side="left")

    # -------------------------------------------------------------
    # BOTOES DE AÇÃO
    # -------------------------------------------------------------
    frame_botoes = tk.Frame(root, bg=BG_COLOR)
    frame_botoes.pack(pady=10)

    btn_salvar = tk.Button(
        frame_botoes, 
        text="Registrar Operação", 
        font=("Helvetica", 9, "bold"), 
        bg="#2563eb", 
        fg="white", 
        padx=15, 
        pady=5, 
        command=registrar_lancamento
    )
    btn_salvar.pack(side="left", padx=10)

    btn_limpar = tk.Button(
        frame_botoes, 
        text="Limpar Campos", 
        font=("Helvetica", 9), 
        bg="#64748b", 
        fg="white", 
        padx=15, 
        pady=5, 
        command=limpar_campos
    )
    btn_limpar.pack(side="left", padx=10)

    # -------------------------------------------------------------
    # RÓTULO DE AUDITORIA / STATUS
    # -------------------------------------------------------------
    lbl_status = tk.Label(
        root, 
        text="Aguardando novo lançamento financeiro...", 
        font=("Helvetica", 8, "italic"), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_status.pack(side="bottom", pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()
