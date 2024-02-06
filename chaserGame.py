import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chaser')

# Define the player character
player_color = (0, 0, 0)  # Black
player_rect = pygame.Rect(100, screen_height - 150, 50, 100)  # x, y, width, height

# Define an obstacle
obstacle_color = (255, 0, 0)  # Red
obstacle_rect = pygame.Rect(screen_width - 150, screen_height - 150, 50, 100)  # x, y, width, height

# Obstacle movement speed
obstacle_speed = 5

# Create a clock object
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Fill the screen with a color to clear it each frame
    screen.fill((242, 173, 71))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        # Make the player duck
        player_rect.height = 50
        player_rect.y = screen_height - 50  # Adjust the y-position so the player remains at the bottom
    else:
        # Return to normal height when not ducking
        player_rect.height = 100
        player_rect.y = screen_height - 150  # Reset the y-position when not ducking

    # Move the obstacle to the left to simulate the player moving forward
    obstacle_rect.x -= obstacle_speed

    # If the obstacle goes off the left side of the screen, reset its position to the right
    if obstacle_rect.x < -obstacle_rect.width:
        obstacle_rect.x = screen_width

    # Draw the player and obstacle
    pygame.draw.rect(screen, player_color, player_rect)
    pygame.draw.rect(screen, obstacle_color, obstacle_rect)

    # Check for collisions
    if player_rect.colliderect(obstacle_rect):
        print("Collision!")
    clock.tick(60) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display after all drawing commands
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


