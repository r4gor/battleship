class Board:
    #  Positions
    #  0 -> free
    #  1 -> Carrier (5 spaces)
    #  2 -> Battleship (4 spaces)
    #  3 -> Cruiser (3 spaces)
    #  4 -> Submarine (3 spaces)
    #  5 -> Destroyer (2 spaces)
    # -1 -> destroyed spot

    def __init__(self):
        self.x = 10
        self.y = 10
        self.board = [[0 for _ in range(self.y)] for _ in range(self.x)]
        self.ships = {
            "Carrier": {"requiredSpaces": 5, "boardSymbol": 1},
            "Battleship": {"requiredSpaces": 4, "boardSymbol": 2},
            "Cruiser": {"requiredSpaces": 3, "boardSymbol": 3},
            "Submarine": {"requiredSpaces": 3, "boardSymbol": 4},
            "Destroyer": {"requiredSpaces": 2, "boardSymbol": 5}
        }

    def hitCoordinate(self, x, y):
        if self.board[x][y] >= 1:
            # hit - ship that got destroyed - allShipsGotDestroyed?
            status = ['hit', '', False]
            shipSymbol = self.board[x][y]
            self.board[x][y] = -1

            if not self.shipActive(shipSymbol):
                status[1] = self.get_ship_by_symbol(shipSymbol)

            status[2] = self.allShipsSunk()

            return status
        status = ['miss', '', False]
        return status

    def shipActive(self, shipSymbol):
        for row in self.board:
            for cell in row:
                if cell == shipSymbol:
                    return True
        return False

    def get_ship_by_symbol(self, symbol):
        for ship_name, details in self.ships.items():
            if details["boardSymbol"] == symbol:
                return ship_name
        return None

    def allShipsSunk(self):
        for row in self.board:
            for cell in row:
                if cell >= 1:
                    return False
        return True

    def getCoordinatesFromString(self, stringCoordinates):
        stringCoordinate = stringCoordinates.upper()
        coordinates = stringCoordinate.split(':')
        x1 = ord(coordinates[0][0]) - ord('A')
        y1 = int(coordinates[0][1])
        x2 = ord(coordinates[1][0]) - ord('A')
        y2 = int(coordinates[1][1])

        return x1, y1, x2, y2

    def canPlaceShip(self, shipType, stringCoordinates):
        x1, y1, x2, y2 = self.getCoordinatesFromString(stringCoordinates)

        # Can't place ship diagonally
        if x1 != x2 and y1 != y2:
            return False

        if x1 == x2:
            if abs(y1 - y2)+1 != self.ships[shipType]["requiredSpaces"]:
                return False

            if y1 < y2:
                for y in range(y1, y2 + 1):
                    if self.board[x1][y] >= 1 or self.board[x1][y] == -1:
                        return False
            else:
                for y in range(y1, y2 - 1, -1):
                    if self.board[x1][y] >= 1 or self.board[x1][y] == -1:
                        return False
        elif y1 == y2:
            if abs(x1 - x2)+1 != self.ships[shipType]["requiredSpaces"]:
                return False

            if x1 < x2:
                for x in range(x1, x2 + 1):
                    if self.board[x][y1] >= 1 or self.board[x][y1] == -1:
                        return False
            else:
                for x in range(x1, x2 - 1, -1):
                    if self.board[x][y1] >= 1 or self.board[x][y1] == -1:
                        return False

        return True

    def placeShip(self, shipType, stringCoordinates):
        x1, y1, x2, y2 = self.getCoordinatesFromString(stringCoordinates)

        if self.canPlaceShip(shipType, stringCoordinates):
            if x1 == x2:
                if y1 < y2:
                    for y in range(y1, y2 + 1):
                        self.board[x1][y] = self.ships[shipType]["boardSymbol"]
                else:
                    for y in range(y1, y2 - 1, -1):
                        self.board[x1][y] = self.ships[shipType]["boardSymbol"]
            elif y1 == y2:
                if x1 < x2:
                    for x in range(x1, x2 + 1):
                        self.board[x][y1] = self.ships[shipType]["boardSymbol"]
                else:
                    for x in range(x1, x2 - 1, -1):
                        self.board[x][y1] = self.ships[shipType]["boardSymbol"]
            return True
        else:
            return False
