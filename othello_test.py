import othello
import unittest

class TestBoardClass(unittest.TestCase):
    
    def setUp(self):
        self.test_board = othello.Board()
        
    def test_create_board(self):
        """
        Check the dimension of the create_board
        """
        size = self.test_board.sizeof()
        
        self.assertEqual(size[0],size[1])
        self.assertEqual(size[0],8)
        
    def test_check_disks_emun(self):
        """
        Check that the enum for the disk values is there
        """
        self.assertEqual(self.test_board.Disk.Empty, 0)
        self.assertEqual(self.test_board.Disk.White, 1)
        self.assertEqual(self.test_board.Disk.Black, 2)
        
    def test_update_square(self):
        """
        See if you can update a square using othello grid coordinates
        """
        self.test_board.update_square('a', '1', self.test_board.Disk.White)
        self.test_board.update_square('f', '7', self.test_board.Disk.Black)

        self.assertEqual(self.test_board._board[0][0], self.test_board.Disk.White)
        self.assertEqual(self.test_board._board[6][5], self.test_board.Disk.Black)
        
    def test_check_square(self):
        """
        Test getting back square values
        """
        self.assertEqual(self.test_board.check_square('b','1'), self.test_board.Disk.Empty)
        self.assertEqual(self.test_board.check_square('e','5'), self.test_board.Disk.White)
        
    def tearDown(self):
        pass
        
if __name__ == '__main__':
    unittest.main(verbosity=2)