import json
import socket
import threading
import time

from EventFactory import EventFactory
from .ClientHandler import ClientHandler
from ServerSide.Lobby import Lobby


# Synchronizer
def synchronized_with_attr(lock_name):
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator


class Server:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        self.clientHandlers = []
        self.lobbies = []
        self.lock = threading.RLock()

    def start(self):
        self.socket.listen(5)
        print("Server started")

        while True:
            clientSocket, address = self.socket.accept()
            print("Client connected" + str(address))

            clientHandler = ClientHandler(self, clientSocket, address)
            clientHandler.daemon = True
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

    @synchronized_with_attr('lock')
    def removeClientHandler(self, clientHandler):
        for lobby in self.lobbies:
            if lobby.id == clientHandler.lobby.id:
                #Lobby automatically gets removed if remains empty
                lobby.remove_player(clientHandler)

                if lobby.gameStarted and len(lobby.players) > 0:
                    notification = EventFactory("opponentLeft")
                    lastPlayerInLobby = lobby.players[0]
                    lastPlayerInLobby.clientSocket.send(notification)

                    # lobby.remove_player(lastPlayerInLobby)
                    # self.clientHandlers.remove(lastPlayerInLobby)
                    # lastPlayerInLobby.stop()
        if clientHandler in self.clientHandlers:
            self.clientHandlers.remove(clientHandler)
        if clientHandler.running:
            clientHandler.stop()

    @staticmethod
    def broadcastLobby(lobby, event):
        for player in lobby.players:
            player.clientSocket.send(event)


if __name__ == "__main__":
    server = Server(5555)
    server.start()
