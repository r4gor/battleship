import json
import threading

from EventFactory import EventFactory


class HandleEventsFromClient(threading.Thread):
    def __init__(self, clientHandler, event):
        threading.Thread.__init__(self)
        self.clientHandler = clientHandler
        self.event = event

    def run(self):
        checkProperties = self.hasProperties("type")
        if checkProperties == "OK":
            print(f"Received from client {self.event}")
            match self.event["type"]:
                case "login":
                    self.handleLoginEvent()

                case _:
                    response = {
                        "type": "error",
                        "message": "Unknown event type"
                    }
                    self.clientHandler.clientSocket.send(json.dumps(response))
        else:
            response = {
                "type": "error",
                "message": f"{checkProperties}"
            }
            self.clientHandler.clientSocket.send(json.dumps(response))

    def handleLoginEvent(self):
        if (self.event["username"] not in self.clientHandler.getAllUsernames() and
                self.event["lobby"] not in self.clientHandler.getAllNotAvailableLobbies()):

            self.clientHandler.setUsername(self.event["username"])

            self.clientHandler.setLobby(self.clientHandler.server.getOrCreateLobby(self.clientHandler,
                                                                                   self.event["lobby"]))

            response = EventFactory("login", username=self.event["username"], lobby=self.event["lobby"])
            self.clientHandler.clientSocket.send(response)
        else:
            if self.event["username"] in self.clientHandler.getAllUsernames():
                response = {
                    "type": "login",
                    "username": "",
                    "lobby": ""
                }
            else:
                response = {
                    "type": "login",
                    "username": self.event["username"],
                    "lobby": ""
                }
            self.clientHandler.clientSocket.send(json.dumps(response).encode())

    def hasProperties(self, *properties):
        for prop in properties:
            if prop not in self.event:
                return f"Missing {prop}"
        return "OK"
