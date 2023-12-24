
import pygame
import sys
from settings import *
from level import Level
from message_screen import *


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
area = 1
start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
typing_screen = TypingTextScreen(SCREEN_WIDTH, SCREEN_HEIGHT, START_TEXT)
level = Level(screen, area)
game_over = GameOver(SCREEN_WIDTH, SCREEN_HEIGHT, 60, (255, 255, 255))
pause_screen = PauseScreen(SCREEN_WIDTH, SCREEN_HEIGHT)  

paused = False 
pause_timer = 0
pause_cooldown = 1000 

while True:
    delta_time = clock.tick(60) / 1000.0
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not paused:  # Only update the game if it's not paused
        screen.fill('black')
        if level.start_text:
            typing_screen.run(screen, delta_time)
        elif not level.started:
            start_screen.run(screen)
        else:
            if not level.over:
                level.run()
            elif level.over:
                game_over.run(screen)

        if level.next_lv:
            area += 1
            level = Level(screen, area)
            level.next_lv = False
            level.started = True

        if keys[pygame.K_a]:
            if level.over:
                level = Level(screen, area)

        if keys[pygame.K_f]:
            if not level.start_text:
                level.start_text = True

        if keys[pygame.K_RETURN]:
            if not level.started:
                level.started = True
                level.start_text = False
                typing_screen.stop_music()
                # del typing_screen
                level.play_music()

    
    if keys[pygame.K_p] and current_time - pause_timer >= pause_cooldown:
        paused = not paused
        pause_timer = current_time  

    if paused:
        pause_screen.display(screen)

    pygame.display.update()
    clock.tick(60)
