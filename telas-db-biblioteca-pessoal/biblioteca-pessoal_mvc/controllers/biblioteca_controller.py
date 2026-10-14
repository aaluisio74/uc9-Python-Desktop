import sqlite3

class BibliotecaController:
    """Controller: valida entradas e conecta ações da View ao Model."""
    def __init__(self, model, view):
        self.model, self.view = model, view
        self.livros = []
        view.registrar_comandos(self.adicionar_livro, self.limpar_campos,
            lambda: self.mudar_status("Lido"), lambda: self.mudar_status("Não Lido"),
            self.remover_livro, self.mostrar_detalhes)
        self.atualizar_lista()

    def atualizar_lista(self):
        try:
            self.livros = self.model.listar()
            self.view.exibir_livros(self.livros); self.view.exibir_estatisticas(self.livros)
        except sqlite3.Error as erro: self.view.erro("Erro", f"Não foi possível listar os livros: {erro}")

    def adicionar_livro(self):
        titulo, autor, ano_texto, status = self.view.obter_dados_formulario()
        if not titulo: self.view.aviso("Aviso", "O título é obrigatório."); return
        ano = None
        if ano_texto:
            try: ano = int(ano_texto)
            except ValueError: self.view.aviso("Aviso", "O ano deve ser um número inteiro."); return
            if not 1400 <= ano <= 2030: self.view.aviso("Aviso", "Informe um ano entre 1400 e 2030."); return
        try:
            self.model.adicionar(titulo, autor, ano, status)
            self.view.limpar_formulario(); self.atualizar_lista(); self.view.informacao("Sucesso", "Livro adicionado!")
        except sqlite3.Error as erro: self.view.erro("Erro", f"Não foi possível adicionar o livro: {erro}")

    def _id_selecionado(self):
        indice = self.view.obter_indice_selecionado()
        if indice is None: self.view.informacao("Aviso", "Selecione um livro."); return None
        if indice >= len(self.livros): self.atualizar_lista(); return None
        return self.livros[indice][0]

    def mostrar_detalhes(self, event=None):
        indice = self.view.obter_indice_selecionado()
        if indice is None or indice >= len(self.livros): return
        try: self.view.exibir_detalhes(self.model.buscar_por_id(self.livros[indice][0]))
        except sqlite3.Error as erro: self.view.erro("Erro", f"Não foi possível carregar os detalhes: {erro}")

    def mudar_status(self, novo_status):
        livro_id = self._id_selecionado()
        if livro_id is None: return
        try:
            self.model.atualizar_status(livro_id, novo_status); self.atualizar_lista()
            self.view.exibir_detalhes(None); self.view.informacao("Sucesso", f"Livro marcado como {novo_status}!")
        except sqlite3.Error as erro: self.view.erro("Erro", f"Não foi possível atualizar o status: {erro}")

    def remover_livro(self):
        livro_id = self._id_selecionado()
        if livro_id is None or not self.view.confirmar("Confirmar", "Remover este livro da biblioteca?"): return
        try:
            self.model.remover(livro_id); self.atualizar_lista(); self.view.limpar_formulario()
            self.view.exibir_detalhes(None); self.view.informacao("Sucesso", "Livro removido!")
        except sqlite3.Error as erro: self.view.erro("Erro", f"Não foi possível remover o livro: {erro}")

    def limpar_campos(self): self.view.limpar_formulario()
