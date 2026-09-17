import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class AppFilaPedidos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Supply Chain - Fila de Processamento de Pedidos")
        self.geometry("620x450")

        self.pedidos_pendentes = [f"ORD-2026-{i:03d}" for i in range(1, 11)]
        self.total_pedidos = len(self.pedidos_pendentes)
        self.processados = 0

        # Título
        self.lbl_title = ctk.CTkLabel(
            self, text="ESTEIRA DE PROCESSAMENTO DE PEDIDOS PENDENTES", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.lbl_title.pack(pady=15)

        # Container de Progresso
        self.frame_progresso = ctk.CTkFrame(self)
        self.frame_progresso.pack(fill="x", padx=25, pady=10)

        self.lbl_status_progresso = ctk.CTkLabel(
            self.frame_progresso, text="Progresso do Lote: 0%", font=ctk.CTkFont(weight="bold")
        )
        self.lbl_status_progresso.pack(pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(self.frame_progresso, width=500)
        self.progress_bar.set(0.0)
        self.progress_bar.pack(pady=(0, 15))

        # Botões de Ação
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10)

        self.btn_processar = ctk.CTkButton(
            self.frame_botoes, text="Faturar Próximo Pedido", command=self.processar_proximo
        )
        self.btn_processar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_reset = ctk.CTkButton(
            self.frame_botoes, text="Reiniciar Esteira", fg_color="#64748b", command=self.reiniciar_esteira
        )
        self.btn_reset.grid(row=0, column=1, padx=10, pady=10)

        # Log Textbox
        self.lbl_log = ctk.CTkLabel(self, text="Console de Auditoria da Esteira:")
        self.lbl_log.pack(anchor="w", padx=25, pady=(10, 2))

        self.txt_log = ctk.CTkTextbox(self, width=560, height=150)
        self.txt_log.pack(padx=25, pady=(0, 15))
        self.txt_log.insert("0.0", "[SISTEMA] Esteira inicializada. 10 pedidos aguardando faturamento.")

    def processar_proximo(self):
        if self.processados < self.total_pedidos:
            pedido = self.pedidos_pendentes[self.processados]
            self.processados += 1
            porcentagem = self.processados / self.total_pedidos
            
            self.progress_bar.set(porcentagem)
            self.lbl_status_progresso.configure(text=f"Progresso do Lote: {int(porcentagem * 100)}%")
            
            self.txt_log.insert("end", f"[OK] Pedido {pedido} faturado e enviado para expedição.")
            self.txt_log.see("end")
        else:
            self.txt_log.insert("end", "[ALERTA] Todos os pedidos da esteira foram processados!")
            self.txt_log.see("end")

    def reiniciar_esteira(self):
        self.processados = 0
        self.progress_bar.set(0.0)
        self.lbl_status_progresso.configure(text="Progresso do Lote: 0%")
        self.txt_log.delete("1.0", "end")
        self.txt_log.insert("0.0", "[SISTEMA] Fila reiniciada com sucesso.")

if __name__ == "__main__":
    app = AppFilaPedidos()
    app.mainloop()
