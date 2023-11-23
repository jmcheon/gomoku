from src.algo.conv import create_CNN_model, create_mini_CNN_model
from src.algo.mcts import MCTS
from src.config import *
from src.game.board import Board
from src.game.game_logic import GameLogic
from src.interface.game_interface import GameInterface
import argparse


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

    def init_debug(self):
        self.interface = GameInterface(self.width, self.height, self.model)
        # game_option = self.interface.new()
        self.game_logic = GameLogic()
        self.game_logic.set_config("debug")
        self.interface.set_game_logic(self.game_logic)
        self.interface.mode = "debug"

    def run(self):
        while self.interface.running:
            self.interface.run()
            # Check for a reset condition (e.g., a key press 'R')
            if self.interface.reset_requested:
                self.interface.reset_requested = False  # Reset the flag
                self.init_game()  # Go back to the main menu

    def run_debug(self):
        while self.interface.running:
            self.interface.run_debug()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gomoku game with optional debug mode."
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    if args.debug == True:
        game = Gomoku(SCREEN_WIDTH, SCREEN_HEIGHT, None)
        game.init_debug()
        game.run_debug()

    else:
        if NUM_LINES == 19:
            model = create_CNN_model()
        elif NUM_LINES == 9:
            model = create_mini_CNN_model()
        else:
            raise ValueError(
                f"Unsupported board size: {NUM_LINES}, choose either 19 or 9."
            )

        game = Gomoku(SCREEN_WIDTH, SCREEN_HEIGHT, model)
        game.init_game()
        game.run()
