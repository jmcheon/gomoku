import copy
import itertools
import time

import numpy as np

from Board import Board
from config import *


class DQN:
    def __init__(self, model, target_model):
        if not all(isinstance(model, NeuralNet) for model in [model, target_model]):
            print(model, target_model)
            raise ValueError(f"Invalid model for DQN.")
        self.model = model
        self.target_model = target_model
        self.replay_buffer = []  # For storing (state, action, reward, next_state)

    def get_state_representation(self, board):
        # print(f"TEST::state representation: {board.position}")
        return np.array(board.get_position())

    def get_q_values(self, state):
        return self.model.forward(self.get_state_representation(state))
