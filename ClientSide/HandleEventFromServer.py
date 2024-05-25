import json
import threading


class HandleEventFromServer:
    def __init__(self, client, event):
        self.event = event
        self.client = client

        checkProperties = hasProperties(self.event, "type")
        if checkProperties == "OK":
            print(f"Received from server:  {self.event}")
            match self.event["type"].lower():
                case "serverconnectionlost":
                    self.handleServerConnectionLost()

                case "notification":
                    self.handleNotificationEvent()

                case "login":
                    self.handleLoginEvent()

                case _:
                    response = {
                        "type": "error",
                        "message": "Unknown event type"
                    }
                    self.client.sendEvent(json.dumps(response).encode())

        else:
            response = {
                "type": "error",
                "message": f"{checkProperties}"
            }
            self.client.sendEvent(json.dumps(response).encode())

    def handleNotificationEvent(self):
        self.client.getMainController().getCurrentController().showResponse(self.event["message"])

    def handleLoginEvent(self):
        if self.event["username"] != "" and self.event["lobby"] != "":
            self.client.setUsername(self.event["username"])

            self.client.getMainController().getCurrentController().showResponse("Logged in successfully")

            #Change to setup phase
            self.client.getMainController().show_setup()
        else:
            if self.event["username"] == "":
                self.client.getMainController().getCurrentController().showResponse("Username already taken")
            else:
                self.client.getMainController().getCurrentController().showResponse("Lobby not available")

    def handleServerConnectionLost(self):
        self.client.getMainController().show_login()


def hasProperties(event, *properties):
    for prop in properties:
        if prop not in event:
            return f"Missing {prop}"
    return "OK"
