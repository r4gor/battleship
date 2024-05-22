import json
import threading

from EventFactory import EventFactory


class ServerHandler(threading.Thread):
    def __init__(self, serverSocket, client):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
        self.client = client
        self.running = True

    def run(self):
        while self.running:
            # Receive data from the server
            data = self.serverSocket.recv(1024).decode()
            if not data:
                event = EventFactory("notification", message="Server closed the connection")
                self.client.getMainController().addToQueue(json.loads(event))
                break

            self.client.getMainController().addToQueue(json.loads(data))

    def stop(self):
        self.running = False
