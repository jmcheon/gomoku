from copy import deepcopy

from config import *

# from doublethree import *


class Board:
    def __init__(self, board=None) -> None:
        # define players
        self.player1 = PLAYER1
        self.player2 = PLAYER2
        self.empty_square = "."

        # define board position
        self.position = [["."] * NUM_LINES for _ in range(NUM_LINES)]

        # self.init_board()

        # create a copy of previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self) -> None:
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                self.position[row][col] = self.empty_square

    def get_value(self, col: int, row: int) -> str:
        return self.position[row][col]

    def set_value(self, col: int, row: int, value: str) -> str:
        self.position[row][col] = value
        return value

    def make_move(self, col: int, row: int) -> object:
        # create new board instance that inherits from the current state
        board = Board(self)

        # make move
        board.position[row][col] = self.player1

        # swap players
        board.swap_player()
        # (board.player1, board.player2) = (board.player2, board.player1)

        # return new board state
        return board

    def swap_player(self) -> None:
        (self.player1, self.player2) = (self.player2, self.player1)

    # get whether the game is drawn
    def is_draw(self) -> bool:
        # loop over board square
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.position[row][col] == self.empty_square:
                    return False
        return True

    # get whether is the game won
    def is_win(self) -> bool:
        # vertical sequence detection
        for col in range(NUM_LINES):
            winning_sequence = []
            for row in range(NUM_LINES):
                if self.position[row][col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) >= 5:
                    return True
        # horizontal sequence detection
        for row in range(NUM_LINES):
            winning_sequence = []
            for col in range(NUM_LINES):
                if self.position[row][col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) >= 5:
                    return True
        # 1st diagonal sequence detection
        winning_sequence = []
        for row in range(NUM_LINES):
            col = row
            if self.position[row][col] == self.player2:
                winning_sequence.append((row, col))
            if len(winning_sequence) >= 5:
                return True
        # 2nd diagonal sequence detection
        winning_sequence = []
        for row in range(NUM_LINES):
            col = NUM_LINES - row - 1
            if self.position[row][col] == self.player2:
                winning_sequence.append((row, col))
            if len(winning_sequence) >= 5:
                return True
        return False

    # generate legal moves to play in the current position
    def generate_states(self) -> list:
        # define states list (move list - list of available actions to consider)
        action_lst = []
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.position[row][col] == self.empty_square:
                    action_lst.append(self.make_move(col, row))
        return action_lst

    def game_loop(self):
        # print("This is initial board state:", board)
        # mcts = MCTS()
        while True:
            user_input = input(">")
            if user_input == "exit":
                break
            if user_input == "":
                continue
            try:
                row = int(user_input.split(",")[1]) - 1
                col = int(user_input.split(",")[0]) - 1

                if self.position[row][col] != self.empty_square:
                    print("Illegal move")
                    continue

                self = self.make_move(col, row)

                # best_move = mcts.search(self)
                # print("best_move:", best_move.board.position)
                # print(best_move.parent.board)
                self = best_move.board
                print(self)

                if self.is_win():
                    print("Player '%s' has won the game!\n" % self.player2)
                    break
                elif self.is_draw():
                    print("Game is drawn")
                    break

            except Exception as e:
                print("Error:", e)
                print("Illegal command")

    def __str__(self) -> str:
        board_str = ""
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                board_str += "%s" % self.position[row][col]
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

    def check_winner(self):
        if self.is_win():
            return True
        if self.is_draw():
            return "tie"

    def is_valid_position(self, x, y):
        # Check if the position (x, y) is within the bounds of the board.
        return 0 <= x < NUM_LINES and 0 <= y < NUM_LINES

    def find_single_threes(self, x, y, player):
        print("x and y", x, y, player)
        # Right, Down, Diagonal Right-Down, Diagonal Right-Up
        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
        ]
        single_threes = []

        for dx, dy in directions:
            count = 0
            empty_count = 0
            # possible_single_three = False

            for i in range(-3, 4):  # Check a window of 7 cells around (x, y)
                new_x, new_y = x + i * dx, y + i * dy
                # print("new_x, new_y", new_x, new_y)
                if self.is_valid_position(new_x, new_y):
                    if self.get_value(new_x, new_y) == player:
                        count += 1
                        if empty_count > 0:
                            possible_single_three = True
                    elif self.get_value(new_x, new_y) == self.empty_square:
                        empty_count += 1
                    else:
                        count = 0
                        empty_count = 0
                    if count == 3:
                        print("new_x, new_y, empty_count", new_x, new_y, empty_count)
                    if (
                        count == 3
                        and (empty_count == 1 or empty_count == 2)
                        and possible_single_three == True
                    ):
                        print(empty_count)
                        single_threes.append(
                            [(x, y), (x + 3 * dx, y + 3 * dy), player]
                        )  # Store the start and end of the single three

        print(count)
        return single_threes


if __name__ == "__main__":
    board = Board()

    # mcts = MCTS()
    """
    score = mcts.rollout(board)
    print("score:", score)
    while True:
        best_move = mcts.search(board)
        board = best_move.board
        print(board)
        input()
    """
    board.game_loop()
