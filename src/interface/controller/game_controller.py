import pygame
from src.config import WHITE
from src.interface.view.game_view import GameView
from src.interface.model.game_model import GameModel

# from src.interface.game_interface import GameInterface


class GameController:
    def __init__(self, width, height, model):
        pygame.init()
        self.model = model
        self.width = width
        self.height = height
        self.view = None
        self.game_model = None

    def init_game(self):
        self.view = GameView(self.width, self.height, self.model)
        # TODO: load option configuration values and pass to self.game_logic
        game_option = self.view.new()
        self.view._initialize_game_view()
        self.game_model = GameModel()
        self.game_model.set_config(game_option)
        self.view.screen.fill(WHITE)
        # self.interface.set_game_logic(self.game_logic)

    def init_debug(self):
        self.interface = GameView(self.width, self.height, self.model)
        # game_option = self.interface.new()
        self.game_logic = GameModel()
        self.game_logic.set_config("debug")
        self.interface.set_game_logic(self.game_logic)
        self.interface.mode = "debug"

    def run(self):
        while self.view.running:
            self.view.draw()
            # Check for a reset condition (e.g., a key press 'R')
            if self.view.reset_requested:
                self.view.reset_requested = False  # Reset the flag
                self.init_game()  # Go back to the main menu

    def run_debug(self):
        while self.view.running:
            self.view.run_debug()
