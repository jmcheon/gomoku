import pygame
import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox
from ui_config import *


class Interface:
    def __init__(self, start_x, start_y, grid_width, grid_height):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board_surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        pygame.display.set_caption("Omok")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font("arial")
        self.grid_created = False
        self.start_x = start_x
        self.start_y = start_y
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.captured_p1 = 0
        self.captured_p2 = 0
        self.turn = PLAYER_1
        self.duration = 1.0  # You can adjust this as needed
        self.animation_start_time = None
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        ##
        ## right pane
        ##
        self.right_pane_rect = pygame.Rect(
            right_pane_begin_x, right_pane_begin_y, right_pane_width, right_pane_height
        )
        self.time_rect = pygame.Rect(
            self.right_pane_rect.centerx - time_width / 2,
            time_height / 2,
            time_width,
            time_height,
        )
        self.scorebox_rect = pygame.Rect(
            self.right_pane_rect.centerx - scorebox_width / 2,
            self.time_rect.bottom,
            scorebox_width,
            scorebox_height,
        )
        self.log_rect = pygame.Rect(
            self.right_pane_rect.centerx - log_width / 2,
            self.scorebox_rect.bottom + self.right_pane_rect.height / 20,
            log_width,
            log_height,
        )
        self.text_box = UITextBox(
            html_text="<body><font color=#E0E080></font>",
            relative_rect=self.log_rect,
            manager=self.ui_manager,
        )

    def new(self):
        self.show_start_screen()

    def show_start_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_text(
            "Press any key to create the grid",
            22,
            LINE_COLOR,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
        )
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_circles(self, x, y, target, color):
        initial_size = 6  # Adjust as needed
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

    def run(self):
        grid_x, grid_y = 0, 0
        while self.running:
            self.screen.blit(self.board_surface, (0, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x -= GRID_START_X
            mouse_y -= GRID_START_Y
            if (
                0 <= mouse_x < CELL_SIZE_X * NUM_LINES
                and 0 <= mouse_y < CELL_SIZE_Y * NUM_LINES
                and mouse_x <= SCREEN_WIDTH - GRID_START_X
                and mouse_y <= SCREEN_HEIGHT - GRID_START_Y
            ):
                grid_x = mouse_x // CELL_SIZE_X
                grid_y = mouse_y // CELL_SIZE_Y

            self.board_surface.fill((0, 0, 0, 0))
            if self.turn == PLAYER_1:
                self.draw_circles(grid_x, grid_y, self.board_surface, black_transparent)
            elif self.turn == PLAYER_2:
                self.draw_circles(grid_x, grid_y, self.board_surface, white_transparent)

            # self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == pygame.BUTTON_LEFT
            ):
                self.turn = PLAYER_2 if self.turn == PLAYER_1 else PLAYER_1
                self.text_box.append_html_text("hihihihi<br>")
                self.text_box.update(5.0)
                self.captured_p1 += 1
                self.captured_p2 -= 1
            self.ui_manager.process_events(event)

    def update(self):
        pygame.display.update()
        pass

    def draw(self):
        if not self.grid_created:
            self.create_grid()
            self.grid_created = True
        self.display_right_pane()

        self.ui_manager.update(0.01)
        self.ui_manager.draw_ui(window_surface=self.screen)
        pygame.display.flip()

    def create_grid(self):
        self.screen.fill(BACKGROUND_COLOR)
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
            # Create a text surface object
            # The first parameter is the text
            # The second parameter is anti-aliasing
            # The third parameter is the color of the text
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
        # self.create_alphabet_row()
        # self.create_number_col()

    def display_right_pane(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.right_pane_rect, 2)

        self.display_time()
        self.display_scorebox()
        self.display_log()

    def display_time(self):
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, self.time_rect)

        # Get the elapsed time since pygame started
        elapsed_time_millis = pygame.time.get_ticks()

        # Convert the time to minutes and seconds
        elapsed_time = divmod(elapsed_time_millis // 1000, 60)

        # Format the time as "00:00"
        formatted_time = "{:02}:{:02}".format(*elapsed_time)

        # Draw the time
        self.draw_text(
            str(formatted_time),
            22,
            BLACK,
            self.time_rect.centerx,
            self.time_rect.centery,
        )

    def display_scorebox(self):
        pygame.draw.rect(self.screen, (0, 255, 0), self.scorebox_rect, 3)

        p1_name_rect = pygame.Rect(
            self.scorebox_rect.left,
            self.scorebox_rect.top,
            self.scorebox_rect.width / 2,
            self.scorebox_rect.height / 2 * 0.8,
        )
        p2_name_rect = pygame.Rect(
            self.scorebox_rect.centerx,
            self.scorebox_rect.top,
            self.scorebox_rect.width / 2,
            self.scorebox_rect.height / 2 * 0.8,
        )

        cursor_left = pygame.Rect(
            self.scorebox_rect.left,
            self.scorebox_rect.top + self.scorebox_rect.height / 2 * 0.8,
            self.scorebox_rect.width / 2,
            self.scorebox_rect.height / 2 * 0.2,
        )

        cursor_right = pygame.Rect(
            self.scorebox_rect.centerx,
            self.scorebox_rect.top + self.scorebox_rect.height / 2 * 0.8,
            self.scorebox_rect.width / 2,
            self.scorebox_rect.height / 2 * 0.2,
        )

        p1_score_rect = pygame.Rect(
            self.scorebox_rect.left,
            self.scorebox_rect.top + self.scorebox_rect.height / 2,
            self.scorebox_rect.width / 2,
            self.scorebox_rect.height / 2,
        )
        p2_score_rect = pygame.Rect(
            self.scorebox_rect.centerx,
            self.scorebox_rect.top + self.scorebox_rect.height / 2,
            # self.scorebox_rect.bottom,
            self.scorebox_rect.width / 2,
            self.scorebox_rect.height / 2,
        )

        pygame.draw.rect(self.screen, BLACK, p1_name_rect, 2)
        pygame.draw.rect(self.screen, BLACK, p2_name_rect, 2)
        pygame.draw.rect(
            self.screen,
            BLACK if self.turn == PLAYER_1 else BACKGROUND_COLOR,
            cursor_left,
        )
        pygame.draw.rect(
            self.screen,
            BLACK if self.turn == PLAYER_2 else BACKGROUND_COLOR,
            cursor_right,
        )
        pygame.draw.rect(self.screen, BLACK, p1_score_rect, 2)
        pygame.draw.rect(self.screen, BLACK, p2_score_rect, 2)

        font_captured_score = pygame.font.Font(
            None, 8 * (SCREEN_WIDTH // 100)
        )  # Use the default font
        p1_text = font_captured_score.render(f"{self.captured_p1}", True, BLACK)
        p1_textbox = p1_text.get_rect()
        p1_textbox.centerx = p1_score_rect.centerx
        p1_textbox.centery = p1_score_rect.centery
        # player1_rect.centery = captured_score_area.centery

        p2_text = font_captured_score.render(f"{self.captured_p2}", True, BLACK)
        p2_textbox = p2_text.get_rect()
        p2_textbox.centerx = p2_score_rect.centerx
        p2_textbox.centery = p2_score_rect.centery

        self.screen.blit(p1_text, p1_textbox)
        self.screen.blit(p2_text, p2_textbox)

    def display_log(self):
        pygame.draw.rect(self.screen, (0, 0, 255), self.log_rect, 3)

    # def display_captured_score(self):
    #     box_width = SCREEN_WIDTH / 5
    #     box_height = 200
    #     captured_score_area = pygame.Rect(
    #         SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4 - 50,
    #         SCREEN_HEIGHT / 8,
    #         box_width,
    #         box_height,
    #     )

    #     p1_name_rect = pygame.Rect(
    #         captured_score_area.left,
    #         captured_score_area.top,
    #         captured_score_area.width / 2,
    #         captured_score_area.height / 2 * 0.8,
    #     )

    #     p2_name_rect = pygame.Rect(
    #         captured_score_area.centerx,
    #         captured_score_area.top,
    #         captured_score_area.width / 2,
    #         captured_score_area.height / 2 * 0.8,
    #     )

    #     cursor_left = pygame.Rect(
    #         captured_score_area.left,
    #         captured_score_area.top + captured_score_area.height / 2 * 0.8,
    #         captured_score_area.width / 2,
    #         captured_score_area.height / 2 * 0.2,
    #     )
    #     cursor_right = pygame.Rect(
    #         captured_score_area.centerx,
    #         captured_score_area.top + captured_score_area.height / 2 * 0.8,
    #         captured_score_area.width / 2,
    #         captured_score_area.height / 2 * 0.2,
    #     )

    #     p1_score_rect = pygame.Rect(
    #         captured_score_area.left,
    #         captured_score_area.top + captured_score_area.height / 2,
    #         captured_score_area.width / 2,
    #         captured_score_area.height / 2,
    #     )
    #     p2_score_rect = pygame.Rect(
    #         captured_score_area.centerx,
    #         captured_score_area.top + captured_score_area.height / 2,
    #         # captured_score_area.bottom,
    #         captured_score_area.width / 2,
    #         captured_score_area.height / 2,
    #     )

    #     pygame.draw.rect(self.screen, BLACK, captured_score_area, 2)
    #     pygame.draw.rect(self.screen, BLACK, cursor_left)
    #     pygame.draw.rect(self.screen, BLACK, cursor_right, 2)
    #     pygame.draw.rect(self.screen, BLACK, p1_name_rect, 2)
    #     pygame.draw.rect(self.screen, BLACK, p2_name_rect, 2)
    #     pygame.draw.rect(self.screen, BLACK, p1_score_rect, 2)
    #     pygame.draw.rect(self.screen, BLACK, p2_score_rect, 2)

    #     font_captured_score = pygame.font.Font(None, 36)  # Use the default font
    #     p1_text = font_captured_score.render(f"{self.captured_p1}", True, BLACK)
    #     p1_textbox = p1_text.get_rect()
    #     p1_textbox.centerx = p1_score_rect.centerx
    #     p1_textbox.centery = p1_score_rect.centery
    #     # player1_rect.centery = captured_score_area.centery

    #     p2_text = font_captured_score.render(f"{self.captured_p2}", True, BLACK)
    #     p2_textbox = p2_text.get_rect()
    #     p2_textbox.centerx = p2_score_rect.centerx
    #     p2_textbox.centery = p2_score_rect.centery

    #     self.screen.blit(p1_text, p1_textbox)
    #     self.screen.blit(p2_text, p2_textbox)

    #     # self.screen.blit(player2_text, player2_rect)


if __name__ == "__main__":
    starting_x = (5 * SCREEN_WIDTH / 8) / 10  # Change the starting X coordinate
    starting_y = SCREEN_HEIGHT / 10  # Change the starting Y coordinate
    grid_width = SCREEN_WIDTH // 2  # Change the width of the grid
    grid_height = SCREEN_HEIGHT // 1.25  # Change the height of the grid

    game = Interface(starting_x, starting_y, grid_width, grid_height)
    game.new()
    game.run()
