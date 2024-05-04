import json
import socket
from ServerHandler import ServerListener


class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.openThreads = {}

    def start(self):
        print("Client started")

        desiredUsername = input("Set username: ")

        connected = False
        while not connected:
            try:
                ip = input("insert server ip:")
                port = int(input("insert server port:"))
                self.clientSocket.connect((ip, port))
                connected = True
            except ConnectionRefusedError:
                print("Server unavailable")
                connected = False

        serverListener = ServerListener(self)
        serverListener.start()
        self.openThreads['serverListener'] = serverListener

        msg = {
            "type": "set_username",
            "username": desiredUsername
        }
        self.clientSocket.send(json.dumps(msg).encode())

        serverListener.join()

    def setUsername(self, username):
        self.username = username


if __name__ == "__main__":
    client = Client()
    client.start()
