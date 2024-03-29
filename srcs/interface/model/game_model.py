from config import *
from srcs.game.board import Board, print_colored_text
from srcs.game.capture import capture_opponent, remove_captured_list
from srcs.game.doublethree import check_double_three
from srcs.game.Player import Player


class GameModel:
    def __init__(self):
        self.board = Board()
        self.player1 = Player(PLAYER_1)
        self.player2 = Player(PLAYER_2)
        self.record_count = 1
        # TODO: integrate with Board
        self.record = []
        # TODO: integrate with Board
        self.trace = []
        self.game_data = []

    # TODO: keep this, or move this into initializer if needed
    def set_config(self, options):
        self.options = options
        print(options)

    def is_draw(self) -> bool:
        # loop over board square
        for row in range(NUM_LINES):
            for col in range(NUM_LINES):
                if self.board.is_empty_square(col, row):
                    return False
        return True

    def make_move(self, col: int, row: int) -> object:
        # create new board instance that inherits from the current state
        board = Board(self.board)

        # make move
        board.position[row][col] = self.board.turn

        return board, (col, row)

    def place_stone(self, x, y, captured_list=None):
        print(f"x: {x}, y: {y}")
        self.board, action = self.make_move(x, y)
        self.record_trace(x, y)
        # self.trace.append(self.game_logic.board)
        if captured_list is not None:
            remove_captured_list(self.board, captured_list)
        # self.change_player_turn()
        self.game_data.append((self.board, action))

    def record_trace(self, x, y):
        self.record.append(((x, y), self.board.turn, self.record_count))
        self.record_count += 1
        self.trace.append(self.board)

    def undo_last_move(self):
        if self.trace:  # Checks if the trace list is not empty
            self.trace.pop()
            self.record.pop()
            if self.trace:
                self.board = self.trace[-1]
            else:
                self.board.position = [["."] * NUM_LINES for _ in range(NUM_LINES)]
            return True
        else:
            return False

    def change_player_turn(self):
        self.board.turn = PLAYER_2 if self.board.turn == PLAYER_1 else PLAYER_1

    def check_doublethree(self, x, y):
        return check_double_three(self.board, x, y, self.board.turn)

    def capture_opponent(self, x, y):
        return capture_opponent(self.board, x, y, self.board.turn)
