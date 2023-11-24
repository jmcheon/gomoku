from src.interface.controller.game_controller import GameController
from src.algo.conv import create_CNN_model, create_mini_CNN_model
from src.algo.mcts import MCTS
from config import *
from src.game.board import Board
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gomoku game with optional debug mode."
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    if args.debug == True:
        game = GameController(SCREEN_WIDTH, SCREEN_HEIGHT, None)
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

        game = GameController(SCREEN_WIDTH, SCREEN_HEIGHT, model)
        game.init_game()
        while game.running == True:
            game.run()
