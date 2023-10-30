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
        if not self.grid_created:
            self.create_grid()
            self.grid_created = True

        pygame.display.flip()

    def create_grid(self):
        cell_width = self.grid_width / NUM_LINES
        cell_height = self.grid_height / NUM_LINES

        for i in range(1, NUM_LINES):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (self.start_x + i * cell_width, self.start_y),
                (self.start_x + i * cell_width, self.start_y + self.grid_height),
            )
        for i in range(1, NUM_LINES):
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (self.start_x, self.start_y + i * cell_height),
                (self.start_x + self.grid_width, self.start_y + i * cell_height),
            )
        self.create_alphabet_row()
        self.create_number_col()

    def create_alphabet_row(self):
        font_size = min(self.grid_width // NUM_LINES, SCREEN_HEIGHT // 35)
        start_x = self.start_x - font_size * 0.5  # Starting X position
        start_y = self.start_y - font_size * 1.2  # Starting Y position

        for i in range(NUM_LINES):  # Displaying A to Z
            character = chr(65 + i)  # Get ASCII character starting from 'A'
            font = pygame.font.Font(self.font_name, font_size)
            text_surface = font.render(character, True, LINE_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (start_x + (font_size) * i, start_y)
            self.screen.blit(text_surface, text_rect)

    def create_number_col(self):
        font_size = min(self.grid_width // NUM_LINES, SCREEN_HEIGHT // 35)
        start_x = self.start_x - font_size * 1.2  # Starting X position
        start_y = self.start_y + font_size * 0.5  # Starting Y position

        for i in range(NUM_LINES):  # Displaying numbers 1 to 19
            character = str(i + 1)  # Display numbers starting from 1
            font = pygame.font.Font(self.font_name, font_size)
            text_surface = font.render(character, True, LINE_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (
                start_x,
                start_y + (font_size + 10) * i,
            )  # Adjust position for vertical layout
            self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    starting_x = 50  # Change the starting X coordinate
    starting_y = 50  # Change the starting Y coordinate
    grid_width = SCREEN_WIDTH // 2  # Change the width of the grid
    grid_height = SCREEN_HEIGHT // 1.25  # Change the height of the grid

    game = Interface(starting_x, starting_y, grid_width, grid_height)
    game.new()
    game.run()
