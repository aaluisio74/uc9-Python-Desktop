import tkinter as tk
from models.livro_model import LivroModel
from views.biblioteca_view import BibliotecaView
from controllers.biblioteca_controller import BibliotecaController

def main():
    janela = tk.Tk()
    model = LivroModel()
    view = BibliotecaView(janela)
    BibliotecaController(model, view)
    janela.mainloop()

if __name__ == "__main__":
    main()
