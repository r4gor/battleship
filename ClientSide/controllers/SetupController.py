from ClientSide.view.SetupView import SetupView


class SetupController:
    def __init__(self, controller):
        self.mainController = controller
        self.client = controller.client
        self.view = SetupView(self)

    def run(self):
        self.view.deiconify()
