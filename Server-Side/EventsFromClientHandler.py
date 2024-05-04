import json
import threading


class EventsFromClientHandler(threading.Thread):
    def __init__(self, clientHandler, event):
        threading.Thread.__init__(self)
        self.clientHandler = clientHandler
        self.event = event

    def run(self):
        checkProperties = hasProperties(self.event, "type")
        if checkProperties == "OK":
            print(f"Received from client {self.event}")
            match self.event["type"]:
                case "set_username":
                    handleSetUsernameEvent(self.clientHandler, self.event)

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


def handleSetUsernameEvent(clientHandler, event):
    if event["username"] not in clientHandler.getAllUsernames():

        clientHandler.setUsername(event["username"])

        response = {
            "type": "set_username",
            "result": "OK",
            "username": event["username"]
        }
        clientHandler.clientSocket.send(json.dumps(response).encode())
    else:
        response = {
            "type": "set_username",
            "result": "KO",
        }
        clientHandler.clientSocket.send(json.dumps(response).encode())


def hasProperties(event, *properties):
    for prop in properties:
        if prop not in event:
            return f"Missing {prop}"
    return "OK"
