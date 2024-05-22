import queue

from ClientSide.controllers.SetupController import SetupController
from ClientSide.controllers.LoginController import LoginController
from ClientSide.HandleEventFromServer import HandleEventFromServer


class Controller:
    def __init__(self, client):
        self.client = client
        self.title = "Battleship"
        self.geometry = "1366x768"
        self.current_controller = None
        self.event_queue = queue.Queue()

    def start(self):
        self.show_login()

    def processEvents(self):
        while self.event_queue.qsize() > 0:
            event = self.event_queue.get(block=False)
            HandleEventFromServer(self.client, event)
        self.current_controller.view.after(100, self.processEvents)

    def switch_controller(self, new_controller_class):
        if self.current_controller is not None:
            self.current_controller.view.withdraw()

        self.current_controller = new_controller_class(self)
        self.current_controller.run()

    def addToQueue(self, data):
        self.event_queue.put(data)

    def show_login(self):
        self.switch_controller(LoginController)

    def show_setup(self):
        self.switch_controller(SetupController)

    def getCurrentController(self):
        return self.current_controller

    # def show_game(self):
    #     self.switch_controller(GameController, False)
