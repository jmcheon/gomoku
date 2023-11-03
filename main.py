from src.game.game_logic import GameLogic
from src.interface.game_interface import GameInterface
from src.config import *


class Gomoku:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.interface = None
        self.game_logic = None

    def init_game(self):
        self.interface = GameInterface(self.width, self.height)
        self.game_logic = GameLogic()
        # TODO: load option configuration values and pass to self.game_logic
        self.interface.new()
        self.interface.set_game_logic(self.game_logic)

    def run(self):
        while self.interface.running:
            self.interface.run()
            # Check for a reset condition (e.g., a key press 'R')
            if self.interface.reset_requested:
                self.interface.reset_requested = False  # Reset the flag
                self.init_game()  # Go back to the main menu

def create_model():
    model = NeuralNet()
    model.create_network(
        [
            DenseLayer(INPUT_SHAPE, 200, activation="ReLU"),
            DenseLayer(200, 100, activation="ReLU", weights_initializer="zero"),
            DenseLayer(100, 50, activation="ReLU", weights_initializer="zero"),
            DenseLayer(
                50, OUTPUT_SHAPE, activation="softmax", weights_initializer="zero"
            ),
        ]
    )
    return model


if __name__ == "__main__":
    game = Gomoku(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.init_game()
    game.run()

    model = create_model()
    target_model = create_model()
    dqn = DQN(model, target_model)

    # print(dqn.get_state_representation(gomoku.board))
