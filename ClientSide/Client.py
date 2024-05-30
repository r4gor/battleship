from ClientSide.controllers.Controller import Controller
from model.Board import Board


class Client:
    def __init__(self):
        self.controller = None
        self.username = None
        self.lobbyID = None
        self.serverHandler = None
        self.serverSocket = None
        self.board = Board()
        self.turn = False

    def start(self):
        print("Client started")
        self.controller = Controller(self)

        self.controller.start()

    def sendEvent(self, event):
        if self.serverSocket is not None:
            self.serverSocket.send(event)

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def setLobby(self, lobbyID):
        self.lobbyID = lobbyID

    def getLobby(self):
        return self.lobbyID

    def setServerHandler(self, handler):
        self.serverHandler = handler

    def getServerHandler(self):
        return self.serverHandler

    def setServerSocket(self, serverSocket):
        self.serverSocket = serverSocket

    def getServerSocket(self):
        return self.serverSocket

    def setMainController(self, controller):
        self.controller = controller

    def getMainController(self):
        return self.controller

    def reset(self):
        self.username = None
        self.lobbyID = None
        self.serverHandler = None
        self.serverSocket = None
        self.board = Board()
        self.turn = False

if __name__ == "__main__":
    client = Client()
    client.start()
