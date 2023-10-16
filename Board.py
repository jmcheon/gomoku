from copy import deepcopy


class Board:
    def __init__(self, board=None):
        # define players
        self.player1 = "X"
        self.player2 = "O"
        self.empty_square = "."

        # define board position
        self.position = {}

        self.init_board()

        # create a copy of previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty_square

    def make_move(self, row, col):
        # create new board instance
        board = Board()

        # make move
        board.position[row, col] = self.player1

        # swap players
        (self.player1, self.player2) = (self.player2, self.player1)

        # return new board state
        return board

    # get whether the game is drawn
    def is_draw(self):
        # loop over board square
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False
        return True

    # get whether is the game won
    def is_win(self):
        # vertical sequence detection
        for col in range(3):
            winning_sequence = []
            for row in range(3):
                if self.position[row, col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True
        # horizontal sequence detection
        for row in range(3):
            winning_sequence = []
            for col in range(3):
                if self.position[row, col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True
        # 1st diagonal sequence detection
        winning_sequence = []
        for row in range(3):
            col = row
            if self.position[row, col] == self.player2:
                winning_sequence.append((row, col))
            if len(winning_sequence) == 3:
                return True
        # 2nd diagonal sequence detection
        winning_sequence = []
        for row in range(3):
            col = 3 - row - 1
            if self.position[row, col] == self.player2:
                winning_sequence.append((row, col))
            if len(winning_sequence) == 3:
                return True
        return False

    def __str__(self):
        board_str = ""
        for row in range(3):
            for col in range(3):
                board_str += "%s" % self.position[row, col]
            board_str += "\n"
        # prepend side to move
        if self.player1 == "X":
            board_str = (
                "\n--------------------\n 'X' to move:\n--------------------\n\n"
                + board_str
            )
        elif self.player1 == "O":
            board_str = (
                "\n--------------------\n 'O' to move:\n--------------------\n\n"
                + board_str
            )
        return board_str


if __name__ == "__main__":
    board = Board()
    board.position = {
        (0, 0): "O",
        (0, 1): "X",
        (0, 2): "O",
        (1, 0): "X",
        (1, 1): "O",
        (1, 2): "X",
        (2, 0): "O",
        (2, 1): "X",
        (2, 2): "X",
    }
    print(board)
    if board.is_win():
        print("Won:", board.is_win())
    else:
        print("Drawn:", board.is_draw())
