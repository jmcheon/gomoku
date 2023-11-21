from copy import deepcopy

import numpy as np
from src.config import *


class Board:
    def __init__(self, board=None) -> None:
        # define board position
        self.position = [[EMPTY_SQUARE] * NUM_LINES for _ in range(NUM_LINES)]

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

    def create_board_state(self, player_turn):
        """
        Args:
            board_position: a list of lists (square matrix)
        Returns:
            board_state: as a numpy.array refined, a matrix of dimension n x n
        """
        board_state = [
            [1 if i == player_turn else i for i in row] for row in self.position
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
