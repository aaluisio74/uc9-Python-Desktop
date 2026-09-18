import tkinter as tk
from tkinter import ttk

def centralizar_janela(janela, largura, altura):
    """
    Função responsável por obter a resolução da tela do usuário
    e calcular as coordenadas (X, Y) para posicionar a janela no centro.
    """
    # Obtém a largura e altura da tela do usuário
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    # Calcula a posição X e Y para centralizar
    pos_x = int((largura_tela / 2) - (largura / 2))
    pos_y = int((altura_tela / 2) - (altura / 2))
    
    # Define a geometria da janela: 'larguraxaltura+x+y'
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def criar_card(parent, titulo, valor, cor_valor, linha, coluna):
    """
    Função auxiliar para criar os cartões de KPIs/Métricas padronizados.
    """
    card = tk.Frame(parent, bg="#1e293b", bd=1, relief="solid", highlightbackground="#334155", highlightthickness=1)
    card.grid(row=linha, column=coluna, padx=12, pady=12, sticky="nsew")
    
    # Rótulo do Título da Métrica
    lbl_titulo = tk.Label(card, text=titulo, font=("Helvetica", 10), fg="#94a3b8", bg="#1e293b")
    lbl_titulo.pack(pady=(15, 5), padx=20)
    
    # Rótulo do Valor em Destaque
    lbl_valor = tk.Label(card, text=valor, font=("Helvetica", 18, "bold"), fg=cor_valor, bg="#1e293b")
    lbl_valor.pack(pady=(0, 15), padx=20)

def main():
    # Inicialização da Janela Principal
    root = tk.Tk()
    root.title("Dashboard Gerencial - Métricas & Desempenho Executivo")
    
    # Configuração de dimensões e centralização
    LARGURA = 600
    ALTURA = 420
    centralizar_janela(root, LARGURA, ALTURA)
    
    # Impede o redimensionamento da janela
    root.resizable(False, False)
    
    # Cor de Fundo Principal (Dark Slate)
    BG_COLOR = "#0f172a"
    root.configure(bg=BG_COLOR)
    
    # -------------------------------------------------------------
    # CABEÇALHO / TÍTULO
    # -------------------------------------------------------------
    lbl_cabecalho = tk.Label(
        root, 
        text="DASHBOARD GERENCIAL DE PERFORMANCE", 
        font=("Helvetica", 13, "bold"), 
        fg="#f8fafc", 
        bg=BG_COLOR
    )
    lbl_cabecalho.pack(pady=(20, 10))
    
    lbl_subtitulo = tk.Label(
        root,
        text="Visão Geral dos Indicadores Financeiros e Operacionais",
        font=("Helvetica", 9),
        fg="#64748b",
        bg=BG_COLOR
    )
    lbl_subtitulo.pack(pady=(0, 15))

    # -------------------------------------------------------------
    # ÁREA DE CARDS (KPIS)
    # -------------------------------------------------------------
    frame_kpis = tk.Frame(root, bg=BG_COLOR)
    frame_kpis.pack(padx=20, pady=10)
    
    # Configuração do grid de 2 linhas x 2 colunas
    frame_kpis.grid_columnconfigure(0, weight=1)
    frame_kpis.grid_columnconfigure(1, weight=1)
    
    # Criação dos Cartões de Métricas
    criar_card(frame_kpis, "Receita Mensal", "R$ 458.900", "#38bdf8", 0, 0)
    criar_card(frame_kpis, "Custo Operacional", "R$ 182.400", "#f87171", 0, 1)
    criar_card(frame_kpis, "Margem de Lucro", "60.2%", "#4ade80", 1, 0)
    criar_card(frame_kpis, "Novos Clientes", "+342", "#fbbf24", 1, 1)

    # -------------------------------------------------------------
    # RODAPÉ DE STATUS
    # -------------------------------------------------------------
    lbl_status = tk.Label(
        root, 
        text="Status do Sistema: Operacional  |  Última Sincronização: Há 1 min  |  v2.4", 
        font=("Helvetica", 8), 
        fg="#64748b", 
        bg=BG_COLOR
    )
    lbl_status.pack(side="bottom", pady=15)

    # Executa o loop principal da interface
    root.mainloop()

if __name__ == "__main__":
    main()
