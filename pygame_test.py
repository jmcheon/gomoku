import pygame
import sys

# Define the constant display size
WIDTH = 461
HEIGHT = 459

# Specify the starting position for the grid
grid_start_x = 22  # Adjust this value to position the grid as needed
grid_start_y = 21  # Adjust this value to position the grid as needed

# Define the number of lines (which determines grid size)
num_lines = 19  # Adjust this value to change the number of lines in the grid

# Calculate the cell size based on the specified starting and ending positions
cell_size = min((WIDTH - grid_start_x), (HEIGHT - grid_start_y)) // num_lines

# for debug
# print(
#     cell_size,
#     WIDTH - grid_start_x,
#     WIDTH - grid_start_x,
#     HEIGHT - grid_start_y,
#     WIDTH - grid_start_x // num_lines,
#     HEIGHT - grid_start_y // num_lines,
# )

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Load your grid image
bg = pygame.image.load("baduk_board.png")

# Define a red color for the dots
red = (255, 0, 0)
red_transparent = pygame.Color(255, 0, 0, 128)

blue = (0, 0, 255)
blue_transparent = pygame.Color(0, 0, 255, 128)

# Create a grid data structure (a list of lists) to represent the intersections
grid = [[0] * num_lines for _ in range(num_lines)]

run = True


def anchor_cursor(grid_x, grid_y, turn):
    # Display a red dot at the intersection if the cursor is inside the grid
    if turn == 1:
        pygame.draw.circle(
            surface,
            red_transparent,
            (
                grid_x * cell_size + grid_start_x + cell_size // 2,
                grid_y * cell_size + grid_start_y + cell_size // 2,
            ),
            5,
        )
    elif turn == 2:
        pygame.draw.circle(
            surface,
            blue_transparent,
            (
                grid_x * cell_size + grid_start_x + cell_size // 2,
                grid_y * cell_size + grid_start_y + cell_size // 2,
            ),
            5,
        )


def draw_circles(grid_x, grid_y):
    for x in range(num_lines):
        for y in range(num_lines):
            if grid[x][y] == 1:
                # Display a red dot at the intersection if it's marked as occupied
                pygame.draw.circle(
                    screen,
                    red,
                    (
                        x * cell_size + grid_start_x + cell_size // 2,
                        y * cell_size + grid_start_y + cell_size // 2,
                    ),
                    5,
                )
            elif grid[x][y] == 2:
                # Display a red dot at the intersection if it's marked as occupied
                pygame.draw.circle(
                    screen,
                    blue,
                    (
                        x * cell_size + grid_start_x + cell_size // 2,
                        y * cell_size + grid_start_y + cell_size // 2,
                    ),
                    5,
                )


# initalize red as a beginning
turn = 1
grid_x, grid_y = 0, 0
trace = []
while run:
    screen.blit(bg, (0, 0))
    screen.blit(surface, (0, 0))

    # Get the current mouse cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the grid coordinates for the cursor position with offset
    mouse_x -= grid_start_x
    mouse_y -= grid_start_y
    if (
        0 <= mouse_x < cell_size * num_lines
        and 0 <= mouse_y < cell_size * num_lines
        and mouse_x <= WIDTH - grid_start_x
        and mouse_y <= HEIGHT - grid_start_y
    ):
        grid_x = mouse_x // cell_size
        grid_y = mouse_y // cell_size

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Ensure the cursor position is within the grid area
                if grid[grid_x][grid_y] != 0:
                    print("this cell is already occupied")
                else:
                    grid[grid_x][grid_y] = turn
                    turn = 3 - turn
                    trace.append((grid_x, grid_y))
            elif event.button == 3:
                if len(trace) > 0:
                    x, y = trace.pop()
                    if grid[x][y] != 0:
                        grid[x][y] = 0
                        turn = 3 - turn
                    print("right click:", x, y)

    surface.fill((0, 0, 0, 0))

    anchor_cursor(grid_x, grid_y, turn)
    draw_circles(grid_x, grid_y)
    pygame.display.update()

pygame.quit()
sys.exit()
