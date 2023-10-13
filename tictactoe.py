import pygame
import sys
import math

from minmax import best_move, check_winner

# Define the constant display size
WIDTH = 640
HEIGHT = 480

# Specify the starting position for the grid
grid_start_x = 20  # Adjust this value to position the grid as needed
grid_start_y = 20  # Adjust this value to position the grid as needed

grid_end_x = 620  # Adjust this value to position the grid as needed
grid_end_y = 460  # Adjust this value to position the grid as needed

# Define the number of lines (which determines grid size)
num_lines = 3  # Adjust this value to change the number of lines in the grid

# Calculate the cell size based on the specified starting and ending positions
cell_size_x = math.ceil((grid_end_x - grid_start_x) / num_lines)
cell_size_y = math.ceil((grid_end_y - grid_start_y) / num_lines)

# print(cell_size_x, cell_size_y)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Load your grid image
bg = pygame.image.load("baduk_board.png")
bg.set_colorkey((230, 230, 230))


# Define a red color for the dots
red = (255, 0, 0)
red_transparent = pygame.Color(255, 0, 0, 128)

blue = (0, 0, 255)
blue_transparent = pygame.Color(0, 0, 255, 128)

black = (0, 0, 0)
black_transparent = pygame.Color(0, 0, 0, 128)

white = (255, 255, 255)
white_transparent = pygame.Color(255, 255, 255, 128)

# Create a grid data structure (a list of lists) to represent the intersections
board = [[0] * num_lines for _ in range(num_lines)]
run = True


def draw_circles(x, y, target, color):
    initial_size = 10  # Adjust as needed
    max_lines = 50  # Adjust as needed
    size_increase = 1  # Adjust as needed

    circle_size = initial_size + (max_lines - num_lines) * size_increase
    # print(x, y, grid_x, grid_y)
    pygame.draw.circle(
        target,
        color,
        (
            x * cell_size_x + grid_start_x + cell_size_x // 2,
            y * cell_size_y + grid_start_y + cell_size_y // 2,
        ),
        circle_size,
    )


# initalize red as a beginning
turn = 1
grid_x, grid_y = 0, 0
trace = []
while run:
    screen.fill((200, 200, 200, 128))
    screen.blit(surface, (0, 0))

    # Get the current mouse cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the grid coordinates for the cursor position with offset
    mouse_x -= grid_start_x
    mouse_y -= grid_start_y
    if (
        0 <= mouse_x < cell_size_x * num_lines
        and 0 <= mouse_y < cell_size_y * num_lines
        and mouse_x <= WIDTH - grid_start_x
        and mouse_y <= HEIGHT - grid_start_y
    ):
        grid_x = mouse_x // cell_size_x
        grid_y = mouse_y // cell_size_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Ensure the cursor position is within the grid area
                if board[grid_x][grid_y] != 0:
                    print("this cell is already occupied")
                else:
                    board[grid_x][grid_y] = turn
                    turn = 3 - turn
                    trace.append((grid_x, grid_y))
            elif event.button == 3:
                if len(trace) > 0:
                    x, y = trace.pop()
                    if board[x][y] != 0:
                        board[x][y] = 0
                        turn = 3 - turn
                        best_move(board)
                    print("right click:", x, y)

    surface.fill((0, 0, 0, 0))

    if turn == 1:
        draw_circles(grid_x, grid_y, surface, black_transparent)
    elif turn == 2:
        best_move(board)
        turn = 1

    for x in range(num_lines):
        for y in range(num_lines):
            if board[x][y] == 1:
                draw_circles(x, y, screen, black)
            elif board[x][y] == 2:
                draw_circles(x, y, screen, white)

    winner = check_winner(board)
    if winner is not None:
        print(f"Player {winner} wins!")
        winner = None
        break

    pygame.display.update()

pygame.quit()
sys.exit()
