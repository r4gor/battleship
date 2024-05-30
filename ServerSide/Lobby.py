

class Lobby:
    def __init__(self, server, name):
        self.server = server
        self.id = name
        self.players = []
        self.gameStarted = False

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
            print(f"Player {player.getUsername()} removed from lobby {self.id}")

        if len(self.players) == 0:
            self.server.removeLobby(self)
            print(f"Lobby {self.id} removed")
