import json
import threading


class EventsFromServerHandler(threading.Thread):
    def __init__(self, client, event):
        threading.Thread.__init__(self)
        self.client = client
        self.event = event

    def run(self):
        checkProperties = hasProperties(self.event, "type")
        if checkProperties == "OK":
            print(f"Received from server:  {self.event}")
            match self.event["type"].lower():
                case "notification":
                    handleNotificationEvent(self.client, self.event)

                case "set_username":
                    handleSetUsernameEvent(self.client, self.event)

                case "error":
                    handleErrorEvent(self.client, self.event)

                case _:
                    response = {
                        "type": "error",
                        "message": "Unknown event type"
                    }
                    self.client.clientSocket.send(json.dumps(response))

        else:
            response = {
                "type": "error",
                "message": f"{checkProperties}"
            }
            self.client.clientSocket.send(json.dumps(response))


def handleNotificationEvent(client, event):
    print("Received notification event: " + json.dumps(event))


def handleSetUsernameEvent(client, event):
    if event["result"] == "OK":
        print(f"Username {event["username"]} set successfully")
        client.setUsername(event["username"])
    else:
        print("Username already taken")
        username = input("Set new username: ")
        response = {
            "type": "set_username",
            "username": username
        }
        client.clientSocket.send(json.dumps(response))


def hasProperties(event, *properties):
    for prop in properties:
        if prop not in event:
            return f"Missing {prop}"
    return "OK"


def handleErrorEvent(client, event):
    print("Received error event: " + json.dumps(event))
