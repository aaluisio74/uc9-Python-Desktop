import tkinter as tk
from tkinter import messagebox


def exibir_sobre():
    messagebox.showinfo(
        "Sobre o Kernel de Processamento",
        "Central de Lotes Corporativos v4.2\n\n"
        "Motor de Processamento de Alto Desempenho\n"
        "Ambiente Corporativo - Direitos Reservados"
    )


def encerrar_sessao():
    if messagebox.askyesno(
        "Confirmar Saída",
        "Deseja encerrar a sessão no Central de Lotes?"
    ):
        janela.quit()


def resetar_lote():
    entry_lote.delete(0, tk.END)
    var_ambiente.set("HOMOLOG")
    var_tipo.set("FINANCEIRO")
    lbl_status.config(text="")


def executar_processamento():
    try:
        volume = int(entry_lote.get())
        ambiente = var_ambiente.get()
        tipo = var_tipo.get()

        if volume <= 0:
            messagebox.showerror(
                "Erro de Parâmetro",
                "O tamanho do lote deve ser maior que zero."
            )
            return

        # Simulação de disparo de lote
        if ambiente == "PROD":
            alerta = (
                f"Lote {tipo} de {volume} registros "
                "enviado para PRODUÇÃO!"
            )
            cor = "#b91c1c"
        else:
            alerta = (
                f"Lote {tipo} de {volume} registros "
                "processado em HOMOLOGAÇÃO."
            )
            cor = "#0369a1"

        lbl_status.config(
            text=f"[STATUS 200 OK]\n{alerta}",
            fg=cor
        )

    except ValueError:
        messagebox.showerror(
            "Erro de Formato",
            "Informe um número inteiro válido para o tamanho do lote."
        )


# ============================================================
# JANELA PRINCIPAL
# ============================================================

janela = tk.Tk()
janela.title(
    "Central de Processamento de Lotes e Notificações (Batch Jobs)"
)
janela.geometry("540x460")
janela.configure(bg="#f8fafc")


# ============================================================
# MENU DA APLICAÇÃO
# ============================================================

menubar = tk.Menu(janela)
janela.config(menu=menubar)

# Menu Operações
menu_ops = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(
    label="Operações",
    menu=menu_ops
)

menu_ops.add_command(
    label="Limpar Filtros",
    command=resetar_lote
)

menu_ops.add_separator()

menu_ops.add_command(
    label="Sair da Central",
    command=encerrar_sessao
)


# Menu Ajuda
menu_ajuda = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(
    label="Ajuda",
    menu=menu_ajuda
)

menu_ajuda.add_command(
    label="Sobre o Kernel",
    command=exibir_sobre
)


# ============================================================
# TÍTULO
# ============================================================

lbl_titulo = tk.Label(
    janela,
    text="CENTRAL DE PROCESSAMENTO DE LOTES (BATCH)",
    font=("Segoe UI", 12, "bold"),
    bg="#f8fafc",
    fg="#0f172a"
)

lbl_titulo.pack(pady=15)


# ============================================================
# FRAME DE PARÂMETROS
# ============================================================

frame_params = tk.Frame(
    janela,
    bg="#f8fafc"
)

frame_params.pack(pady=10)


# Tamanho do lote
tk.Label(
    frame_params,
    text="Tamanho do Lote (Registros):",
    font=("Segoe UI", 10),
    bg="#f8fafc"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)

entry_lote = tk.Entry(
    frame_params,
    width=15,
    font=("Segoe UI", 10)
)

entry_lote.grid(
    row=0,
    column=1,
    padx=10,
    pady=5
)


# ============================================================
# OPÇÕES / RADIOBUTTONS
# ============================================================

frame_opcoes = tk.Frame(
    frame_params,
    bg="#f8fafc"
)

frame_opcoes.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=15
)


var_ambiente = tk.StringVar(
    value="HOMOLOG"
)

var_tipo = tk.StringVar(
    value="FINANCEIRO"
)


# ============================================================
# GRUPO: AMBIENTE
# ============================================================

grp_ambiente = tk.LabelFrame(
    frame_opcoes,
    text="Ambiente de Execução",
    font=("Segoe UI", 9, "bold"),
    bg="#f8fafc"
)

grp_ambiente.grid(
    row=0,
    column=0,
    padx=15
)


tk.Radiobutton(
    grp_ambiente,
    text="Homologação (Staging)",
    variable=var_ambiente,
    value="HOMOLOG",
    bg="#f8fafc"
).pack(
    anchor="w",
    padx=8,
    pady=3
)


tk.Radiobutton(
    grp_ambiente,
    text="Produção (Live)",
    variable=var_ambiente,
    value="PROD",
    bg="#f8fafc"
).pack(
    anchor="w",
    padx=8,
    pady=3
)


# ============================================================
# GRUPO: TIPO DE LOTE
# ============================================================

grp_tipo = tk.LabelFrame(
    frame_opcoes,
    text="Tipo de Carga",
    font=("Segoe UI", 9, "bold"),
    bg="#f8fafc"
)

grp_tipo.grid(
    row=0,
    column=1,
    padx=15
)


tk.Radiobutton(
    grp_tipo,
    text="Lote Financeiro",
    variable=var_tipo,
    value="FINANCEIRO",
    bg="#f8fafc"
).pack(
    anchor="w",
    padx=8,
    pady=3
)


tk.Radiobutton(
    grp_tipo,
    text="Disparo de Notificações",
    variable=var_tipo,
    value="NOTIFICACOES",
    bg="#f8fafc"
).pack(
    anchor="w",
    padx=8,
    pady=3
)


# ============================================================
# BOTÕES DE AÇÃO
# ============================================================

frame_acao = tk.Frame(
    janela,
    bg="#f8fafc"
)

frame_acao.pack(pady=15)


btn_exec = tk.Button(
    frame_acao,
    text="Iniciar Processamento",
    command=executar_processamento,
    bg="#0284c7",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=20
)

btn_exec.grid(
    row=0,
    column=0,
    padx=5
)


btn_reset = tk.Button(
    frame_acao,
    text="Resetar Lote",
    command=resetar_lote,
    bg="#64748b",
    fg="white",
    font=("Segoe UI", 10),
    width=14
)

btn_reset.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# DISPLAY DE STATUS
# ============================================================

lbl_status = tk.Label(
    janela,
    text="",
    font=("Segoe UI", 10, "bold"),
    bg="#f8fafc"
)

lbl_status.pack(
    pady=15
)


# =============================================================
# INICIALIZAÇÃO
# =============================================================

janela.mainloop()
