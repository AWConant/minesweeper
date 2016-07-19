import unittest
import board
import cell

class TestMS(unittest.TestCase):
    def setUp(self):
        self.b = board.Board(9, 9, 10)

    def test_init_board(self):
        self.b.print_board()

    def test_valid_coord(self):
        self.assertFalse(self.b.valid_coord((-1, 0)))
        self.assertFalse(self.b.valid_coord((-10, -10)))
        self.assertTrue(self.b.valid_coord( (0, 0)))
        self.assertTrue(self.b.valid_coord( (4, 4)))
        self.assertTrue(self.b.valid_coord( (8, 8)))
        self.assertFalse(self.b.valid_coord((9, 8)))
        self.assertFalse(self.b.valid_coord((8, 9)))
        self.assertFalse(self.b.valid_coord((9, 9)))

if __name__ == '__main__':
    unittest.main()
