import pygame, sys, time
from settings import *
from sprites import BackGround, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('chaser')
        self.clock = pygame.time.Clock()
        self.active = False  # Start with no movement, waiting for game start
        self.state = 'START_MENU'  # Initial game state is the start menu
        self.obstacles_passed = 0

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Scale factor based on background size and window height
        bg_height = pygame.image.load("graphics/environment/simple.png").get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # Initial sprite setup
        BackGround(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor * 1.3, "bottom")
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor * 2, "top")
        self.plane = Plane(self.all_sprites, self.scale_factor*0.25)

        # Timer for obstacle generation
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Setup for displaying text (score and instructions)
        self.font = pygame.font.Font("graphics/font/font.ttf", 27)
        self.menu_font = pygame.font.Font("graphics/font/font.ttf", 20) 
        self.score = 0
        self.start_offset = 0

        # Main menu setup
        # self.menu_surf = pygame.image.load("graphics/menu.png").convert_alpha()
        # self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))
        # Main menu setup with text instead of an image
        menu_text = "Press Spacebar to Try Again"
        menu_text_quit = "Press Q to Quit"
        self.menu_surf = self.menu_font.render(menu_text, True, (0, 0, 0))  # White color text
        self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT / 4))
        #For Quit
        self.menu_surf_q = self.menu_font.render(menu_text_quit, True, (0, 0, 0))  # White color text
        self.menu_q_rect = self.menu_surf_q.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT / 3))

        # Background music setup
        self.music = pygame.mixer.Sound("graphics/sounds/free.mp3")
        self.music.play(loops=-1)

    def display_start_screen(self):
        
        # Load the background image
        background_image = pygame.image.load('graphics/environment/simple.png').convert()  # Update the path to your image
        # Scale the image to fit the screen
        background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
        # Blit the background image
        self.display_surface.blit(background_image, (0, 0))
        # Display the game title and "Press Spacebar to Start" instructions
        # self.display_surface.fill('red')
        title_surf = self.font.render("chaser", True, 'black')
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))
        instructions_surf = self.font.render("Press Spacebar to Begin", True, 'black')
        instructions_rect = instructions_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.display_surface.blit(title_surf, title_rect)
        self.display_surface.blit(instructions_surf, instructions_rect)


    def collisions(self):
        # Collision detection between the plane and obstacles
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask):
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False  # Stop game movement
            self.plane.kill()  # Remove the plane sprite

    def update_obstacles_passed(self):
        for sprite in self.collision_sprites:
            if getattr(sprite, 'sprite_type', None) == 'obstacle' and sprite.rect.right < self.plane.rect.left and not sprite.passed:
                self.obstacles_passed += 1
                sprite.passed = True

    def display_score(self):
        # Display the current score or final score based on game state
        if self.active:
            time = (pygame.time.get_ticks() - self.start_offset) // 1000
            self.score = time + self.obstacles_passed * 5
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)
        score_surf = self.font.render("Score: " + str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time  # Calculate delta time for frame-independent movement
            last_time = time.time()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:       
                    if event.key == pygame.K_SPACE:
                        if self.state == 'START_MENU':
                            # Start the game from the start menu
                            self.state = 'PLAYING'
                            self.active = True  # Enable game movement and logic
                            self.start_offset = pygame.time.get_ticks()  # Reset score timer
                        elif self.state == 'PLAYING' and self.active:
                            # Allow jumping only when the game is in the 'PLAYING' state and active
                            self.plane.jump()
                        else:
                            self.plane = Plane(self.all_sprites, self.scale_factor*0.25)
                            self.active = True
                            self.start_offset = pygame.time.get_ticks()
            
                if event.type == self.obstacle_timer and self.active:
                    # Generate a new obstacle
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)


            if self.state == 'START_MENU':
                self.display_start_screen()  # Display the start screen
            elif self.state == 'PLAYING':
                # Update and draw sprites, display score, and handle collisions
                self.all_sprites.update(dt)
                self.update_obstacles_passed() 
                self.all_sprites.draw(self.display_surface)
                self.display_score()
                       
                if self.active:
                    self.collisions()
                else: 
                    self.display_surface.blit(self.menu_surf, self.menu_rect)
                    self.display_surface.blit(self.menu_surf_q,self.menu_q_rect)
                    self.obstacles_passed = 0

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()