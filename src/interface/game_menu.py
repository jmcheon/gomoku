import pygame
import pygame_gui
from src.config import *


class GameMenu:
    def __init__(self, screen, ui_manager=None):
        self.screen = screen
        self.manager = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT), "resources/log_theme.json"
        )
        self.init_buttons()
        self.init_texts()
        self.show_main_menu = True
        self.show_options_menu = False

    def init_buttons(self):
        # Create the main menu button
        self.button_main = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 200), (200, 50)),
            text="Options",
            manager=self.manager,
        )

        # Create the options menu button
        self.button_options = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 300), (200, 50)),
            text="Back",
            manager=self.manager,
        )
        self.button_options.hide()  # Hide the options button initially

    def init_texts(self):
        font = pygame.font.Font(None, 36)
        # Create texts for different screens
        self.text_main = font.render("Main Menu", True, BLACK)
        self.text_options = font.render("Options Menu", True, BLACK)

    def draw(self):
        self.screen.fill(WHITE)  # Set a background color for the screen

        if self.show_main_menu:
            self.screen.blit(self.text_main, (700, 200))  # Adjusted text positions

        if self.show_options_menu:
            self.screen.blit(self.text_options, (700, 200))  # Adjusted text positions

        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def wait_for_key(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.button_main:
                            self.show_main_menu = False
                            self.show_options_menu = True
                            self.button_main.hide()
                            self.button_options.show()

                        if event.ui_element == self.button_options:
                            self.show_main_menu = True
                            self.show_options_menu = False
                            self.button_main.show()
                            self.button_options.hide()

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw()
