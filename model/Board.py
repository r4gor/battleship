class Board:
    #  Positions
    #  0 -> free
    #  1 -> occupied by ship
    # -1 -> destroyed ship
    def __init__(self):
        self.x = 10
        self.y = 10
        self.board = [[0 for _ in range(self.y)] for _ in range(self.x)]

    def hitCoordinate(self, x, y):
        if self.board[x][y] == 1:
            self.board[x][y] = -1
            return True
        return False

    def getCoordinatesFromString(self, stringCoordinates):
        stringCoordinate = stringCoordinates.upper()
        coordinates = stringCoordinate.split(':')
        x1 = ord(coordinates[0]) - ord('A')
        y1 = int(coordinates[1]) - 1
        x2 = ord(coordinates[2]) - ord('A')
        y2 = int(coordinates[1]) - 1

        return x1, y1, x2, y2

    def canPlaceShip(self, stringCoordinates):
        x1, y1, x2, y2 = self.getCoordinatesFromString(stringCoordinates)

        if x1 != x2 and y1 != y2:
            return False

        if x1 == x2:
            if y1 < y2:
                for y in range(y1, y2 + 1):
                    if self.board[x1][y] == 1 or self.board[x1][y] == -1:
                        return False
            else:
                for y in range(y1, y2 - 1, -1):
                    if self.board[x1][y] == 1 or self.board[x1][y] == -1:
                        return False
        elif y1 == y2:
            if x1 < x2:
                for x in range(x1, x2 + 1):
                    if self.board[x][y1] == 1 or self.board[x][y1] == -1:
                        return False
            else:
                for x in range(x1, x2 - 1, -1):
                    if self.board[x][y1] == 1 or self.board[x][y1] == -1:
                        return False

        return True

    def placeShip(self, stringCoordinates):
        x1, y1, x2, y2 = self.getCoordinatesFromString(stringCoordinates)

        if self.canPlaceShip(stringCoordinates):
            if x1 == x2:
                if y1 < y2:
                    for y in range(y1, y2 + 1):
                        self.board[x1][y] = 1
                else:
                    for y in range(y1, y2 - 1, -1):
                        self.board[x1][y] = 1
            elif y1 == y2:
                if x1 < x2:
                    for x in range(x1, x2 + 1):
                        self.board[x][y1] = 1
                else:
                    for x in range(x1, x2 - 1, -1):
                        self.board[x][y1] = 1
            return True
        else:
            return False
