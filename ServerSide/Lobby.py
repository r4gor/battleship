

class Lobby:
    def __init__(self, server, name):
        self.server = server
        self.id = name
        self.players = []

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        if len(self.players) == 0:
            self.server.removeLobby(self)