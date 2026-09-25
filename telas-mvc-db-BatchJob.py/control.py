from tkinter import messagebox
import sqlite3

class AppController:
    def __init__(self, model):
        self.model = model
        self.main_view = None
        self.janela_lotes = None

    def set_views(self, main_view):
        self.main_view = main_view

    def abrir_janela_lotes(self):
        self.main_view.withdraw()
        from view import JanelaPesquisaLotes
        self.janela_lotes = JanelaPesquisaLotes(self.main_view, self)
        self.atualizar_tabela_lotes()

    def fechar_janela_lotes(self):
        if self.janela_lotes:
            self.janela_lotes.destroy()
            self.janela_lotes = None
        self.main_view.deiconify()

    def salvar_lote(self):
        v = self.janela_lotes
        if not v.id_selecionado:
            messagebox.showwarning("Seleção Inválida", "Selecione um lote na tabela para editar.", parent=v)
            return

        try:
            volume = int(v.entry_volume.get().strip())
            ambiente = v.cb_ambiente.get().strip()
            tipo = v.cb_tipo.get().strip()

            if volume <= 0 or not ambiente or not tipo:
                messagebox.showwarning("Inconsistência de Dados", "Preencha todos os campos corretamente.", parent=v)
                return

            v.withdraw()
            try:
                self.model.atualizar_lote(v.id_selecionado, volume, ambiente, tipo)
                self.atualizar_tabela_lotes()
                v.limpar_campos()
                v.lbl_audit.config(text="[REGISTRO DE LOTE ATUALIZADO COM SUCESSO]", fg="#15803d")
            finally:
                v.deiconify()
        except ValueError:
            messagebox.showerror("Erro de Formato", "O volume deve ser um número inteiro válido.", parent=v)

    def excluir_lote(self):
        v = self.janela_lotes
        if not v.id_selecionado:
            messagebox.showwarning("Seleção Inválida", "Selecione um registro na tabela para excluir.", parent=v)
            return

        if messagebox.askyesno("Confirmar Exclusão", "Deseja remover o lote selecionado?", parent=v):
            v.withdraw()
            try:
                self.model.deletar_lote(v.id_selecionado)
                self.atualizar_tabela_lotes()
                v.limpar_campos()
                v.lbl_audit.config(text="[LOTE EXCLUÍDO COM SUCESSO]", fg="#dc2626")
            finally:
                v.deiconify()

    def filtrar_lotes(self):
        termo = self.janela_lotes.entry_busca.get().strip()
        self.atualizar_tabela_lotes(termo)

    def atualizar_tabela_lotes(self, termo=""):
        registros = self.model.buscar_lotes(termo)
        for item in self.janela_lotes.tree.get_children():
            self.janela_lotes.tree.delete(item)
        for reg in registros:
            self.janela_lotes.tree.insert("", "end", values=reg)

    def executar_processamento(self):
        try:
            volume = int(self.main_view.entry_lote.get())
            ambiente = self.main_view.var_ambiente.get()
            tipo = self.main_view.var_tipo.get()

            if volume <= 0:
                messagebox.showerror("Erro de Parâmetro", "O tamanho do lote deve ser maior que zero.", parent=self.main_view)
                return

            self.main_view.withdraw()
            try:
                self.model.registrar_lote(volume, ambiente, tipo)
            finally:
                self.main_view.deiconify()

            if ambiente == "PROD":
                alerta = f"Lote {tipo} de {volume} registros enviado para PRODUÇÃO!"
                cor = "#b91c1c"
            else:
                alerta = f"Lote {tipo} de {volume} registros processado em HOMOLOGAÇÃO."
                cor = "#0369a1"

            self.main_view.lbl_status.config(
                text=f"[STATUS 200 OK]\n{alerta}",
                fg=cor
            )
        except ValueError:
            messagebox.showerror("Erro de Formato", "Informe um número inteiro válido para o tamanho do lote.", parent=self.main_view)

    def exibir_sobre(self):
        messagebox.showinfo(
            "Sobre o Kernel de Processamento",
            "Central de Lotes Corporativos v4.2\n\n"
            "Motor de Processamento de Alto Desempenho\n"
            "Ambiente Corporativo - Direitos Reservados",
            parent=self.main_view
        )

    def encerrar_sessao(self):
        if messagebox.askyesno("Confirmar Saída", "Deseja encerrar a sessão na Central de Lotes?", parent=self.main_view):
            self.main_view.destroy()