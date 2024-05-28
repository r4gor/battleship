import json


class WrongEvent(Exception):
    def __init__(self, message):
        super().__init__(message)


def EventFactory(eventType, **kwargs):
    event = None
    match eventType:
        case 'serverConnectionLost':
            event = generateServerConnectionLostEvent(eventType, kwargs)

        case 'notification':
            event = generateNotificationEvent(eventType, kwargs)

        case 'login':
            event = generateLoginEvent(eventType, kwargs)

        case 'setup':
            event = generateSetupEvent(eventType, kwargs)

        case 'start':
            event = generateStartEvent(eventType, kwargs)

        case 'turn':
            event = generateTurnEvent(eventType, kwargs)

        case 'hit':
            event = generateHitEvent(eventType, kwargs)

        case 'hitConfirm':
            event = generateHitConfirmEvent(eventType, kwargs)

        case 'hitMiss':
            event = generateHitMissEvent(eventType, kwargs)

        case _:
            raise WrongEvent(f'Wrong event type {eventType}')

    return json.dumps(event).encode()


def generateServerConnectionLostEvent(eventType, kwargs):
    event = {
        "type": eventType
    }
    return event


def generateNotificationEvent(eventType, kwargs):
    if 'message' in kwargs:
        event = {
            "type": eventType,
            "message": kwargs['message']
        }
        return event
    else:
        raise WrongEvent(f'Event missing required arguments {eventType} - {str(kwargs)} ')


def generateLoginEvent(eventType, kwargs):
    if 'username' in kwargs and 'lobby' in kwargs:
        event = {
            "type": eventType,
            "username": kwargs['username'],
            "lobby": kwargs['lobby']
        }
        return event
    else:
        raise WrongEvent(f'Event missing required arguments {eventType} - {str(kwargs)} ')


def generateSetupEvent(eventType, kwargs):
    event = {
        "type": eventType,
        "Carrier": kwargs['Carrier'],
        "Battleship": kwargs['Battleship'],
        "Cruiser": kwargs['Cruiser'],
        "Submarine": kwargs['Submarine'],
        "Destroyer": kwargs['Destroyer']
    }
    return event


def generateTurnEvent(eventType, kwargs):
    event = {
        "type": eventType,
        "player": kwargs['player'],
    }
    return event


def generateStartEvent(eventType, kwargs):
    event = {
        "type": eventType
    }
    return event


def generateHitEvent(eventType, kwargs):
    event = {
        "type": eventType,
        "x": kwargs['x'],
        "y": kwargs['y']
    }
    return event


def generateHitConfirmEvent(eventType, kwargs):
    event = {
        "type": eventType,
        "x": kwargs['x'],
        "y": kwargs['y'],
        "sunk": kwargs['sunk'],
        "allShipsSunk": kwargs["allShipsSunk"]
    }
    return event


def generateHitMissEvent(eventType, kwargs):
    event = {
        "type": eventType,
        "x": kwargs['x'],
        "y": kwargs['y']
    }
    return event
