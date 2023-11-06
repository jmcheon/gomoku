import pygame
import pygame_gui

# Pygame initialization
pygame.init()
win_width, win_height = 800, 600
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Menu Example")

# Pygame GUI initialization
manager = pygame_gui.UIManager((win_width, win_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Create the main menu button
button_main = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 200), (200, 50)), text="Options", manager=manager
)

# Create the options menu button
button_options = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 300), (200, 50)), text="Back", manager=manager
)
button_options.hide()  # Hide the options button initially

# Create texts for different screens
text_main = font.render("Main Menu", True, black)
text_options = font.render("Options Menu", True, black)

running = True
show_main_menu = True
show_options_menu = False

while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # if event.type == pygame.USEREVENT:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_main:
                show_main_menu = False
                show_options_menu = True
                button_main.hide()
                button_options.show()

            if event.ui_element == button_options:
                show_main_menu = True
                show_options_menu = False
                button_main.show()
                button_options.hide()

        manager.process_events(event)

    window.fill(white)
    manager.update(time_delta)

    if show_main_menu:
        window.blit(text_main, (350, 100))
        manager.draw_ui(window)

    if show_options_menu:
        window.blit(text_options, (320, 100))
        manager.draw_ui(window)

    pygame.display.update()

pygame.quit()
