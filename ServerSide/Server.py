import json
import socket
from .ClientHandler import ClientHandler
from ServerSide.Lobby import Lobby


class Server:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        self.clientHandlers = []
        self.lobbies = []

    def start(self):
        self.socket.listen(5)
        print("Server started")

        while True:
            clientSocket, address = self.socket.accept()
            print("Client connected" + str(address))

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
        return handlers

    def addLobby(self, lobby):
        self.lobbies.append(lobby)

    def removeLobby(self, lobby):
        self.lobbies.remove(lobby)

    def getOrCreateLobby(self, clientHandler, lobbyID):
        for lobby in self.lobbies:
            if lobby.id == lobbyID:
                lobby.add_player(clientHandler)
                return lobby
        newLobby = Lobby(self, lobbyID)
        newLobby.add_player(clientHandler)
        self.addLobby(newLobby)
        return newLobby

    def removeClientHandler(self, clientHandler):
        for lobby in self.lobbies:
            if lobby.id == clientHandler.lobby.id:
                #Lobby automatically gets removed if remains empty
                lobby.remove_player(clientHandler)
        self.clientHandlers.remove(clientHandler)

    @staticmethod
    def broadcastLobby(lobby, event):
        for player in lobby.players:
            player.clientSocket.send(event)


if __name__ == "__main__":
    server = Server(5555)
    server.start()
