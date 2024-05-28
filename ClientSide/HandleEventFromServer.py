import json
import threading


class HandleEventFromServer:
    def __init__(self, client, event):
        self.event = event
        self.client = client

        checkProperties = hasProperties(self.event, "type")
        if checkProperties == "OK":
            match self.event["type"]:
                case "serverConnectionLost":
                    self.handleServerConnectionLost()

                case "notification":
                    self.handleNotificationEvent()

                case "login":
                    self.handleLoginEvent()

                case "start":
                    self.handleStartEvent()

                case "turn":
                    self.handleTurnEvent()

                case "hit":
                    self.handleHitEvent()

                case "hitConfirm":
                    self.handleHitConfirmEvent()

                case "hitMiss":
                    self.handleHitMissEvent()

                case _:
                    response = {
                        "type": "error",
                        "message": "Unknown event type"
                    }
                    print("Unknown event type")
                    print(self.event)
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
            self.client.setLobby(self.event["lobby"])

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

    def handleStartEvent(self):
        self.client.getMainController().show_game()

    def handleTurnEvent(self):
        if self.event["player"] == self.client.getUsername():
            self.client.turn = True
            self.client.getMainController().getCurrentController().showResponse("It's your turn")
        else:
            self.client.turn = False

    def handleHitEvent(self):
        self.client.getMainController().getCurrentController().hitMyBoard(self.event["x"],
                                                                          self.event["y"])

    def handleHitConfirmEvent(self):
        self.client.getMainController().getCurrentController().hitOpponentBoard(self.event["x"],
                                                                                self.event["y"],
                                                                                self.event["sunk"],
                                                                                self.event["allShipsSunk"])

    def handleHitMissEvent(self):
        self.client.getMainController().getCurrentController().missOpponentBoard(self.event["x"], self.event["y"])




def hasProperties(event, *properties):
    for prop in properties:
        if prop not in event:
            return f"Missing {prop}"
    return "OK"
