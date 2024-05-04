

class Board:
    def __init__(self):
        self.x = 8
        self.y = 8
        self.board = [[0 for _ in range(self.y)] for _ in range(self.x)]
