import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Moving Rect")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)

# Rectangle properties
rect_width, rect_height = 50, 50
rect_x = 50
rect_y = win_height // 2 - rect_height // 2
rect_speed = 3  # Number of pixels to move per frame

range_start, range_end = 50, win_width - rect_width - 50  # Define the range

clock = pygame.time.Clock()  # Clock object to control frame rate

# Variables to track the current position and movement
current_position = "left"  # Assuming the initial position is on the left
target_position = range_start  # Target position for movement

moving = False  # Flag to indicate if the rectangle is currently moving

# Main game loop
running = True
while running:
    win.fill(white)  # Fill the window with white color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not moving:
                if current_position == "left":
                    target_position = range_end  # Move to the right side
                    current_position = "right"
                else:
                    target_position = range_start  # Move to the left side
                    current_position = "left"
                moving = True

    # Move towards the target position gradually
    if moving:
        if current_position == "right":
            if rect_x < target_position:
                rect_x += rect_speed
                if rect_x >= target_position:
                    rect_x = target_position
                    moving = False
        else:
            if rect_x > target_position:
                rect_x -= rect_speed
                if rect_x <= target_position:
                    rect_x = target_position
                    moving = False

    # Draw the rectangle
    pygame.draw.rect(win, red, (rect_x, rect_y, rect_width, rect_height))

    pygame.display.update()
    clock.tick(120)  # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
