from ClientSide.view.GameView import GameView
from EventFactory import EventFactory


class GameController:
    def __init__(self, controller):
        self.mainController = controller
        self.client = controller.client
        self.view = GameView(controller.main_window, self)

    def run(self):
        self.view.pack(fill="both", expand=True)

    def showResponse(self, response, time=5000):
        self.view.show_message(response, time)

    def hit(self, x, y):
        if self.client.turn:
            self.client.turn = False
            self.view.disable_button(x, y)
            self.view.hide_message()
            event = EventFactory("hit", x=x, y=y)
            self.client.sendEvent(event)
        else:
            self.showResponse("It's not your turn!")

    def hitMyBoard(self, x, y):
        status = self.client.board.hitCoordinate(x, y)
        if status[0] == 'hit':
            self.view.myBoardButtons[(x, y)].configure(fg_color="red")
            if status[1] != '':
                self.view.get_status_label_myBoard(status[1]).configure(text="Sunk", text_color="red")
                if status[2]:
                    self.view.disable_all_buttons()

                    self.showResponse("You Lost!\n Redirecting to\n login in 10 sec", 10000)
                    self.mainController.main_window.after(10000, self.mainController.show_login)
        else:
            self.view.myBoardButtons[(x, y)].configure(fg_color="grey")

    def hitOpponentBoard(self, x, y, shipType, allShipsSunk):
        self.view.opponentBoardButtons[(x, y)].configure(fg_color="red")
        if shipType != '':
            self.view.get_status_label_opponentBoard(shipType).configure(text="Sunk", text_color="red")
            if allShipsSunk:
                self.view.disable_all_buttons()

                self.showResponse("You WIN!\n Redirecting to\n login in 10 sec", 10000)
                self.mainController.main_window.after(10000, self.mainController.show_login)

    def missOpponentBoard(self, x, y):
        self.view.opponentBoardButtons[(x, y)].configure(fg_color="grey")
