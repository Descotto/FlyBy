
import pygame, sys
from settings import *
from level import Level
from gameover import GameOver



pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
level = Level(screen)
game_over = GameOver(SCREEN_WIDTH, SCREEN_HEIGHT,  60, (255, 255, 255))
image = pygame.image.load('./Assets/map_files/map_1/map_1.png')

def background_load(image):
    screen.blit(image, (0,0))




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    if not level.over:
        level.run()
    elif level.over:
        game_over.run(screen)

   
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if level.over:
            level = Level(screen)      
        

    pygame.display.update()
    clock.tick(60)