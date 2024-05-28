import json
import socket
import threading

from model.Board import Board
from .HandleEventsFromClient import HandleEventsFromClient


class ClientHandler(threading.Thread):
    def __init__(self, server, clientSocket, address):
        threading.Thread.__init__(self)
        self.server = server
        self.clientSocket: socket.socket = clientSocket
        self.address = address
        self.running = True
        self.lobby = None
        self.username = ''
        self.board = Board()
        self.ready = False

    def run(self):
        while self.running:

            data = self.clientSocket.recv(1024).decode()
            if not data:
                print('Client disconnected')
                self.server.removeClientHandler(self)
                self.stop()
                break

            print(f"Received from client {self.getUsername()} {data}")
            HandleEventsFromClient(self, json.loads(data)).start()

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username

    def setLobby(self, lobby):
        self.lobby = lobby

    def getLobby(self):
        return self.lobby

    def getAllUsernames(self):
        usernames = []
        if self.server.getAllClientHandlers():
            for clientHandler in self.server.getAllClientHandlers():
                usernames.append(clientHandler.getUsername())
        return usernames

    def getAllNotAvailableLobbies(self):
        notAvailableLobbies = []
        for lobby in self.server.lobbies:
            if len(lobby.players) == 2:
                notAvailableLobbies.append(lobby.id)
        return notAvailableLobbies


    def stop(self):
        self.running = False
        self.clientSocket.close()
