from hrms_model import FuncionarioModel
from hrms_controller import FuncionarioController
from hrms_view import JanelaPrincipal

if __name__ == "__main__":
    # Instancia o banco de dados e regras de negócio
    model = FuncionarioModel()
    controller = FuncionarioController(model)

    # Inicia a janela principal da aplicação
    app = JanelaPrincipal(controller)
    app.mainloop()
