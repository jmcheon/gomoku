import pygame
import pygame_gui


class ModalWindow:
    def __init__(self, manager, screen_size):
        self.manager = manager
        self.screen_size = screen_size
        self.is_open = False
        self.modal_window = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((100, 100), (400, 400)),
            manager=self.manager,
            visible=False,
        )
        self.modal_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (self.screen_size[0] - 20, 40)),
            text="This is a modal window!",
            manager=self.manager,
            container=self.modal_window,
        )
        # 'Back to Main' button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 60), (130, 40)),
            text="Back to Main",
            manager=self.manager,
            container=self.modal_window,
        )
        # 'Exit' button
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 60), (100, 40)),
            text="Exit",
            manager=self.manager,
            container=self.modal_window,
        )

    def open_modal(self):
        self.modal_window.show()
        self.is_open = True
        self.modal_window.visible = True

    def close_modal(self):
        self.modal_window.hide()
        self.is_open = False

    def wait_for_response(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.exit_button:
                        pygame.quit()
                    elif event.ui_element == self.back_button:
                        print(
                            "back to main menu: TODO, reset board, pull up modal window"
                        )
            self.manager.process_events(event)
