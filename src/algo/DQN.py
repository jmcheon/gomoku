import copy
import itertools
import time

import numpy as np

from Board import Board
from config import *


class DQN:
    def __init__(self, model, target_model, epsilon=0.1, alpha=0.5, gamma=0.9):
        if not all(isinstance(model, NeuralNet) for model in [model, target_model]):
            print(model, target_model)
            raise ValueError(f"Invalid model for DQN.")
        self.model = model
        self.target_model = target_model
        self.replay_buffer = []  # For storing (state, action, reward, next_state)
        self.epsilon = epsilon  # exploration rate
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor

    def get_state_representation(self, board):
        # print(f"TEST::state representation: {board.position}")
        return np.array(board.get_position())

    def get_possible_actions(self, board):
        pass

    def get_q_values(self, state):
        return self.model.forward(self.get_state_representation(state))

    def update(self, batch):
        # Update Neural Network based on a batch of experiences
        # This involves calculating the Q-values for the current and next states, and updating the weights based on the TD error
        states, actions, rewards, next_states = zip(*batch)

        states = np.array(states)
        next_states = np.array(next_states)
        rewards = np.array(rewards)
        actions = np.array(actions)

        current_qs = self.model.predict(states)
        next_qs = self.target_model.predict(next_states)

        # Using Q-Learning
        max_next_qs = np.max(next_qs, axis=1)
        target_qs = rewards + self.gamma * max_next_qs

        # Update the Q value for the given action to the target Q value
        current_qs[np.arange(len(current_qs)), actions] = target_qs

        # Train the model on the states and updated Q values
        self.model.train_on_batch(states, current_qs)

    def train(self):
        for episode in range(NUM_EPISODES):
            board = Board()
            done = False
            while not done:
                state = self.get_state_representation(board)
                action = self.select_action(state)
                reward, next_state, done = self.step(action)
                self.replay_buffer.append((state, action, reward, next_state))
                if len(self.replay_buffer) > BATCH_SIZE:
                    batch = random.sample(self.replay_buffer, BATCH_SIZE)
                    self.update(batch)
                if episode % UPDATE_FREQ == 0:
                    self.target_model = deepcopy(self.model)
