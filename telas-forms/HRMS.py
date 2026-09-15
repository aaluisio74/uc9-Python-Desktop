import tkinter as tk
from tkinter import messagebox

def registrar_colaborador():
    matricula = entry_matricula.get().strip()
    nome = entry_nome.get().strip()
    cargo = entry_cargo.get().strip()
    
    if matricula and nome and cargo:
        lbl_audit.config(
            text=f"[REGISTRO COM SUCESSO] Matrícula: {matricula} | {nome} ({cargo})",
            fg="#15803d"
        )
    else:
        messagebox.showwarning("Inconsistência de Dados", "Todos os campos corporativos são obrigatórios.")

def limpar_formulario():
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_cargo.delete(0, tk.END)
    lbl_audit.config(text="")

janela = tk.Tk()
janela.title("HRMS - Gestão de Colaboradores e Quadro Funcional")
janela.geometry("480x360")
janela.configure(bg="#f8fafc")

# Cabeçalho
header = tk.Label(
    janela,
    text="Cadastro de Colaborador Corporativo",
    font=("Segoe UI", 13, "bold"),
    fg="#0f172a",
    bg="#f8fafc"
)
header.pack(pady=(15, 5))

# Formulário
frame_form = tk.Frame(janela, bg="#f8fafc")
frame_form.pack(pady=10, padx=20)

# Matrícula
tk.Label(frame_form, text="Matrícula:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").grid(row=0, column=0, padx=5, pady=8, sticky="e")
entry_matricula = tk.Entry(frame_form, width=32, font=("Segoe UI", 9), relief="solid", bd=1)
entry_matricula.grid(row=0, column=1, padx=5, pady=8)

# Nome Completo
tk.Label(frame_form, text="Nome Completo:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").grid(row=1, column=0, padx=5, pady=8, sticky="e")
entry_nome = tk.Entry(frame_form, width=32, font=("Segoe UI", 9), relief="solid", bd=1)
entry_nome.grid(row=1, column=1, padx=5, pady=8)

# Cargo / Função
tk.Label(frame_form, text="Cargo / Função:", font=("Segoe UI", 9, "bold"), bg="#f8fafc", fg="#334155").grid(row=2, column=0, padx=5, pady=8, sticky="e")
entry_cargo = tk.Entry(frame_form, width=32, font=("Segoe UI", 9), relief="solid", bd=1)
entry_cargo.grid(row=2, column=1, padx=5, pady=8)

# Botões de Ação
frame_botoes = tk.Frame(janela, bg="#f8fafc")
frame_botoes.pack(pady=15)

btn_salvar = tk.Button(
    frame_botoes,
    text="Salvar Colaborador",
    command=registrar_colaborador,
    bg="#2563eb",
    fg="white",
    font=("Segoe UI", 9, "bold"),
    padx=10, pady=3, bd=0
)
btn_salvar.grid(row=0, column=0, padx=8)

btn_limpar = tk.Button(
    frame_botoes,
    text="Limpar Formulário",
    command=limpar_formulario,
    bg="#64748b",
    fg="white",
    font=("Segoe UI", 9),
    padx=10, pady=3, bd=0
)
btn_limpar.grid(row=0, column=1, padx=8)

# Feedback de Auditoria
lbl_audit = tk.Label(janela, text="", font=("Segoe UI", 8, "italic"), bg="#f8fafc")
lbl_audit.pack(pady=10)

janela.mainloop()
