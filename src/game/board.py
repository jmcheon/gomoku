from copy import deepcopy

import numpy as np
from src.config import *


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

    def is_empty_square(self, x, y):
        return self.get_value(x, y) == EMPTY_SQUARE

    def is_draw(self) -> bool:
        # loop over board square
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.is_empty_square(col, row):
                    return False
        return True

    def is_win(self) -> bool:
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

        return board, (row, col)

    # generate legal moves to play in the current position
    def generate_states(self) -> list:
        # define states list (move list - list of available actions to consider)
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
