
import pygame, sys
from settings import *
from level import Level
from message_screen import *


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Project FlyBy')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
area = 1
player_stats = {'salvage': 0, 'lives': 5, 'weapons': ['gravity']}
respawn = False
def record_player(level,player):
    global player_stats
    if player.salv_trigger:
        player.salv_trigger = False
        if player.salvage < player_stats['salvage']:
            player_stats['salvage'] = player.salvage
        elif player.lives > player_stats['lives']:
            player.lives = player_stats['lives']
        elif len(player.weapons_owned) > len(player_stats['weapons']):
            player_stats['weapons'] = player.weapons_owned
        else:
            player_stats = {'salvage': player.salvage, 'lives': player.lives, 'weapons': player.weapons_owned}
    else:
        if player.salvage < player_stats['salvage']:
            player.salvage = player_stats['salvage']
        elif player.lives > player_stats['lives']:
            player.lives = player_stats['lives']
        else:
            player_stats = {'salvage': player.salvage, 'lives': player.lives}

    global respawn
    respawn = level.respawn

start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
typing_screen = TypingTextScreen(SCREEN_WIDTH, SCREEN_HEIGHT, START_TEXT)
respawn_screen = TypingTextScreen(SCREEN_WIDTH, SCREEN_HEIGHT, RESPAWN_TEXT)
level = Level(screen, area, player_stats, record_player)
game_over = GameOver(SCREEN_WIDTH, SCREEN_HEIGHT, 60, (255, 255, 255))
pause_screen = PauseScreen(SCREEN_WIDTH, SCREEN_HEIGHT)  

paused = False 
show_fullscreen_image = False
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
            if not level.over and not respawn:
                level.run()
                level.check_gameover()
            elif level.over:
                game_over.run(screen)
            elif level.respawn:
                respawn_screen.run(screen, delta_time)

        if level.next_lv:
            area += 1
            level = Level(screen, area, player_stats, record_player)
            level.next_lv = False
            level.started = True

        if keys[pygame.K_a]:
            if level.over:
                area = 1
                player_stats = {'salvage': 0, 'lives': 5, 'weapons': ['gravity']}
                level = Level(screen, area, player_stats, record_player)
                level.started = False

        if keys[pygame.K_f]:
            if respawn:
                level = Level(screen, area, player_stats, record_player)
                level.started = True
                respawn = False
        
        start_screen.handle_input(level,typing_screen)
        

    if keys[pygame.K_c] and paused and current_time - pause_timer >= pause_cooldown:
        show_fullscreen_image = not show_fullscreen_image  # Toggle the flag
        pause_timer = current_time
    if paused:
        pause_screen.display(screen, show_fullscreen_image)

    if keys[pygame.K_p] and current_time - pause_timer >= pause_cooldown:
        paused = not paused
        pause_timer = current_time  

    if paused:
        pause_screen.display(screen)

    pygame.display.update()
    clock.tick(60)
