import tkinter as tk
from tkinter import ttk, messagebox

def centralizar_janela(janela, largura, altura):
    """
    Calcula as coordenadas X e Y com base na resolução da tela do usuário
    para abrir a janela perfeitamente centralizada.
    """
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    pos_x = int((largura_tela / 2) - (largura / 2))
    pos_y = int((altura_tela / 2) - (altura / 2))
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def salvar_colaborador():
    matricula = entry_matricula.get().strip()
    nome = entry_nome.get().strip()
    cargo = entry_cargo.get().strip()
    departamento = combo_departamento.get().strip()
    modalidade = var_modalidade.get()

    # Validação de campos obrigatórios
    if not matricula or not nome or not cargo or not departamento:
        lbl_status.config(
            text="Erro: Todos os campos cadastrais são de preenchimento obrigatório!", 
            fg="#ef4444"
        )
        messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos do formulário.")
        return

    # Confirmação do cadastro
    resposta = messagebox.askyesno(
        "Confirmar Cadastro", 
        f"Deseja confirmar o cadastro do colaborador abaixo?\n\n"
        f"Matrícula: {matricula}\n"
        f"Nome: {nome}\n"
        f"Cargo: {cargo}\n"
        f"Departamento: {departamento}\n"
        f"Modalidade: {modalidade}"
    )

    if resposta:
        lbl_status.config(
            text=f"Sucesso: Colaborador '{nome}' ({matricula}) cadastrado com sucesso!", 
            fg="#10b981"
        )
        messagebox.showinfo("Sucesso", "Registro salvo com sucesso no banco de dados!")
        limpar_formulario(confirmar=False)

def limpar_formulario(confirmar=True):
    if confirmar:
        resposta = messagebox.askyesno("Confirmar Limpeza", "Tem certeza que deseja limpar todos os campos?")
        if not resposta:
            return

    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_cargo.delete(0, tk.END)
    combo_departamento.set("")
    var_modalidade.set("Presencial")
    
    if confirmar:
        lbl_status.config(text="Formulário reinicializado.", fg="#64748b")
    
    entry_matricula.focus_set()

def main():
    global entry_matricula, entry_nome, entry_cargo, combo_departamento, var_modalidade, lbl_status

    root = tk.Tk()
    root.title("HRMS - Sistema de Gestão de Colaboradores e Quadro Funcional")
    
    # Dimensões e Centralização da Janela
    LARGURA = 580
    ALTURA = 460
    centralizar_janela(root, LARGURA, ALTURA)
    root.resizable(False, False)

    # Cor de Fundo Corporativa (Tema Slate Claro)
    BG_COLOR = "#f8fafc"
    root.configure(bg=BG_COLOR)

    # -------------------------------------------------------------
    # CABEÇALHO INSTITUCIONAL
    # -------------------------------------------------------------
    lbl_titulo = tk.Label(
        root, 
        text="CADASTRO DE COLABORADOR CORPORATIVO", 
        font=("Helvetica", 13, "bold"), 
        fg="#0f172a", 
        bg=BG_COLOR
    )
    lbl_titulo.pack(pady=(15, 2))

    lbl_subtitulo = tk.Label(
        root, 
        text="Módulo de Recursos Humanos e Perfis Ocupacionais (HRMS)", 
        font=("Helvetica", 9), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_subtitulo.pack(pady=(0, 15))

    # -------------------------------------------------------------
    # FORMULÁRIO DE DADOS FUNCIONAIS
    # -------------------------------------------------------------
    frame_form = tk.LabelFrame(
        root, 
        text=" Dados Pessoais & Funcionais ", 
        font=("Helvetica", 10, "bold"), 
        fg="#1e293b", 
        bg=BG_COLOR, 
        padx=15, 
        pady=10
    )
    frame_form.pack(fill="x", padx=25, pady=5)

    # Matrícula
    tk.Label(frame_form, text="Matrícula:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=0, column=0, sticky="w", pady=6)
    entry_matricula = tk.Entry(frame_form, font=("Helvetica", 9), width=35)
    entry_matricula.grid(row=0, column=1, pady=6, padx=10)

    # Nome Completo
    tk.Label(frame_form, text="Nome Completo:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=1, column=0, sticky="w", pady=6)
    entry_nome = tk.Entry(frame_form, font=("Helvetica", 9), width=35)
    entry_nome.grid(row=1, column=1, pady=6, padx=10)

    # Cargo / Função
    tk.Label(frame_form, text="Cargo / Função:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=2, column=0, sticky="w", pady=6)
    entry_cargo = tk.Entry(frame_form, font=("Helvetica", 9), width=35)
    entry_cargo.grid(row=2, column=1, pady=6, padx=10)

    # Departamento (Combobox)
    tk.Label(frame_form, text="Departamento:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=3, column=0, sticky="w", pady=6)
    
    departamentos = [
        "TI & Sistemas", 
        "Recursos Humanos", 
        "Operações & Logística", 
        "Financeiro & Controladoria", 
        "Marketing & Comercial"
    ]
    combo_departamento = ttk.Combobox(frame_form, values=departamentos, font=("Helvetica", 9), width=33, state="readonly")
    combo_departamento.grid(row=3, column=1, pady=6, padx=10)

    # Modalidade de Trabalho (Radiobutton)
    tk.Label(frame_form, text="Modalidade:", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#334155").grid(row=4, column=0, sticky="w", pady=6)
    
    frame_modalidade = tk.Frame(frame_form, bg=BG_COLOR)
    frame_modalidade.grid(row=4, column=1, sticky="w", pady=6, padx=10)

    var_modalidade = tk.StringVar(value="Presencial")
    rb_presencial = tk.Radiobutton(frame_modalidade, text="Presencial", variable=var_modalidade, value="Presencial", bg=BG_COLOR, activebackground=BG_COLOR)
    rb_hibrido = tk.Radiobutton(frame_modalidade, text="Híbrido", variable=var_modalidade, value="Híbrido", bg=BG_COLOR, activebackground=BG_COLOR)
    rb_remoto = tk.Radiobutton(frame_modalidade, text="Remoto", variable=var_modalidade, value="Remoto", bg=BG_COLOR, activebackground=BG_COLOR)

    rb_presencial.pack(side="left", padx=(0, 5))
    rb_hibrido.pack(side="left", padx=5)
    rb_remoto.pack(side="left", padx=5)

    # -------------------------------------------------------------
    # BOTÕES DE AÇÃO
    # -------------------------------------------------------------
    frame_botoes = tk.Frame(root, bg=BG_COLOR)
    frame_botoes.pack(pady=15)

    btn_salvar = tk.Button(
        frame_botoes, 
        text="Salvar Colaborador", 
        font=("Helvetica", 9, "bold"), 
        bg="#1e40af", 
        fg="white", 
        padx=15, 
        pady=6, 
        command=salvar_colaborador
    )
    btn_salvar.pack(side="left", padx=10)

    btn_limpar = tk.Button(
        frame_botoes, 
        text="Limpar Formulário", 
        font=("Helvetica", 9), 
        bg="#475569", 
        fg="white", 
        padx=15, 
        pady=6, 
        command=lambda: limpar_formulario(confirmar=True)
    )
    btn_limpar.pack(side="left", padx=10)

    # -------------------------------------------------------------
    # RÓTULO DE AUDITORIA / STATUS
    # -------------------------------------------------------------
    lbl_status = tk.Label(
        root, 
        text="Aguardando inserção de dados do colaborador...", 
        font=("Helvetica", 8, "italic"), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_status.pack(side="bottom", pady=12)

    root.mainloop()

if __name__ == "__main__":
    main()
