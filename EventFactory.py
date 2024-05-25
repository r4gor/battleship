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
