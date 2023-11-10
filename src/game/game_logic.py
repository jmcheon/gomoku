from src.config import *
from src.game.board import Board
from src.game.capture import capture_opponent, remove_captured_list
from src.game.doublethree import check_double_three
from src.game.Player import Player


class GameLogic:
    def __init__(self):
        self.board = Board()
        self.player1 = Player(PLAYER_1)
        self.player2 = Player(PLAYER_2)
        # TODO: integrate with Board
        self.turn = PLAYER_1
        self.record = []
        # TODO: integrate with Board
        self.trace = []

    # TODO: keep this, or move this into initializer if needed
    def set_config(self, options):
        print(options)

    def is_draw(self) -> bool:
        # loop over board square
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.board.is_empty_square(col, row):
                    return False
        return True

    def is_win(self) -> bool:
        # vertical sequence detection
        for col in range(NUM_LINES):
            winning_sequence = []
            for row in range(NUM_LINES):
                if self.board.get_value(col, row) == self.turn:
                    winning_sequence.append((row, col))
                if len(winning_sequence) >= 5:
                    return True
        # horizontal sequence detection
        for row in range(NUM_LINES):
            winning_sequence = []
            for col in range(NUM_LINES):
                if self.board.get_value(col, row) == self.turn:
                    winning_sequence.append((row, col))
                if len(winning_sequence) >= 5:
                    return True
        # 1st diagonal sequence detection
        winning_sequence = []
        for row in range(NUM_LINES):
            col = row
            if self.board.get_value(col, row) == self.turn:
                winning_sequence.append((row, col))
            if len(winning_sequence) >= 5:
                return True
        # 2nd diagonal sequence detection
        winning_sequence = []
        for row in range(NUM_LINES):
            col = NUM_LINES - row - 1
            if self.board.get_value(col, row) == self.turn:
                winning_sequence.append((row, col))
            if len(winning_sequence) >= 5:
                return True
        return False

    def make_move(self, col: int, row: int) -> object:
        # create new board instance that inherits from the current state
        board = Board(self.board)

        # make move
        board.position[row][col] = self.turn

        return board

    def place_stone(self, x, y, captured_list=None):
        self.board = self.make_move(x, y)
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
