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
        self.init_main_menu()
        self.init_options_menu()
        self.init_texts()
        self.menu = MAIN_MENU

    def init_main_menu(self):
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

    def init_options_menu(self):
        # Slider and label for capture stone
        self.capture_stone_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((int(self.width / 2) - 120, int(self.height * 0.4)), (240, 25)),
            10.0,
            (10.0, 50.0),
            self.manager,
            object_id="#capture_stone_slider",
            click_increment=2,
        )
        self.capture_stone_label = pygame_gui.elements.UILabel(
            pygame.Rect(
                (int(self.width / 2) - 120, int(self.height * 0.4) - 40), (40, 40)
            ),
            str(int(self.capture_stone_slider.get_current_value())),
            self.manager,
        )

        # Slider and label for black capture
        self.black_capture_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((int(self.width / 2) - 120, int(self.height * 0.5)), (240, 25)),
            0,
            (0, 6),
            self.manager,
            object_id="#black_capture_slider",
            click_increment=2,
        )
        self.black_capture_label = pygame_gui.elements.UILabel(
            pygame.Rect(
                (int(self.width / 2) - 120, int(self.height * 0.5) - 40), (40, 40)
            ),
            str(int(self.black_capture_slider.get_current_value())),
            self.manager,
        )

        # Slider and label for white capture
        self.white_capture_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((int(self.width / 2) - 120, int(self.height * 0.6)), (240, 25)),
            0,
            (0, 6),
            self.manager,
            object_id="#white_capture_slider",
            click_increment=2,
        )
        self.white_capture_label = pygame_gui.elements.UILabel(
            pygame.Rect(
                (int(self.width / 2) - 120, int(self.height * 0.6) - 40), (40, 40)
            ),
            str(int(self.white_capture_slider.get_current_value())),
            self.manager,
        )

        # "Capture" button
        self.capture_button = pygame_gui.elements.UIButton(
            pygame.Rect((int(self.width / 2) + 80, int(self.height * 0.5)), (80, 30)),
            "Enable",
            self.manager,
            object_id="#capture_button",
        )

        # "Double Three" button
        self.doublethree_button = pygame_gui.elements.UIButton(
            pygame.Rect((int(self.width / 2) + 80, int(self.height * 0.6)), (80, 30)),
            "Enable",
            self.manager,
            object_id="#doublethree_button",
        )

        # Dropdown menu
        options = [
            "Standard",
            "Pro",
            "Swap",
            "Swap2",
        ]  # Replace with your desired options
        self.dropdown_menu = pygame_gui.elements.UIDropDownMenu(
            options,
            options[0],
            pygame.Rect((int(self.width / 2) + 80, int(self.height * 0.7)), (80, 30)),
            self.manager,
            object_id="#dropdown_menu",
        )

        # "Back" button at the bottom
        self.button_to_main = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (int(self.width / 2) - 100, self.height - 60), (200, 50)
            ),
            text="Back",
            manager=self.manager,
        )

    def init_texts(self):
        # Create UI Label elements for texts on different screens
        text_main_rect = (400, 100)
        self.text_main = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (self.width / 2 - text_main_rect[0] / 2, 200), text_main_rect
            ),
            text="오목 // Gomoku",
            manager=self.manager,
            object_id="#main_title",
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

    def show_main_menu(self):
        self.text_main.show()
        self.button_to_singleplay.show()
        self.button_to_multiplay.show()
        self.button_to_options.show()

    def hide_main_menu(self):
        self.text_main.hide()
        self.button_to_singleplay.hide()
        self.button_to_multiplay.hide()
        self.button_to_options.hide()

    def show_options_menu(self):
        self.text_options.show()
        self.capture_stone_label.show()
        self.capture_stone_slider.show()
        self.black_capture_label.show()
        self.black_capture_slider.show()
        self.white_capture_label.show()
        self.white_capture_slider.show()
        self.capture_button.show()
        self.doublethree_button.show()
        self.dropdown_menu.show()
        self.button_to_main.show()

    def hide_options_menu(self):
        self.text_options.hide()
        self.capture_stone_label.hide()
        self.capture_stone_slider.hide()
        self.black_capture_label.hide()
        self.black_capture_slider.hide()
        self.white_capture_label.hide()
        self.white_capture_slider.hide()
        self.capture_button.hide()
        self.doublethree_button.hide()
        self.dropdown_menu.hide()
        self.button_to_main.hide()

    def draw(self):
        self.screen.fill(WHITE)  # Set a background color for the screen

        if self.menu == MAIN_MENU:
            self.show_main_menu()
            self.hide_options_menu()

        elif self.menu == OPTIONS_MENU:
            self.show_options_menu()
            self.hide_main_menu()

        # TODO: responsive
        # self.screen.blit(self.text_name_email_1, (self.width - 550, self.height - 70))
        # self.screen.blit(self.text_name_email_2, (self.width - 460, self.height - 40))
        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def wait_for_key(self):
        running = True
        clock = pygame.time.Clock()

        selected_options = None
        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.button_to_main:
                            self.menu = MAIN_MENU

                        if event.ui_element == self.button_to_options:
                            self.menu = OPTIONS_MENU

                        if event.ui_element == self.button_to_singleplay:
                            print("Not Available")
                        if event.ui_element == self.button_to_multiplay:
                            # TODO: append all the options and return
                            selected_options = self.dropdown_menu.selected_option
                            self.menu = None
                            running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw()

        return selected_options
