import socket

from ClientSide.ServerHandler import ServerHandler
from ClientSide.view.LoginView import LoginView
from EventFactory import EventFactory


class LoginController:
    def __init__(self, controller):
        self.mainController = controller
        self.client = controller.client
        self.view = LoginView(self)

    def run(self):
        self.view.after(100, self.mainController.processEvents)
        # self.view.protocol("WM_DELETE_WINDOW", self.mainController.on_close)
        if self.mainController.mainLoopStarted:
            self.view.deiconify()
        else:
            self.mainController.mainLoopStarted = True
            self.view.mainloop()

    def connect(self):
        username = self.view.username_entry.get()
        lobby = self.view.lobby_entry.get()
        ip = self.view.ip_entry.get()
        port = self.view.port_entry.get()

        if not username:
            self.showResponse("Username must not be empty")
        elif len(username) > 6:
            self.showResponse("Username must be 6 characters max")
        elif not lobby:
            self.showResponse("Lobby must not be empty")
        elif len(lobby) > 4:
            self.showResponse("Lobby must be 4 characters max")
        elif not ip:
            self.showResponse("IP must not be empty")
        elif not port:
            self.showResponse("Port must not be empty")
        else:
            # self.view.show_message("Login successful")  # Placeholder for successful login action
            self.showResponse(self.connectToServer(ip, int(port), username, lobby))

    def checkUsernameAndLobby(self, username, lobby):
        usernameEvent = EventFactory("login", username=username, lobby=lobby)
        self.client.sendEvent(usernameEvent)

    def connectToServer(self, ip, port, username, lobby):
        try:
            self.client.setServerSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            self.client.getServerSocket().connect((ip, port))

            self.client.setServerHandler(ServerHandler(self.client.getServerSocket(), self.client))
            self.client.getServerHandler().start()

            self.checkUsernameAndLobby(username, lobby)

            return "Waiting for server confirmation"
        except socket.error:
            return "Server unavailable"

    def showResponse(self, response):
        self.view.show_message(response)
