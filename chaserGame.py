import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('chaser')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to clear it each frame
    screen.fill((242, 173, 71))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
