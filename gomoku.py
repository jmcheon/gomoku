import math
import sys

import pygame

from Board import Board
from config import *
from mcts import *
from minmax import best_move, check_winner

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Load your grid image
bg = pygame.image.load("baduk_board.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg.set_colorkey((230, 230, 230))


# Create a grid data structure (a list of lists) to represent the intersections
board = Board()  # [[0] * NUM_LINES for _ in range(NUM_LINES)]

print(CELL_SIZE_X, CELL_SIZE_Y)


def draw_circles(x, y, target, color):
    initial_size = 10  # Adjust as needed
    max_lines = 20  # Adjust as needed
    size_increase = 1  # Adjust as needed

    circle_size = initial_size + (max_lines - NUM_LINES) * size_increase
    # print(x, y, grid_x, grid_y)
    pygame.draw.circle(
        target,
        color,
        (
            x * CELL_SIZE_X + GRID_START_X + CELL_SIZE_X // 2,
            y * CELL_SIZE_Y + GRID_START_Y + CELL_SIZE_Y // 2,
        ),
        circle_size,
    )


def best_move(board):
    mcts = MCTS()
    best_move = mcts.search(board)
    board = best_move.board
    print(board)
    return board


# initalize red as a beginning
turn = PLAYER1
grid_x, grid_y = 0, 0
trace = []
run = True
while run:
    # screen.fill((200, 200, 200, 128))
    screen.blit(bg, (0, 0))
    screen.blit(surface, (0, 0))

    # Get the current mouse cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the grid coordinates for the cursor position with offset
    mouse_x -= GRID_START_X
    mouse_y -= GRID_START_Y
    if (
        0 <= mouse_x < CELL_SIZE_X * NUM_LINES
        and 0 <= mouse_y < CELL_SIZE_Y * NUM_LINES
        and mouse_x <= WIDTH - GRID_START_X
        and mouse_y <= HEIGHT - GRID_START_Y
    ):
        grid_x = mouse_x // CELL_SIZE_X
        grid_y = mouse_y // CELL_SIZE_Y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Ensure the cursor position is within the grid area
                if board.position[grid_y][grid_x] != board.empty_square:
                    print("this cell is already occupied")
                else:
                    # board[grid_x][grid_y] = turn
                    board = board.make_move(grid_y, grid_x)
                    print(board)
                    board.swap_player()
                    turn = PLAYER1 if turn == PLAYER2 else PLAYER2
                    trace.append((grid_x, grid_y))

            # revert with right click
            elif event.button == 3:
                if len(trace) > 0:
                    # if board.position[grid_y][grid_x] != board.empty_square:
                    x, y = trace.pop()
                    board.position[y][x] = board.empty_square
                    board.swap_player()
                    turn = PLAYER1 if turn == PLAYER2 else PLAYER2
                    print("right click:", x, y, turn)

    surface.fill((0, 0, 0, 0))

    if board.is_win():
        print("Player '%s' has won the game!\n" % board.player2)
        break
    elif board.is_draw():
        print("Game is drawn")
        break

    if turn == PLAYER1:
        draw_circles(grid_x, grid_y, surface, black_transparent)
    elif turn == PLAYER2:
        draw_circles(grid_x, grid_y, surface, white_transparent)
        # board = best_move(board)

    for x in range(NUM_LINES):
        for y in range(NUM_LINES):
            if board.position[y][x] == "X":
                draw_circles(x, y, screen, black)
            elif board.position[y][x] == "O":
                draw_circles(x, y, screen, white)

    pygame.display.update()
