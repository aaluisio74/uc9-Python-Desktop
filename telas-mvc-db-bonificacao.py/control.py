from tkinter import messagebox
from model import BonificacaoModel
from view import MainView, Atividade2Window, BonificacaoCRUDWindow

class AppController:
    def __init__(self):
        self.model = BonificacaoModel()
        self.main_view = MainView(self)
        self.active_window = None
        self.crud_view = None

    def executar(self):
        self.main_view.mainloop()

    def ocultar_janela_principal(self):
        """Oculta a janela principal quando houver operação/janela modal ativa."""
        self.main_view.withdraw()

    def exibir_janela_principal(self):
        """Reexibe a janela principal ao fechar a tela secundária."""
        self.main_view.deiconify()

    def abrir_atividade2(self):
        self.ocultar_janela_principal()
        self.active_window = Atividade2Window(self.main_view, on_close=self.exibir_janela_principal)

    def abrir_atividade3_crud(self):
        self.ocultar_janela_principal()
        self.crud_view = BonificacaoCRUDWindow(self.main_view, self, on_close=self.exibir_janela_principal)
        self.carregar_dados()

    def carregar_dados(self):
        registros = self.model.listar_registros()
        self.atualizar_tabela_view(registros)

    def filtrar(self):
        filtro = self.crud_view.ent_filtro.get().strip()
        registros = self.model.listar_registros(filtro_nome=filtro)
        self.atualizar_tabela_view(registros)

    def atualizar_tabela_view(self, registros):
        for item in self.crud_view.tree.get_children():
            self.crud_view.tree.delete(item)
        
        for reg in registros:
            # Formatando valores no padrão brasileiro
            salario_fmt = f"{reg[2]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            bonus_fmt = f"{reg[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.crud_view.tree.insert("", "end", values=(reg[0], reg[1], salario_fmt, f"{reg[3]:.1f}", bonus_fmt, reg[5]))

    def validar_e_calcular(self):
        nome = self.crud_view.ent_nome.get().strip()
        try:
            salario = float(self.crud_view.ent_salario.get().replace(",", "."))
            meta = float(self.crud_view.ent_meta.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro de Formato", "Informe valores numéricos válidos para Salário e Metas.")
            return None

        if salario <= 0 or meta < 0:
            messagebox.showerror("Erro de Validação", "O salário deve ser > 0 e a meta não pode ser negativa.")
            return None

        fator, categoria, _ = self.model.calcular_fator_e_categoria(meta)
        bonus = salario * fator

        # ATUALIZAÇÃO DA VIEW: Exibe o bônus calculado na interface
        if hasattr(self.crud_view, 'ent_bonus'):
            self.crud_view.ent_bonus.config(state="normal")
            self.crud_view.ent_bonus.delete(0, "end")
            self.crud_view.ent_bonus.insert(0, f"{bonus:.2f}")
            self.crud_view.ent_bonus.config(state="readonly")

        return nome, salario, meta, bonus, categoria

    def salvar(self):
        dados = self.validar_e_calcular()
        if dados:
            self.model.inserir_registro(*dados)
            messagebox.showinfo("Sucesso", "Cálculo e registro salvos no SQLite com sucesso!")
            self.crud_view.limpar_campos()
            self.carregar_dados()

    def atualizar(self):
        if not self.crud_view.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para atualizar.")
            return
        
        dados = self.validar_e_calcular()
        if dados:
            self.model.atualizar_registro(self.crud_view.id_selecionado, *dados)
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
            self.crud_view.limpar_campos()
            self.carregar_dados()

    def excluir(self):
        if not self.crud_view.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para excluir.")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", "Deseja realmente remover este registro do SQLite?"):
            self.model.excluir_registro(self.crud_view.id_selecionado)
            messagebox.showinfo("Sucesso", "Registro removido do banco de dados!")
            self.crud_view.limpar_campos()
            self.carregar_dados()
