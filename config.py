import math

# Define the constant display size
WIDTH = 640
HEIGHT = 480
PLAYER1 = "X"
PLAYER2 = "O"

# Specify the starting position for the grid
GRID_START_X = 20  # Adjust this value to position the grid as needed
GRID_START_Y = 20  # Adjust this value to position the grid as needed

GRID_END_X = 620  # Adjust this value to position the grid as needed
GRID_END_Y = 460  # Adjust this value to position the grid as needed

# Define the number of lines (which determines grid size)
NUM_LINES = 5  # Adjust this value to change the number of lines in the grid

# Calculate the cell size based on the specified starting and ending positions
CELL_SIZE_X = math.ceil((GRID_END_X - GRID_START_X) / NUM_LINES)
CELL_SIZE_Y = math.ceil((GRID_END_Y - GRID_START_Y) / NUM_LINES)
