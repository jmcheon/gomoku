import pygame
import pygame.freetype

pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 24
TEXT_BOX_HEIGHT = 100
SCROLL_SPEED = 1

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a font
font = pygame.freetype.SysFont(None, FONT_SIZE)

# Create a list of texts
texts = ["Line {}".format(i) for i in range(1, 51)]

# Create a surface for the text box
text_box_surf = pygame.Surface((WIDTH, TEXT_BOX_HEIGHT))

# Create a rect for the text box
text_box_rect = text_box_surf.get_rect(topleft=(0, HEIGHT - TEXT_BOX_HEIGHT))

# Variables to keep track of scrolling
scroll_y = 0
scrolling_up = False
scrolling_down = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scrolling_up = True
            elif event.key == pygame.K_DOWN:
                scrolling_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                scrolling_up = False
            elif event.key == pygame.K_DOWN:
                scrolling_down = False

    # Fill the screen
    screen.fill(WHITE)

    # Fill the text box
    text_box_surf.fill(WHITE)

    # Draw the texts
    for i, text in enumerate(texts):
        text_surf, _ = font.render(text, BLACK)
        text_rect = text_surf.get_rect(topleft=(0, i * FONT_SIZE - scroll_y))
        text_box_surf.blit(text_surf, text_rect)

    # Scroll the text box
    if scrolling_up:
        scroll_y -= SCROLL_SPEED
    elif scrolling_down:
        scroll_y += SCROLL_SPEED

    # Draw the text box
    screen.blit(text_box_surf, text_box_rect)

    # Update the display
    pygame.display.flip()

pygame.quit()
