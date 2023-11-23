from src.algo.conv import create_CNN_model, create_mini_CNN_model
from src.algo.mcts import MCTS
from src.config import *
from src.game.board import Board
from src.game.game_logic import GameLogic
from src.interface.game_interface import GameInterface


class Gomoku:
    def __init__(self, width, height, model):
        pygame.init()
        self.model = model
        self.width = width
        self.height = height
        self.interface = None
        self.game_logic = None

    def init_game(self):
        self.interface = GameInterface(self.width, self.height, self.model)
        # TODO: load option configuration values and pass to self.game_logic
        game_option = self.interface.new()
        self.game_logic = GameLogic()
        self.game_logic.set_config(game_option)
        self.interface.set_game_logic(self.game_logic)

    def run(self):
        while self.interface.running:
            self.interface.run()
            # Check for a reset condition (e.g., a key press 'R')
            if self.interface.reset_requested:
                self.interface.reset_requested = False  # Reset the flag
                self.init_game()  # Go back to the main menu


if __name__ == "__main__":
    if NUM_LINES == 19:
        model = create_CNN_model()
    elif NUM_LINES == 9:
        model = create_mini_CNN_model()
    else:
        raise ValueError(f"Unsupported board size: {NUM_LINES}, choose either 19 or 9.")
    game = Gomoku(SCREEN_WIDTH, SCREEN_HEIGHT, model)
    game.init_game()
    game.run()
