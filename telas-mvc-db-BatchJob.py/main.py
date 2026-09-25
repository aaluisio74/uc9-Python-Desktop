from model import AppModel
from control import AppController
from view import MainView

def main():
    model = AppModel()
    controller = AppController(model)
    app = MainView(controller)
    controller.set_views(app)
    app.mainloop()

if __name__ == "__main__":
    main()