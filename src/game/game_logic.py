from src.config import *
from src.game.board import Board


class GameLogic:
    def __init__(self):
        self.board = Board()
        # TODO: integrate with Board
        self.captured_p1 = 0
        self.captured_p2 = 0
        # TODO: integrate with Board
        self.trace = []
