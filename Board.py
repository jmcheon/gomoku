from copy import deepcopy


class Board:
    def __init__(self, board=None) -> None:
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

    def init_board(self) -> None:
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty_square

    def make_move(self, row: int, col: int) -> object:
        # create new board instance that inherits from the current state
        board = Board(self)

        # make move
        board.position[row, col] = self.player1

        # swap players
        (board.player1, board.player2) = (board.player2, board.player1)

        # return new board state
        return board

    # get whether the game is drawn
    def is_draw(self) -> bool:
        # loop over board square
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False
        return True

    # get whether is the game won
    def is_win(self) -> bool:
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

    # generate legal moves to play in the current position
    def generate_states(self) -> list:
        # define states list (move list - list of available actions to consider)
        action_lst = []
        for row in range(3):
            for col in range(3):
                if self.position[row, col] == self.empty_square:
                    action_lst.append(self.make_move(row, col))
        return action_lst

    def __str__(self) -> str:
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
    print("This is initial board state:", board)

    """
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
        """

    action_lst = board.generate_states()
    board = action_lst[0]
    print("First generated move has been made on the board:", board)

    action_lst = board.generate_states()
    for action in action_lst:
        print(action)
