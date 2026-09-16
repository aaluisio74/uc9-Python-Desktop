import tkinter as tk
from tkinter import messagebox


def calcular_bonificacao():
    try:
        colaborador = entry_nome.get().strip()
        salario = float(entry_salario.get())
        meta = float(entry_meta.get())

        if salario <= 0 or meta < 0:
            messagebox.showerror(
                "Erro de Validação",
                "O Salário deve ser maior que zero e o percentual de metas não pode ser negativo."
            )
            return

        # Escala Corporativa de Bonificação
        if meta < 80:
            fator = 0.0
            classificacao = "Meta Não Atingida (Sem Bônus)"
            cor = "#dc2626"

        elif meta < 100:
            fator = 0.5
            classificacao = "Atingimento Parcial (Bônus 50%)"
            cor = "#d97706"

        elif meta <= 120:
            fator = 1.0
            classificacao = "Meta Integral Atingida (Bônus 100%)"
            cor = "#16a34a"

        elif meta <= 150:
            fator = 1.5
            classificacao = "Superação de Metas (Bônus 150%)"
            cor = "#2563eb"

        else:
            fator = 2.0
            classificacao = "Performance Excepcional Executiva (Bônus 200%)"
            cor = "#7c3aed"

        bonificacao = salario * fator

        # Formatação do resultado
        valor_formatado = (
            f"R$ {bonificacao:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        nome_txt = (
            f"Colaborador: {colaborador}\n"
            if colaborador
            else ""
        )

        lbl_resultado.config(
            text=f"{nome_txt}Valor da Bonificação: {valor_formatado}"
        )

        lbl_classificacao.config(
            text=f"Categoria: {classificacao}",
            fg=cor
        )

    except ValueError:
        messagebox.showerror(
            "Erro de Formato",
            "Informe valores numéricos válidos para Salário e Atingimento de Metas."
        )


def resetar():
    entry_nome.delete(0, tk.END)
    entry_salario.delete(0, tk.END)
    entry_meta.delete(0, tk.END)

    lbl_resultado.config(text="")
    lbl_classificacao.config(text="")


# Janela principal
janela = tk.Tk()
janela.title("Calculadora de Participação nos Lucros & Bonificações (PLR)")
janela.geometry("520x450")
janela.configure(bg="#f1f5f9")


# Título da aplicação
lbl_header = tk.Label(
    janela,
    text="CÁLCULO DE BONIFICAÇÃO CORPORATIVA",
    font=("Segoe UI", 12, "bold"),
    bg="#f1f5f9",
    fg="#0f172a"
)
lbl_header.pack(pady=15)


# Frame de parâmetros
frame_inputs = tk.Frame(
    janela,
    bg="#f1f5f9"
)
frame_inputs.pack(pady=10)


tk.Label(
    frame_inputs,
    text="Colaborador / Gestor:",
    font=("Segoe UI", 10),
    bg="#f1f5f9"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=6,
    sticky="e"
)

entry_nome = tk.Entry(
    frame_inputs,
    width=28,
    font=("Segoe UI", 10)
)
entry_nome.grid(
    row=0,
    column=1,
    padx=10,
    pady=6
)


tk.Label(
    frame_inputs,
    text="Salário Base (R$):",
    font=("Segoe UI", 10),
    bg="#f1f5f9"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=6,
    sticky="e"
)

entry_salario = tk.Entry(
    frame_inputs,
    width=28,
    font=("Segoe UI", 10)
)
entry_salario.grid(
    row=1,
    column=1,
    padx=10,
    pady=6
)


tk.Label(
    frame_inputs,
    text="Atingimento de Metas (%):",
    font=("Segoe UI", 10),
    bg="#f1f5f9"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=6,
    sticky="e"
)

entry_meta = tk.Entry(
    frame_inputs,
    width=28,
    font=("Segoe UI", 10)
)
entry_meta.grid(
    row=2,
    column=1,
    padx=10,
    pady=6
)


# Botões de processamento
frame_botoes = tk.Frame(
    janela,
    bg="#f1f5f9"
)
frame_botoes.pack(pady=15)


btn_calc = tk.Button(
    frame_botoes,
    text="Calcular Bônus",
    command=calcular_bonificacao,
    bg="#059669",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=14
)
btn_calc.grid(
    row=0,
    column=0,
    padx=8
)


btn_limp = tk.Button(
    frame_botoes,
    text="Limpar Campos",
    command=resetar,
    bg="#475569",
    fg="white",
    font=("Segoe UI", 10),
    width=14
)
btn_limp.grid(
    row=0,
    column=1,
    padx=8
)


# Quadro de exibição dos resultados.
lbl_resultado = tk.Label(
    janela,
    text="",
    font=("Segoe UI", 11, "bold"),
    bg="#f1f5f9",
    fg="#0f172a"
)
lbl_resultado.pack(pady=5)


lbl_classificacao = tk.Label(
    janela,
    text="",
    font=("Segoe UI", 10, "bold"),
    bg="#f1f5f9"
)
lbl_classificacao.pack()


janela.mainloop()
