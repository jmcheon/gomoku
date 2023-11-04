# Constants
import math

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
NUM_LINES = 19
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = BLACK
BACKGROUND_COLOR = WHITE
PLAYER_1 = 1
PLAYER_2 = 2

GRID_START_X = (5 * SCREEN_WIDTH / 8) / 10
GRID_START_Y = SCREEN_HEIGHT / 10

GRID_END_X = GRID_START_X + SCREEN_WIDTH // 2
GRID_END_Y = GRID_START_Y + SCREEN_HEIGHT // 1.25

CELL_SIZE_X = (SCREEN_WIDTH // 2) / NUM_LINES
CELL_SIZE_Y = (SCREEN_HEIGHT // 1.25) / NUM_LINES


black = (0, 0, 0)
black_transparent = pygame.Color(0, 0, 0, 128)

white = (0, 0, 0)
white_transparent = pygame.Color(0, 0, 0, 128)

right_pane_begin_x = 5 * SCREEN_WIDTH / 8
right_pane_begin_y = 0
right_pane_width = 3 * SCREEN_WIDTH / 8
right_pane_height = SCREEN_HEIGHT

time_width = right_pane_width / 3
time_height = right_pane_height / 10

scorebox_width = 4 * right_pane_width / 5
scorebox_height = right_pane_height / 3

log_width = 5 * right_pane_width / 6
log_height = 4 * right_pane_height / 10
