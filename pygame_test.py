import pygame
import sys

# Define the constant display size
width = 461
height = 459

# Specify the starting position for the grid
grid_start_x = 22  # Adjust this value to position the grid as needed
grid_start_y = 21  # Adjust this value to position the grid as needed

# Define the number of lines (which determines grid size)
num_lines = 19  # Adjust this value to change the number of lines in the grid

# Calculate the cell size based on the specified starting and ending positions
cell_size = min((width - grid_start_x), (height - grid_start_y)) // num_lines


pygame.init()
screen = pygame.display.set_mode((width, height))

# Load your grid image
bg = pygame.image.load("baduk_board.png")

# Define a red color for the dots
red = (255, 0, 0)

# Create a grid data structure (a list of lists) to represent the intersections
grid = [[0] * num_lines for _ in range(num_lines)]

run = True
while run:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get the current mouse cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the grid coordinates for the cursor position with offset
    mouse_x -= grid_start_x
    mouse_y -= grid_start_y

    # Ensure the cursor position is within the grid area
    if (
        0 <= mouse_x < cell_size * num_lines
        and 0 <= mouse_y < cell_size * num_lines
        and mouse_x <= width - grid_start_x
        and mouse_y <= height - grid_start_y
    ):
        grid_x = mouse_x // cell_size
        grid_y = mouse_y // cell_size

        # Display a red dot at the intersection if the cursor is inside the grid
        pygame.draw.circle(
            screen,
            red,
            (
                grid_x * cell_size + grid_start_x + cell_size // 2,
                grid_y * cell_size + grid_start_y + cell_size // 2,
            ),
            5,
        )

    pygame.display.update()

pygame.quit()
sys.exit()
