import json
import threading
import time

from EventFactory import EventFactory


class HandleEventsFromClient(threading.Thread):
    def __init__(self, clientHandler, event):
        threading.Thread.__init__(self)
        self.clientHandler = clientHandler
        self.event = event

    def run(self):
        checkProperties = self.hasProperties("type")
        if checkProperties == "OK":
            match self.event["type"]:
                case "login":
                    self.handleLoginEvent()

                case "setup":
                    self.handleSetupEvent()

                case "hit":
                    self.handleHitEvent()

                case "quit":
                    self.handleQuitEvent()

                case _:
                    response = {
                        "type": "error",
                        "message": "Unknown event type"
                    }
                    print('Unknown event type')
                    print(self.event)
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

    def handleSetupEvent(self):
        self.clientHandler.ready = True
        for shipType in self.event:
            if shipType != "type":
                self.clientHandler.board.placeShip(shipType, self.event[shipType])

        if (len(self.clientHandler.lobby.players) == 2 and
                self.clientHandler.lobby.players[0].ready and
                self.clientHandler.lobby.players[1].ready):
            # Signal start of game phase
            event = EventFactory("start")
            self.clientHandler.server.broadcastLobby(self.clientHandler.lobby, event)

            self.clientHandler.lobby.gameStarted = True

            time.sleep(0.3)
            # Send turn event
            self.sendTurn()

    def sendTurn(self):
        event2 = EventFactory("turn", player=self.clientHandler.lobby.players[0].getUsername())
        self.clientHandler.lobby.players.reverse()
        self.clientHandler.server.broadcastLobby(self.clientHandler.lobby, event2)

    def hasProperties(self, *properties):
        for prop in properties:
            if prop not in self.event:
                return f"Missing {prop}"
        return "OK"

    def handleHitEvent(self):
        status = self.clientHandler.lobby.players[0].board.hitCoordinate(self.event["x"], self.event["y"])
        if status[0] == 'hit':
            # Confirm hit
            hitConfirmEvent = EventFactory("hitConfirm",
                                           x=self.event["x"],
                                           y=self.event["y"],
                                           sunk=status[1],
                                           allShipsSunk=status[2])
            self.clientHandler.clientSocket.send(hitConfirmEvent)
        else:
            hitMissEvent = EventFactory("hitMiss", x=self.event["x"], y=self.event["y"])
            self.clientHandler.clientSocket.send(hitMissEvent)

        time.sleep(0.2)
        # First player in lobby player list is the next player about to execute turn
        # Send to the other player which coordinate was hit
        hitEvent = EventFactory("hit", x=self.event["x"], y=self.event["y"])
        self.clientHandler.lobby.players[0].clientSocket.send(hitEvent)

        time.sleep(0.2)
        if not status[2]:
            self.sendTurn()
        # else:
        #     self.gameEnded(self.clientHandler)

    def handleQuitEvent(self):
        # self.clientHandler.clientSocket.close()
        if self.clientHandler in self.clientHandler.server.clientHandlers:
            self.clientHandler.server.removeClientHandler(self.clientHandler)

    @staticmethod
    def gameEnded(clientHandler):
        time.sleep(10)
        for ch in clientHandler.lobby.players:
            ch.server.removeClientHandler(ch)
            ch.stop()
