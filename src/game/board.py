from copy import deepcopy

import numpy as np
from src.config import *


class TextColors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


def print_colored_text(text, color_code):
    if color_code.upper() in dir(TextColors):
        color = getattr(TextColors, color_code.upper())
        print(f"{color}{text}{TextColors.RESET}")
    else:
        print(text)


class Board:
    def __init__(self, board=None) -> None:
        # define board position
        self.position = [[EMPTY_SQUARE] * NUM_LINES for _ in range(NUM_LINES)]
        self.turn = PLAYER_1

        # create a copy of previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def get_position(self) -> list:
        return deepcopy(self.position)

    def get_value(self, col: int, row: int) -> str:
        return self.position[row][col]

    def set_value(self, col: int, row: int, value: str) -> str:
        self.position[row][col] = value
        return value

    def get_horizontal_list(self, row):
        lst = []
        for col in range(NUM_LINES):
            lst.append((col, row))
        return lst

    def is_empty_square(self, x, y):
        return self.get_value(x, y) == EMPTY_SQUARE

    def is_draw(self) -> bool:
        # loop over board square
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.is_empty_square(col, row):
                    return False
        return True

    def check_vertical_sequence(self, y, x):
        count = 0
        for i in range(6):
            if y + i < NUM_LINES and self.get_value(x, y + i) == self.turn:
                count += 1
                if count >= 5:
                    return True
            else:
                break
        for i in range(1, 5):
            if y - i >= 0 and self.get_value(x, y - i) == self.turn:
                count += 1
                if count >= 5:
                    return True
            else:
                break
        return False

    def check_horizontal_sequence(self, x, y):
        count = 0
        print("current move: ", x, y)
        """
        0 1 2 3 4 5 - 18
        -4 0 4
        for i in range(-4, 5):
            if x + i >= 0 and self.get_value(x + i, y) == self.turn:
                print("checking: ", x + i, y)
                count += 1
                if count >= 5:
                    print("true count: ", count)
                    return True
            else:
                count = 0
                """
        for i in range(6):
            if x - i >= 0 and self.get_value(x - i, y) == self.turn:
                print("checking backward: ", x - i, y)
                count += 1
                if count >= 5:
                    print("true count: ", count)
                    return True
            else:
                break
        for i in range(1, 5):
            if x + i < NUM_LINES and self.get_value(x + i, y) == self.turn:
                print("checking forward: ", x + i, y)
                count += 1
                if count >= 5:
                    print("true count: ", count)
                    return True
            else:
                break
        print("false count: ", count)
        return False

    def check_1st_diagonal_sequence(self, y, x):
        count = 0
        print_colored_text(f"current move: {x} {y}", "blue")
        for i in range(6):
            if x - i >= 0 and y - i >= 0 and self.get_value(x - i, y - i) == self.turn:
                print("checking 1st diagonal backward: ", x - i, y - i)
                count += 1
                if count >= 5:
                    print("true 1st diagonal count: ", count)
                    return True
            else:
                break
        for i in range(1, 5):
            if (
                x + i < NUM_LINES
                and y + i < NUM_LINES
                and self.get_value(x + i, y + i) == self.turn
            ):
                print("checking 1st diagonal forward: ", x + i, y + i)
                count += 1
                if count >= 5:
                    print("true 1st diagonal count: ", count)
                    return True
            else:
                break
        print("false 1st diagonal count: ", count)
        return False

    def check_2nd_diagonal_sequence(self, y, x):
        count = 0
        for i in range(6):
            if (
                x - i >= 0
                and y + i < NUM_LINES
                and self.get_value(x - i, y + i) == self.turn
            ):
                count += 1
                if count >= 5:
                    return True
            else:
                break
        for i in range(1, 5):
            if (
                x + i < NUM_LINES
                and y - i >= 0
                and self.get_value(x + i, y - i) == self.turn
            ):
                count += 1
                if count >= 5:
                    return True
            else:
                break
        return False

    def is_win(self) -> bool:
        # vertical sequence detection
        for col in range(NUM_LINES):
            for row in range(NUM_LINES):
                if self.get_value(col, row) == self.turn:
                    if self.check_vertical_sequence(col, row):
                        print_colored_text(
                            "vertical sequence detection: True", "yellow"
                        )
                        return True
        # horizontal sequence detection
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                # print("horizontal sequence detection: ", self.position[row])
                if self.get_value(col, row) == self.turn:
                    if self.check_horizontal_sequence(col, row):
                        print_colored_text(
                            "horizontal sequence detection: True", "yellow"
                        )
                        return True
        # 1st diagonal sequence detection
        for row in range(NUM_LINES):
            col = row
            if self.get_value(col, row) == self.turn:
                if self.check_1st_diagonal_sequence(col, row):
                    print_colored_text(
                        "1st diagonal sequence detection: True", "yellow"
                    )
                    return True
        # 2nd diagonal sequence detection
        for row in range(NUM_LINES):
            col = NUM_LINES - row - 1
            if self.get_value(col, row) == self.turn:
                if self.check_2nd_diagonal_sequence(col, row):
                    print_colored_text(
                        "2nd diagonal sequence detection: True", "yellow"
                    )
                    return True
        return False

    def is_win2(self) -> bool:
        # vertical sequence detection
        for col in range(NUM_LINES):
            winning_sequence = []
            for row in range(NUM_LINES):
                if self.get_value(col, row) == self.turn:
                    winning_sequence.append((row, col))
                if len(winning_sequence) >= 5:
                    return True
        # horizontal sequence detection
        for row in range(NUM_LINES):
            winning_sequence = []
            for col in range(NUM_LINES):
                if self.get_value(col, row) == self.turn:
                    winning_sequence.append((row, col))
                if len(winning_sequence) >= 5:
                    return True
        # 1st diagonal sequence detection
        winning_sequence = []
        for row in range(NUM_LINES):
            col = row
            if self.get_value(col, row) == self.turn:
                winning_sequence.append((row, col))
            if len(winning_sequence) >= 5:
                return True
        # 2nd diagonal sequence detection
        winning_sequence = []
        for row in range(NUM_LINES):
            col = NUM_LINES - row - 1
            if self.get_value(col, row) == self.turn:
                winning_sequence.append((row, col))
            if len(winning_sequence) >= 5:
                return True
        return False

    def make_move(self, col: int, row: int) -> object:
        # create new board instance that inherits from the current state
        board = Board(self)

        # make move
        board.position[row][col] = self.turn

        return board, (col, row)

    # generate legal moves to play in the current position
    def generate_states(self) -> list:
        # define states list (move list - list of available actions to consider)
        # print("board before generating states:\n", self)
        states_lst = []
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.position[row][col] == EMPTY_SQUARE:
                    new_board, action = self.make_move(col, row)
                    states_lst.append((new_board, action))
        return states_lst

    def create_board_state(self, player_turn):
        """
        Args:
            board_position: a list of lists (square matrix)
        Returns:
            board_state: as a numpy.array refined, a matrix of dimension n x n
        """
        board_state = [
            [1 if i == player_turn else 0 for i in row] for row in self.position
        ]

        return np.array(board_state)

    def __str__(self) -> str:
        board_str = ""
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                board_str += "%s" % self.position[row][col]
            board_str += "\n"
        """
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
        """
        return board_str
