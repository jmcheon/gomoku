import pygame
import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox
from Board import Board
from ui_config import *


class Interface:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.Surface((self.width, self.height))
        self.font_name = pygame.font.match_font("arial")
        # Other initializations
        self._initialize_game()
        self._initialize_ui()

    def _initialize_game(self):
        # Game-related initializations
        self.board = Board()
        self.start_x = GRID_START_X
        self.start_y = GRID_START_Y
        self.grid_width = SCREEN_WIDTH // 2
        self.grid_height = SCREEN_HEIGHT // 1.25
        self.running = True
        # Other game-related attributes

    def _initialize_ui(self):
        # UI-related initializations
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self._initialize_gameboard()
        self._initialize_right_pane()

    def _initialize_gameboard(self):
        self.board_surface = pygame.Surface(
            (5 * SCREEN_WIDTH / 8, SCREEN_HEIGHT), pygame.SRCALPHA
        )

    def _initialize_right_pane(self):
        # Right pane UI setup
        self.right_pane_rect = pygame.Rect(
            right_pane_begin_x, right_pane_begin_y, right_pane_width, right_pane_height
        )
        self._initialize_time_rect()
        self._initialize_scorebox_rect()
        self._initialize_log_rect()
        self._initialize_text_box()

    def _initialize_time_rect(self):
        # Initialize time rectangle within the right pane
        self.time_rect = pygame.Rect(
            self.right_pane_rect.centerx - time_width / 2,
            time_height / 2,
            time_width,
            time_height,
        )

    def _initialize_scorebox_rect(self):
        # Initialize time rectangle within the right pane
        self.scorebox_rect = pygame.Rect(
            self.right_pane_rect.centerx - scorebox_width / 2,
            self.time_rect.bottom,
            scorebox_width,
            scorebox_height,
        )

    def _initialize_log_rect(self):
        # Initialize time rectangle within the right pane
        self.log_rect = pygame.Rect(
            self.right_pane_rect.centerx - log_width / 2,
            self.scorebox_rect.bottom + self.right_pane_rect.height / 20,
            log_width,
            log_height,
        )

    # Other _initialize_* methods for different UI elements within the right pane

    def _initialize_text_box(self):
        # Initialize the text box
        self.text_box = UITextBox(
            html_text="<body><font color=#E0E080></font>",
            relative_rect=self.log_rect,
            manager=self.ui_manager,
        )

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_stone(self, x, y, target, color, thickness=0):
        initial_size = 6  # Adjust as needed
        max_lines = 20  # Adjust as needed
        size_increase = 1  # Adjust as needed

        circle_size = initial_size + (max_lines - NUM_LINES) * size_increase
        # print(x, y, grid_x, grid_y)

        if color == BLACK or color == BLACK_TRANSPARENT:
            pygame.draw.circle(
                target,
                color,
                (
                    x * CELL_SIZE_X + GRID_START_X + CELL_SIZE_X // 2,
                    y * CELL_SIZE_Y + GRID_START_Y + CELL_SIZE_Y // 2,
                ),
                circle_size,
            )
        elif color == WHITE or color == WHITE_TRANSPARENT:
            pygame.draw.circle(
                target,
                color,
                (
                    x * CELL_SIZE_X + GRID_START_X + CELL_SIZE_X // 2,
                    y * CELL_SIZE_Y + GRID_START_Y + CELL_SIZE_Y // 2,
                ),
                circle_size,
            )
            pygame.draw.circle(
                target,
                BLACK,
                (
                    x * CELL_SIZE_X + GRID_START_X + CELL_SIZE_X // 2,
                    y * CELL_SIZE_Y + GRID_START_Y + CELL_SIZE_Y // 2,
                ),
                circle_size,
                thickness,
            )

    def wait_for_key(self):
        waiting = True
        while waiting:
            # self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()

    def new(self):
        pygame.init()
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_text(
            "Press any key to create the grid",
            22,
            LINE_COLOR,
            self.width / 2,
            self.height / 2,
        )
        pygame.display.flip()
        self.wait_for_key()

    def _convert_mouse_to_grid(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= GRID_START_X
        mouse_y -= GRID_START_Y
        grid_x = 0
        grid_y = 0
        if (
            0 <= mouse_x < CELL_SIZE_X * NUM_LINES
            and 0 <= mouse_y < CELL_SIZE_Y * NUM_LINES
            and mouse_x <= SCREEN_WIDTH - GRID_START_X
            and mouse_y <= SCREEN_HEIGHT - GRID_START_Y
        ):
            grid_x = mouse_x // CELL_SIZE_X
            grid_y = mouse_y // CELL_SIZE_Y

        return int(grid_x), int(grid_y)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid_x, grid_y = self._convert_mouse_to_grid()
                if self.board.get_value(grid_x, grid_y) != self.board.empty_square:
                    print("this cell is already occupied")
                else:
                    self.board = self.board.make_move(grid_x, grid_y)
                    print(self.board.player_turn)
            self.ui_manager.process_events(event)

    def _anchor_mouse_stones(self):
        self.board_surface.fill(BACKGROUND_COLOR)
        grid_x, grid_y = self._convert_mouse_to_grid()

        # for anchor
        if self.board.player_turn == PLAYER_1:
            self.draw_stone(grid_x, grid_y, self.board_surface, BLACK)
        elif self.board.player_turn == PLAYER_2:
            self.draw_stone(grid_x, grid_y, self.board_surface, WHITE, 1)

    def _draw_placed_stones(self):
        # for drawing already placed dots
        for x in range(NUM_LINES):
            for y in range(NUM_LINES):
                if self.board.get_value(x, y) == "X":
                    self.draw_stone(x, y, self.screen, BLACK)
                elif self.board.get_value(x, y) == "O":
                    self.draw_stone(x, y, self.screen, WHITE, 1)

    def create_grid(self):
        cell_width = self.grid_width / NUM_LINES
        cell_height = self.grid_height / NUM_LINES

        font_size = min(self.grid_width // NUM_LINES, SCREEN_HEIGHT // 35)
        font = pygame.font.Font(None, font_size)

        for i in range(1, NUM_LINES + 1):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (self.start_x + i * cell_width - (cell_width / 2), self.start_y),
                (
                    self.start_x + i * cell_width - (cell_width / 2),
                    self.start_y + self.grid_height,
                ),
            )
            text = font.render(chr(64 + i), True, (0, 0, 0))

            # Get the width and height of the text surface
            text_width, text_height = text.get_size()

            # Calculate the x and y coordinates to center the text
            x = self.start_x + (i - 1) * cell_width + cell_width / 2 - text_width / 2
            y = self.start_y - text_height * 1.2

            # Draw the text on the screen
            self.screen.blit(text, (x, y))

        for i in range(1, NUM_LINES + 1):
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (
                    self.start_x,
                    self.start_y + i * cell_height - (cell_height / 2),
                ),
                (
                    self.start_x + self.grid_width,
                    self.start_y + i * cell_height - (cell_height / 2),
                ),
            )
            # Create a text surface object for horizontal lines
            text = font.render(str(i), True, (0, 0, 0))

            # Get the width and height of the text surface
            text_width, text_height = text.get_size()

            # Calculate the x and y coordinates to center the text
            x = self.start_x - text_width * 1.2
            y = self.start_y + (i - 1) * cell_height + cell_height / 2 - text_height / 2

            # Draw the text on the screen
            self.screen.blit(text, (x, y))

    def draw(self):
        # clear board surface
        self.create_grid()
        self._anchor_mouse_stones()
        self._draw_placed_stones()

    def run(self):
        while self.running:
            # self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.board_surface, (0, 0))
            # self.clock.tick(60)
            self.events()
            # self.update()
            self.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Interface(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.new()
    game.run()