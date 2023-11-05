from src.interface.game_interface import GameInterface
from src.config import *

if __name__ == "__main__":
    game = GameInterface(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.new()
    game.run()
