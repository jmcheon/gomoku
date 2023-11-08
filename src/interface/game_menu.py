import pygame
import pygame_gui
from src.config import *


class GameMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.width = screen_width
        self.height = screen_height
        self.manager = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT), "resources/log_theme.json"
        )
        self.init_buttons()
        self.init_texts()
        self.show_main_menu = True
        self.show_options_menu = False

    def init_buttons(self):
        button_width = self.width / 6
        button_height = self.height / 12
        button_padding_horiz = button_height / 3
        # Create the main menu button
        self.button_to_singleplay = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width - button_width) // 2, self.height / 2),
                (button_width, button_height),
            ),
            text="Single Player (vs AI)",
            manager=self.manager,
        )

        self.button_to_multiplay = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (
                    (self.width - button_width) // 2,
                    self.height / 2 + (button_height + button_padding_horiz),
                ),
                (button_width, button_height),
            ),
            text="Multiplayer",
            manager=self.manager,
        )

        self.button_to_options = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (
                    (self.width - button_width) // 2,
                    self.height / 2 + (2 * (button_height + button_padding_horiz)),
                ),
                (button_width, button_height),
            ),
            text="Options",
            manager=self.manager,
        )

        # Create the options menu button
        self.button_to_main = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width / 2, self.height / 2), (200, 50)),
            text="Back",
            manager=self.manager,
        )
        # self.button_options.hide()  # Hide the options button initially

    def init_texts(self):
        # Create UI Label elements for texts on different screens
        self.text_main = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width / 2, 200), (400, 100)),
            text="오목 // Gomoku",
            manager=self.manager,
        )

        self.text_options = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((700, 200), (200, 50)),
            text="Options Menu",
            manager=self.manager,
            visible=False,
        )

        self.text_name_email_1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width - 550, self.height - 70), (400, 30)),
            text="by Jung Moo Cheon (cjung-mo@student.42.fr)",
            manager=self.manager,
        )

        self.text_name_email_2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width - 460, self.height - 40), (300, 30)),
            text="Sungyong Cho (sucho@student.42.fr)",
            manager=self.manager,
        )

    def draw(self):
        self.screen.fill(WHITE)  # Set a background color for the screen

        if self.show_main_menu:
            self.text_main.show()
            self.text_options.hide()
            self.button_to_singleplay.show()
            self.button_to_multiplay.show()
            self.button_to_options.show()
            self.button_to_main.hide()

        if self.show_options_menu:
            self.text_main.hide()
            self.text_options.show()
            self.button_to_singleplay.hide()
            self.button_to_multiplay.hide()
            self.button_to_options.hide()
            self.button_to_main.show()

        # TODO: responsive
        # self.screen.blit(self.text_name_email_1, (self.width - 550, self.height - 70))
        # self.screen.blit(self.text_name_email_2, (self.width - 460, self.height - 40))
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
                        if event.ui_element == self.button_to_main:
                            self.show_main_menu = True
                            self.show_options_menu = False

                        if event.ui_element == self.button_to_options:
                            self.show_main_menu = False
                            self.show_options_menu = True

                        if event.ui_element == self.button_to_singleplay:
                            print("Not Available")
                        if event.ui_element == self.button_to_multiplay:
                            self.show_main_menu = False
                            self.show_options_menu = False
                            running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw()
