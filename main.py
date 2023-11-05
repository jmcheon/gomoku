from src.game.game_logic import GameLogic
from src.interface.game_interface import GameInterface
from src.config import *


class Gomoku:
    def __init__(self, width, height):
        pygame.init()
        self.game_logic = GameLogic()
        self.interface = GameInterface(width, height)
        # self.ui_handling = U

    def main_menu(self):
        # waiting = True
        self.interface.new()
        self.interface.set_game_logic(self.game_logic)

    def run(self):
        while self.interface.running:
            self.interface.run()
            # Handle events
            # Update game logic
            # Update UI elements
            # Draw the screen
            # pass


if __name__ == "__main__":
    game = Gomoku(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.main_menu()
    game.run()
