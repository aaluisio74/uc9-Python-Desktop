import tkinter as tk

# Inicialização da janela principal
janela = tk.Tk()
janela.title("Painel de Controle - Gestão de Ativos Corporativos (EAM)")
janela.geometry("500x350")
janela.configure(bg="#0f172a")  # Dark Slate Corporativo
janela.resizable(False, False)

# Centralização da janela
largura_j, altura_j = 500, 350
largura_s = janela.winfo_screenwidth()
altura_s = janela.winfo_screenheight()
pos_x = (largura_s - largura_j) // 2
pos_y = (altura_s - altura_j) // 2
janela.geometry(f"{largura_j}x{altura_j}+{pos_x}+{pos_y}")

# Cabeçalho do Dashboard
header = tk.Frame(janela, bg="#1e293b", height=60)
header.pack(fill="x", side="top")

lbl_titulo = tk.Label(
    header,
    text="SISTEMA DE GESTÃO DE ATIVOS & EQUIPAMENTOS",
    font=("Segoe UI", 12, "bold"),
    fg="#f8fafc",
    bg="#1e293b"
)
lbl_titulo.pack(pady=15)

# Container de Métricas (KPIs)
frame_kpi = tk.Frame(janela, bg="#0f172a")
frame_kpi.pack(expand=True, fill="both", padx=30, pady=20)

# Cartões de Métricas
def criar_kpi(parent, titulo, valor, cor_valor, row, col):
    card = tk.Frame(parent, bg="#1e293b", bd=1, relief="solid")
    card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    tk.Label(card, text=titulo, font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(pady=(10, 2))
    tk.Label(card, text=valor, font=("Segoe UI", 16, "bold"), fg=cor_valor, bg="#1e293b").pack(pady=(0, 10))

frame_kpi.grid_columnconfigure(0, weight=1)
frame_kpi.grid_columnconfigure(1, weight=1)

criar_kpi(frame_kpi, "Total de Ativos", "1,248", "#38bdf8", 0, 0)
criar_kpi(frame_kpi, "Em Operação", "1,180", "#4ade80", 0, 1)
criar_kpi(frame_kpi, "Em Manutenção", "54", "#fbbf24", 1, 0)
criar_kpi(frame_kpi, "Falhas Críticas", "14", "#f87171", 1, 1)

# Rodapé de Status do Sistema
footer = tk.Label(
    janela,
    text="Status do Sistema: Operacional | Úm. Sincronização: Há 2 min",
    font=("Segoe UI", 8),
    fg="#64748b",
    bg="#0f172a"
)
footer.pack(side="bottom", pady=10)

janela.mainloop()
