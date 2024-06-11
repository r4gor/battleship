import unittest

from model.Board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_setup(self):
        for row in self.board.board:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_getCoordinatesFromString(self):
        coords = self.board.getCoordinatesFromString("A0:B0")
        self.assertEqual(coords, (0, 0, 1, 0))

        coords = self.board.getCoordinatesFromString("A1:A5")
        self.assertEqual(coords, (0, 1, 0, 5))

    def test_canPlaceShip(self):
        self.assertTrue(self.board.canPlaceShip("Carrier", "A0:A4"))
        self.assertFalse(self.board.canPlaceShip("Carrier", "A0:A5"))
        self.assertTrue(self.board.canPlaceShip("Destroyer", "B0:C0"))
        self.assertFalse(self.board.canPlaceShip("Destroyer", "B0:D0"))

        self.board.placeShip("Carrier", "A0:A4")
        self.assertFalse(self.board.canPlaceShip("Battleship", "A0:A3"))

    def test_placeShip(self):
        self.assertTrue(self.board.placeShip("Carrier", "A0:A4"))
        self.assertEqual(self.board.board[0][0], 1)
        self.assertEqual(self.board.board[0][4], 1)

        self.assertFalse(self.board.placeShip("Carrier", "A0:A5"))

        self.assertTrue(self.board.placeShip("Destroyer", "B0:C0"))
        self.assertEqual(self.board.board[1][0], 5)
        self.assertEqual(self.board.board[2][0], 5)

    def test_hitCoordinate(self):
        self.board.placeShip("Carrier", "A0:A4")
        self.assertEqual(self.board.hitCoordinate(0, 0), ['hit', '', False])
        self.assertEqual(self.board.board[0][0], -1)

        self.assertEqual(self.board.hitCoordinate(0, 5), ['miss', '', False])

    def test_shipActive(self):
        self.board.placeShip("Carrier", "A0:A4")
        self.assertTrue(self.board.shipActive(1))

        for i in range(5):
            self.board.hitCoordinate(0, i)
        self.assertFalse(self.board.shipActive(1))

    def test_allShipsSunk(self):
        self.assertTrue(self.board.allShipsSunk())

        self.board.placeShip("Carrier", "A0:A4")
        self.assertFalse(self.board.allShipsSunk())

        for i in range(5):
            self.board.hitCoordinate(0, i)
        self.assertTrue(self.board.allShipsSunk())

    def test_get_ship_by_symbol(self):
        self.assertEqual(self.board.get_ship_by_symbol(1), "Carrier")
        self.assertEqual(self.board.get_ship_by_symbol(2), "Battleship")
        self.assertEqual(self.board.get_ship_by_symbol(3), "Cruiser")
        self.assertEqual(self.board.get_ship_by_symbol(4), "Submarine")
        self.assertEqual(self.board.get_ship_by_symbol(5), "Destroyer")
        self.assertIsNone(self.board.get_ship_by_symbol(6))

    def test_diagonal_ship_placement(self):
        self.assertFalse(self.board.canPlaceShip("Carrier", "A0:C2"))
        self.assertFalse(self.board.placeShip("Carrier", "A0:C2"))

    def test_placing_on_occupied_space(self):
        self.board.placeShip("Carrier", "A0:A4")
        self.assertFalse(self.board.canPlaceShip("Destroyer", "A0:A1"))
        self.assertFalse(self.board.placeShip("Destroyer", "A0:A1"))

    def test_repeated_hits(self):
        self.board.placeShip("Carrier", "A0:A4")
        self.assertEqual(self.board.hitCoordinate(0, 0), ['hit', '', False])
        self.assertEqual(self.board.hitCoordinate(0, 0), ['miss', '', False])

    def test_edge_of_board_placement(self):
        self.assertTrue(self.board.canPlaceShip("Destroyer", "J0:J1"))
        self.assertTrue(self.board.placeShip("Destroyer", "J0:J1"))

        self.assertTrue(self.board.canPlaceShip("Destroyer", "I9:J9"))
        self.assertTrue(self.board.placeShip("Destroyer", "I9:J9"))

    def test_edge_case_ships(self):
        self.assertFalse(self.board.canPlaceShip("Carrier", "J6:J10"))
        self.assertFalse(self.board.placeShip("Carrier", "J6:J10"))

if __name__ == '__main__':
    unittest.main()
