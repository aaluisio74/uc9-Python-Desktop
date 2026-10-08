class FuncionarioController:
    def __init__(self, model):
        self.model = model

    def salvar_funcionario(self, matricula, nome, cargo, departamento=""):
        # Validação corporativa obrigatória da Atividade 2
        if not matricula or not nome or not cargo:
            return False, "Todos os campos corporativos (Matrícula, Nome e Cargo) são obrigatórios!"
        
        return self.model.inserir(matricula, nome, cargo, departamento)

    def buscar_funcionarios(self, filtro=""):
        return self.model.listar_todos(filtro)

    def editar_funcionario(self, id_reg, matricula, nome, cargo, departamento=""):
        if not id_reg:
            return False, "Nenhum registro selecionado para edição."
        if not matricula or not nome or not cargo:
            return False, "Todos os campos são obrigatórios para edição."
        
        return self.model.atualizar(id_reg, matricula, nome, cargo, departamento)

    def excluir_funcionario(self, id_reg):
        if not id_reg:
            return False, "Nenhum registro selecionado para exclusão."
        return self.model.excluir(id_reg)
