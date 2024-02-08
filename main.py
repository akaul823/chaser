import pygame, sys, time
from settings import *
from sprites import BackGround, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('chaser')
        self.clock = pygame.time.Clock()
        self.active = True

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load("graphics/environment/simple.png").get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        #sprite setup
        BackGround(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites,self.collision_sprites], self.scale_factor*1.3, "bottom")
        Ground([self.all_sprites,self.collision_sprites], self.scale_factor * 2, "top")
        self.plane = Plane(self.all_sprites, self.scale_factor)

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        #text
        self.font = pygame.font.Font("graphics/font/font.ttf",30)
        self.score = 0

        #menu
        self.menu_surf = pygame.image.load("graphics/menu.png").convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT /3))
    
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites,False, pygame.sprite.collide_mask):
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            self.score = pygame.time.get_ticks() // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height/1.5)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH /2,y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            #delta time
            dt = time.time() - last_time
            last_time = time.time()

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.active:
                            self.plane.jump()
                        else:
                            self.plane = Plane(self.all_sprites, self.scale_factor)
                            self.active = True
                if event.type == self.obstacle_timer:
                    Obstacle([self.all_sprites,self.collision_sprites], self.scale_factor*1.1)

            #game logic
            self.display_surface.fill('purple')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active: self.collisions()
            else: self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()