import json
import threading

from EventFactory import EventFactory


class ServerHandler(threading.Thread):
    def __init__(self, serverSocket, client):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
        self.client = client
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            # Receive data from the server
            data = self.serverSocket.recv(1024).decode()
            if not data:
                event = EventFactory("serverConnectionLost")
                self.client.getMainController().addToQueue(json.loads(event))

                #Wait for event to get processed
                while self.client.getMainController().event_queue.qsize() > 0:
                    pass

                event2 = EventFactory("notification", message="Server closed the connection")
                self.client.getMainController().addToQueue(json.loads(event2))
                break

            print(f"Received from server:  {data}")
            self.client.getMainController().addToQueue(json.loads(data))

    def stop(self):
        self._stop_event.set()
        self.serverSocket.close()
