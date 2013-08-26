import sys

def enum(*sequential, **named):
        """
        Create a class the mimics enumeration behaviour
        """
        enums = dict(zip(sequential, range(len(sequential))), **named)
        
        return type('Enum', (), enums)
        
class Board(object):
    """
    This is the board object in play
    """
    Disk = enum(Empty=0, White=1, Black=2)
    
    def __init__(self):
        """
        Setup the board with size 8.
        Layout the board with starting layout, following convention that
        the dark disks are NE and SW
        """
        self._size=8
        
        self._starting_layout = [[Board.Disk.Empty for i in range(self._size)] for j in range(self._size)]
        self._starting_layout[3][3] = Board.Disk.White
        self._starting_layout[4][4] = Board.Disk.White
        self._starting_layout[3][4] = Board.Disk.Black
        self._starting_layout[4][3] = Board.Disk.Black
        
        self._board_size = self._size
        self._column_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._row_labels = ['1', '2', '3', '4', '5', '6', '7', '8']
        self._board = [[Board.Disk.Empty for i in range(self._size)] for j in range(self._size)]
        
        self.initialize_board()
        
    def print_board(self):
        """
        Print the board onto the console
        """
        print self.create_row(' ', self._column_labels)
        
        for i in range (len(self._board)):
            print self.create_row(self._row_labels[i], self._board[i][:])
        
        row = ""
        for label in self._column_labels:
            row = row + "%(column_label)s" % {"column_label": label}
        print self.create_row(' ', self._column_labels)
        
    def sizeof(self):
        """
        Return the size of the board as a listh
        """
        return [len(self._board[:][0]),len(self._board[0][:])]
        
    def create_row(self, label, contents):
        """
        Generate the row contents to print
        """
        output_row = label
        
        for data in contents:
            output_row = output_row + "%(column_data)s" % {"column_data": data}
        output_row = output_row + label
        
        return output_row
    
    def update_square(self, update_column, update_row, new_value):
        """
        Update the specified square with the new value.
        We follow othello convention and specify the column first e.g. d4
        """
        try:
            column = self._column_labels.index(update_column)
            row = self._row_labels.index(update_row)
            
            if new_value == Board.Disk.Empty:
                self._board[row][column] = new_value
            elif new_value == Board.Disk.White:
                self._board[row][column] = new_value
            elif new_value == Board.Disk.Black:
                self._board[row][column] = new_value
            else:
                raise ValueError("%(input)s is not valid Disk value. Try 0, 1, or 2" % {"input": new_value})
        except ValueError as ve:
            print ve
        except:
            print sys.exc_info()
            raise
            
    def check_square(self, update_column, update_row):
        """
        For a given set of coordinates, return the current disk state
        """
        try:
            column = self._column_labels.index(update_column)
            row = self._row_labels.index(update_row)
            
            return self._board[row][column]
        except:
            print sys.exc_info()
            raise
        
    def initialize_board(self, layout=None):
        """
        Setup the disks in the specified configuration, if none given
        use the starting configuration
        """
        size = self.sizeof()
        
        if layout==None:
            layout=self._starting_layout
        
        for i in range(size[0]):
            for j in range(size[0]):
                self._board[i][j] = layout[i][j]
        
    def full_board(self):
        """
        Determines if the board has been completed
        """
        return False
        
class CommandLineHelper(object):
    """
    This contains all the command line parsing stuff and input handling
    as well as the strings to display
    """
    def __init__(self):
        """
        setup the game on turn 1
        """
        _turn = 1
    
    @staticmethod
    def current_player(turn):
        """
        Based on the turn, tells which player's turn it is
        """
        try:
            turn = int(turn)
            if turn % 2 == 0:
                return 1
            else:
                return 2
        except ValueError:
            print("Turn should be an int")
    
    @staticmethod        
    def game_intro(game_board):
        """
        Display the starting text and display the starting board
        """
        intro_text = """Welcome to Othello.
The second player (dark) begins the game. The game continues until the board is full or no moves can be made."""
                         
        try:
            print intro_text
            game_board.print_board()
        except AttributeError:
            print("You need to pass in a game board object.")
        except:
            print sys.exc_info()
            raise
            
    @staticmethod        
    def player_prompt(current_player, game_board):
        """
        Prompt the player for a move. If the move is bad, keep prompting.
        """
        checked_move=None
        while checked_move==None:
            prompt = "Player %(current_player)s's move" % {"current_player": current_player}
            move=raw_input(prompt + ": ")
            checked_move = CommandLineHelper.check_move(move, game_board)
            if checked_move != None:
                CommandLineHelper.complete_move(current_player, move, game_board)
        
        return checked_move
    
    @staticmethod
    def check_move(player_input, game_board):
        """
        Process players command line input
        """
        try:
            game_board.check_square('d', '4')
            if len(player_input) == 2:
                return player_input
            else:
                print "Moves must be column followed by row, e.g. a1"
                return None
        except AttributeError:
            print("You need to pass in a game board object.")
        except ValueError:
            print "Valid columns are a, b, c, d, e, f, g, and h. Valid rows are 1, 2, 3, 4, 5, 6, 7, and 8"
        except:
            print sys.exc_info()
            raise
            
    @staticmethod
    def complete_move(player, player_input, game_board):
        """
        Take in moves in column-row format and parse to match method on board
        """
        column = player_input[0]
        row = player_input[1]
        
        if player == Board.Disk.White:
            game_board.update_square(column, row, Board.Disk.White)
        elif player == Board.Disk.Black:
            game_board.update_square(column, row, Board.Disk.Black)
        else:
            print "Invalid player id. Player must be 1 (white) or 2 (dark)"
        
def main():
    board = Board()

    turn = 1
    CommandLineHelper.game_intro(board)
    while board.full_board() == False:
        player = CommandLineHelper.current_player(turn)
            
        current_move = CommandLineHelper.player_prompt(player, board)
        
        turn = turn + 1
        board.print_board()

if __name__ == "__main__":
    main()