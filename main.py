from src.game.game_logic import GameLogic
from src.interface.game_interface import GameInterface
from src.config import *


class Gomoku:
    def __init__(self, width, height):
        pygame.init()
        self.game_logic = None
        self.interface = GameInterface(width, height)
        self.reset_requested = False

    def main_menu(self):
        # waiting = True
        self.interface.new()
        self.game_logic = GameLogic()
        self.interface.set_game_logic(self.game_logic)

    def run(self):
        while self.interface.running:
            self.interface.run()
            # Check for a reset condition (e.g., a key press 'R')
            if self.interface.reset_requested:
                self.interface.reset_requested = False  # Reset the flag
                self.main_menu()  # Go back to the main menu


if __name__ == "__main__":
    game = Gomoku(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.main_menu()
    game.run()
