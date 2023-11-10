import pygame
import pygame_gui
import math

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame GUI Example")

# Create a UI manager
ui_manager = pygame_gui.UIManager(window_size)

# Create the first slider and label above the bar
capture_stone_slider = pygame_gui.elements.UIHorizontalSlider(
    pygame.Rect((int(window_size[0] / 2), int(window_size[1] * 0.5) - 40), (240, 25)),
    10.0,
    (10.0, 50.0),
    ui_manager,
    object_id="#capture_stone_slider",
    click_increment=2,
)
capture_stone_label = pygame_gui.elements.UILabel(
    pygame.Rect((int(window_size[0] / 2), int(window_size[1] * 0.5) - 80), (40, 40)),
    str(int(capture_stone_slider.get_current_value())),
    ui_manager,
)

# Create the second slider and label above the bar
black_capture_slider = pygame_gui.elements.UIHorizontalSlider(
    pygame.Rect((int(window_size[0] / 2), int(window_size[1] * 0.6) - 40), (240, 25)),
    0,
    (0, 6),
    ui_manager,
    object_id="#black_capture_slider",
    click_increment=2,
)
black_capture_label = pygame_gui.elements.UILabel(
    pygame.Rect((int(window_size[0] / 2), int(window_size[1] * 0.6) - 80), (40, 40)),
    str(int(black_capture_slider.get_current_value())),
    ui_manager,
)

# Create the second slider and label above the bar
white_capture_slider = pygame_gui.elements.UIHorizontalSlider(
    pygame.Rect((int(window_size[0] / 2), int(window_size[1] * 0.7) - 40), (240, 25)),
    0,
    (0, 6),
    ui_manager,
    object_id="#white_capture_slider",
    click_increment=2,
)
white_capture_label = pygame_gui.elements.UILabel(
    pygame.Rect((int(window_size[0] / 2), int(window_size[1] * 0.7) - 80), (40, 40)),
    str(int(white_capture_slider.get_current_value())),
    ui_manager,
)


# Create "Capture" button
capture_button_rect = pygame.Rect(
    (int(window_size[0] / 2) + 260, int(window_size[1] * 0.5) - 40), (80, 30)
)
capture_button = pygame_gui.elements.UIButton(
    capture_button_rect,
    "Enable",
    ui_manager,
    object_id="#capture_button",
)

# Create "Double-Three" button
double_three_button_rect = pygame.Rect(
    (int(window_size[0] / 2) + 260, int(window_size[1] * 0.6) - 40), (80, 30)
)
double_three_button = pygame_gui.elements.UIButton(
    double_three_button_rect,
    "Enable",
    ui_manager,
    object_id="#double_three_button",
)

options = ["Standard", "Pro", "Swap", "Swap2"]  # Replace with your desired options
dropdown_rect = pygame.Rect(
    (int(window_size[0] / 2), int(window_size[1] * 0.8) - 40), (240, 25)
)
dropdown_menu = pygame_gui.elements.UIDropDownMenu(
    options,
    options[0],  # Default selected option
    dropdown_rect,
    ui_manager,
    object_id="#dropdown_menu",
)


# Run the game loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        ui_manager.process_events(event)

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == capture_stone_slider:
                value = int(capture_stone_slider.get_current_value())
                capture_stone_label.set_text(str(value))

                # Update the maximum value of the second slider dynamically
                slider2_max_value = value / 2 + (1 if (value / 2) % 2 != 0 else 0)
                black_capture_slider.value_range = (0, slider2_max_value)
                print(0, slider2_max_value)
                # Adjust the position of slider2 within the new range
                current_value = black_capture_slider.get_current_value()
                if current_value > slider2_max_value:
                    black_capture_slider.set_current_value(slider2_max_value)
                black_capture_label.set_text(
                    str(int(black_capture_slider.get_current_value()))
                )
            elif event.ui_element == black_capture_slider:
                black_capture_label.set_text(
                    str(int(black_capture_slider.get_current_value()))
                )
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == capture_button:
                if capture_button.text == "Enable":
                    capture_button.set_text("Disable")
                else:
                    capture_button.set_text("Enable")
            elif event.ui_element == double_three_button:
                if double_three_button.text == "Enable":
                    double_three_button.set_text("Disable")
                else:
                    double_three_button.set_text("Enable")
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == dropdown_menu:
                selected_option = dropdown_menu.selected_option

    ui_manager.update(time_delta)

    screen.fill((255, 255, 255))

    ui_manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
