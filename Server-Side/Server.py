import json
import socket
from ClientHandler import ClientHandler


class Server:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        self.clientHandlers = []
        self.lobbies = []

    def start(self):
        self.socket.listen(5)

        while True:
            print("Server started")
            clientSocket, address = self.socket.accept()
            print("Client connected" + str(address))

            msg = {
                "type": "notification",
                "msg": "Welcome to the server! Please send your desired username",
            }
            clientSocket.send(json.dumps(msg).encode())
            print("server sent: " + json.dumps(msg))

            clientHandler = ClientHandler(self, clientSocket, address)
            clientHandler.start()

            self.clientHandlers.append(clientHandler)

    def stop_handlers(self):
        for handler in self.clientHandlers:
            handler.stop()

    def getAllClientHandlers(self):
        handlers = []
        for handler in self.clientHandlers:
            handlers.append(handler)
        return

    def addLobby(self, lobby):
        self.lobbies.append(lobby)

    def removeLobby(self, lobby):
        self.lobbies.remove(lobby)


if __name__ == "__main__":
    server = Server(54321)
    server.start()
