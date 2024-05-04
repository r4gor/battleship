import json
import threading
from EventsFromClientHandler import EventsFromClientHandler


class ClientHandler(threading.Thread):
    def __init__(self, server, clientSocket, address):
        threading.Thread.__init__(self)
        self.server = server
        self.clientSocket = clientSocket
        self.address = address
        self.running = True
        self.Lobby = None
        self.username = ''

    def run(self):
        while self.running:

            data = self.clientSocket.recv(1024).decode()
            if not data:
                break

            EventsFromClientHandler(self, json.loads(data)).start()

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username

    def getAllUsernames(self):
        usernames = []
        if self.server.getAllClientHandlers():
            for clientHandler in self.server.getAllClientHandlers():
                usernames.append(clientHandler.getUsername())
        return usernames

    def stop(self):
        self.running = False
        self.clientSocket.close()
