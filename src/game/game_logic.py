from src.config import *
from src.game.board import Board
from src.game.capture import capture_opponent, remove_captured_list
from src.game.doublethree import check_double_three


class GameLogic:
    def __init__(self):
        self.board = Board()
        # TODO: integrate with Board
        self.turn = PLAYER_1
        self.captured_p1 = 0
        self.captured_p2 = 0
        self.record = []
        # TODO: integrate with Board
        self.trace = []

    def is_emptyspace(self, x, y):
        return self.board.get_value(x, y) == self.board.empty_square

    def is_game_drawn(self):
        return self.board.is_draw()

    def place_stone(self, x, y, captured_list=None):
        self.board = self.board.make_move(x, y)
        self.record_trace()
        # self.trace.append(self.game_logic.board)
        if captured_list is not None:
            remove_captured_list(self.board, captured_list)
        self.change_player_turn()

    def record_trace(self):
        self.trace.append(self.board)

    def undo_last_move(self):
        if self.trace:  # Checks if the trace list is not empty
            print("trace.pop", self.trace.pop())
            if self.trace:
                self.board = self.trace[-1]
            else:
                self.board.position = [["."] * NUM_LINES for _ in range(NUM_LINES)]
            return True
        else:
            return False

    def change_player_turn(self):
        self.turn = PLAYER_2 if self.turn == PLAYER_1 else PLAYER_1

    def check_doublethree(self, x, y):
        return check_double_three(self.board, x, y, self.turn)

    def capture_opponent(self, x, y):
        return capture_opponent(self.board, x, y, self.turn)
