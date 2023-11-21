import math
import os
import sys

import pygame

path = os.path.join(os.path.dirname(__file__), "..", "multilayer_perceptron")
sys.path.insert(1, path)
from DenseLayer import DenseLayer
from NeuralNet import NeuralNet

# Define the constant display size
# baduk_board original size is 461 x 459
WIDTH = 690
HEIGHT = 690
PLAYER1 = "X"
PLAYER2 = "O"

# Specify the starting position for the grid
GRID_START_X = 35  # Adjust this value to position the grid as needed
GRID_START_Y = 35  # Adjust this value to position the grid as needed

GRID_END_X = 680  # Adjust this value to position the grid as needed
GRID_END_Y = 680  # Adjust this value to position the grid as needed

# Define the number of lines (which determines grid size)
NUM_LINES = 5  # Adjust this value to change the number of lines in the grid

# Calculate the cell size based on the specified starting and ending positions
CELL_SIZE_X = math.ceil((GRID_END_X - GRID_START_X) / NUM_LINES)
CELL_SIZE_Y = math.ceil((GRID_END_Y - GRID_START_Y) / NUM_LINES)

# Define a red color for the dots
red = (255, 0, 0)
red_transparent = pygame.Color(255, 0, 0, 128)

blue = (0, 0, 255)
blue_transparent = pygame.Color(0, 0, 255, 128)

black = (0, 0, 0)
black_transparent = pygame.Color(0, 0, 0, 128)

white = (255, 255, 255)
white_transparent = pygame.Color(255, 255, 255, 128)


# Neural Network
INPUT_SHAPE = NUM_LINES * NUM_LINES
OUTPUT_SHAPE = NUM_LINES
NUM_EPISODES = 1000
BATCH_SIZE = 5

# path
MLP_DIR_NAME = "multilayer_perceptron"

# doublethree direction
NORTH = (0, -1)
NORTHEAST = (1, -1)
EAST = (1, 0)
SOUTHEAST = (1, 1)
SOUTH = (0, 1)
SOUTHWEST = (-1, 1)
WEST = (-1, 0)
NORTHWEST = (-1, -1)

DIRECTIONS = [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST]
