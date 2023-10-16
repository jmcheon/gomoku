import math

# Define the constant display size
WIDTH = 640
HEIGHT = 480
PLAYER1 = "X"
PLAYER2 = "O"

# Specify the starting position for the grid
grid_start_x = 20  # Adjust this value to position the grid as needed
grid_start_y = 20  # Adjust this value to position the grid as needed

grid_end_x = 620  # Adjust this value to position the grid as needed
grid_end_y = 460  # Adjust this value to position the grid as needed

# Define the number of lines (which determines grid size)
num_lines = 5  # Adjust this value to change the number of lines in the grid

# Calculate the cell size based on the specified starting and ending positions
cell_size_x = math.ceil((grid_end_x - grid_start_x) / num_lines)
cell_size_y = math.ceil((grid_end_y - grid_start_y) / num_lines)
