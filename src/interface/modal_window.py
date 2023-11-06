import pygame
import pygame_gui


class ModalWindow:
    def __init__(self, manager, window_size):
        self.manager = manager
        self.window_size = window_size
        self.modal_window = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((100, 100), self.window_size),
            manager=self.manager,
            visible=False,
        )
        self.modal_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (self.window_size[0] - 20, 40)),
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

    def close_modal(self):
        self.modal_window.hide()


def main():
    pygame.init()

    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("PygameGUI Modal Window")

    manager = pygame_gui.UIManager(window_size)

    modal = ModalWindow(manager, (300, 150))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 50), (150, 40)),
        text="Open Modal",
        manager=manager,
    )

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button:
                        modal.open_modal()
                    elif event.ui_element == modal.exit_button:
                        pygame.quit()  # Exits the application when 'Exit' button is clicked
                    elif event.ui_element == modal.back_button:
                        modal.close_modal()  # To go back to the main screen

            manager.process_events(event)

        manager.update(time_delta)
        window.fill((255, 255, 255))
        manager.draw_ui(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
