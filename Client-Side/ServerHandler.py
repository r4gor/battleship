import json
import threading
from EventsFromServerHandler import EventsFromServerHandler


class ServerListener(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.running = True

    def run(self):
        while self.running:
            # Receive data from the server
            data = self.client.clientSocket.recv(1024).decode()
            if not data:
                print("Server closed the connection")
                break

            EventsFromServerHandler(self.client, json.loads(data)).start()

    def stop(self):
        self.running = False
