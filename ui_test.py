import pygame

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
NUM_LINES = 19
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = BLACK
BACKGROUND_COLOR = WHITE


class Interface:
    def __init__(self, start_x, start_y, grid_width, grid_height):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.start_pos = None
        self.end_pos = None
        self.duration = 1.0  # You can adjust this as needed
        self.animation_start_time = None

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

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        # self.screen.fill(BACKGROUND_COLOR)
        if not self.grid_created:
            self.create_grid()
            self.grid_created = True

        self.display_time()
        self.display_captured_score()
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

    def display_time(self):
        # Define the area where the time is displayed (adjust as needed)
        time_area = pygame.Rect(
            SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4 - 50, SCREEN_HEIGHT / 10 - 20, 100, 40
        )

        # Fill the area with the background color
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, time_area)

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
            SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4,
            SCREEN_HEIGHT / 10,
        )

    def display_captured_score(self):
        box_width = SCREEN_WIDTH / 5
        box_height = 200
        captured_score_area = pygame.Rect(
            SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4 - 50,
            SCREEN_HEIGHT / 8,
            box_width,
            box_height,
        )

        p1_name_rect = pygame.Rect(
            captured_score_area.left,
            captured_score_area.top,
            captured_score_area.width / 2,
            captured_score_area.height / 2 * 0.8,
        )

        p2_name_rect = pygame.Rect(
            captured_score_area.centerx,
            captured_score_area.top,
            captured_score_area.width / 2,
            captured_score_area.height / 2 * 0.8,
        )

        cursor_left = pygame.Rect(
            captured_score_area.left,
            captured_score_area.top + captured_score_area.height / 2 * 0.8,
            captured_score_area.width / 2,
            captured_score_area.height / 2 * 0.2,
        )
        cursor_right = pygame.Rect(
            captured_score_area.centerx,
            captured_score_area.top + captured_score_area.height / 2 * 0.8,
            captured_score_area.width / 2,
            captured_score_area.height / 2 * 0.2,
        )

        p1_score_rect = pygame.Rect(
            captured_score_area.left,
            captured_score_area.top + captured_score_area.height / 2,
            captured_score_area.width / 2,
            captured_score_area.height / 2,
        )
        p2_score_rect = pygame.Rect(
            captured_score_area.centerx,
            captured_score_area.top + captured_score_area.height / 2,
            # captured_score_area.bottom,
            captured_score_area.width / 2,
            captured_score_area.height / 2,
        )

        pygame.draw.rect(self.screen, BLACK, captured_score_area, 2)
        pygame.draw.rect(self.screen, BLACK, cursor_left)
        pygame.draw.rect(self.screen, BLACK, cursor_right, 2)
        pygame.draw.rect(self.screen, BLACK, p1_name_rect, 2)
        pygame.draw.rect(self.screen, BLACK, p2_name_rect, 2)
        pygame.draw.rect(self.screen, BLACK, p1_score_rect, 2)
        pygame.draw.rect(self.screen, BLACK, p2_score_rect, 2)

        font_captured_score = pygame.font.Font(None, 36)  # Use the default font
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

        # self.screen.blit(player2_text, player2_rect)
        def animate(self, time_elapsed):
            progress = time_elapsed / self.duration
            if progress > 1.0:
                progress = 1.0
            x = self.start_pos[0] * (1 - progress) + self.end_pos[0] * progress
            y = self.start_pos[1] * (1 - progress) + self.end_pos[1] * progress
            self.cursor_left.topleft = (x, y)


if __name__ == "__main__":
    starting_x = 50  # Change the starting X coordinate
    starting_y = 50  # Change the starting Y coordinate
    grid_width = SCREEN_WIDTH // 2  # Change the width of the grid
    grid_height = SCREEN_HEIGHT // 1.25  # Change the height of the grid

    game = Interface(starting_x, starting_y, grid_width, grid_height)
    game.new()
    game.run()
