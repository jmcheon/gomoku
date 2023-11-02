import math
import sys

import pygame

from Board import Board
from capture import capture_opponent, remove_captured_list
from config import *
from doublethree import check_double_three
from mcts import MCTS
from minmax import best_move, check_winner
from QLearningAgent import QLearningAgent


class Gomoku:
    def __init__(self):
        self.board = Board()
        self.mcts = MCTS(None)
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Load your grid image
        self.bg = pygame.image.load("baduk_board.png")
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.bg.set_colorkey((230, 230, 230))
        print(CELL_SIZE_X, CELL_SIZE_Y)

    def draw_circles(self, x, y, target, color):
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

    def best_move(self, board):
        best_move = self.mcts.search(board)
        board = best_move.board
        print(board)
        return board

    def play(self):
        # initalize red as a beginning
        turn = self.board.player1
        grid_x, grid_y = 0, 0
        trace = []
        run = True
        while run:
            # screen.fill((200, 200, 200, 128))
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.surface, (0, 0))

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
                        if (
                            self.board.get_value(grid_x, grid_y)
                            != self.board.empty_square
                        ):
                            print("this cell is already occupied")
                        else:
                            self.board = self.board.make_move(grid_x, grid_y)
                            if self.board.is_win() == False:
                                print("Wtf")
                            elif self.board.is_draw():
                                print("Game is drawn")
                                break
                            # self.board[grid_x][grid_y] = turn
                            capture_list = capture_opponent(
                                self.board, grid_x, grid_y, turn
                            )
                            if capture_list:
                                remove_captured_list(self.board, capture_list)
                            check_double_three(self.board, grid_x, grid_y, turn)
                            # turn = PLAYER1 if turn == PLAYER2 else PLAYER2
                            trace.append(self.board.position)

                    # revert with right click
                    elif event.button == 3:
                        # print("trace enabled")
                        if trace:  # Checks if the trace list is not empty
                            trace.pop()  # Remove the last item from the list
                            if trace:
                                self.board.position = trace[-1]
                            else:
                                self.board.position = [
                                    ["."] * NUM_LINES for _ in range(NUM_LINES)
                                ]
                            self.board.swap_player()
                        else:
                            print("Trace is empty, cannot go back further")

            self.surface.fill((0, 0, 0, 0))

            if self.board.is_win():
                print("Player '%s' has won the game!\n" % self.board.player2)
                break
            elif self.board.is_draw():
                print("Game is drawn")
                break

            if self.board.player1 == PLAYER1:
                self.draw_circles(grid_x, grid_y, self.surface, black_transparent)
            elif self.board.player1 == PLAYER2:
                self.draw_circles(grid_x, grid_y, self.surface, white_transparent)
                # self.board = best_move(self.board)

            for x in range(NUM_LINES):
                for y in range(NUM_LINES):
                    if self.board.get_value(x, y) == "X":
                        self.draw_circles(x, y, self.screen, black)
                    elif self.board.get_value(x, y) == "O":
                        self.draw_circles(x, y, self.screen, white)

            pygame.display.update()
