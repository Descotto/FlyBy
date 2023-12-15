import pygame
import os
from settings import *
from player import Player
from tiles import Tile
from bullet import *
from cannon import Cannon

class Level:
    def __init__(self,surface):
        
        self.display_surface = surface
        self.level_setup()
        self.over = False
        self.play_music('./Assets/midi/here-i-go.mp3')
        

    def level_setup(self):
        self.visuals = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        maps = MAP_LAYOUTS['map_1']
        
        for style,map in maps.items():
            for row_index, row in enumerate(map):
                for col_index, cell in enumerate(row):

                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if cell != '-1':
                        if style == 'floor':
                            tile = Tile((x,y), [self.obstacle_sprites])
                            # CREATING PLAYER 
                        if style == 'player': 
                            player_one = Player(
                                (x,y),
                                [self.visuals,self.player],
                                self.shoot,
                                self.secondary_shot)

                        if style == 'cannons':
                            cannon = Cannon((x,y), [self.visuals, self.obstacle_sprites])

    def play_music(self, music_file):
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)

    def collisions(self,player):

        player.rect.x += player.direction.x * player.speed
        player.rect.y += player.direction.y * player.speed

        for sprite in self.obstacle_sprites.sprites():
            if sprite.rect.colliderect(player.hitbox):
                player.hp = 0
  
    def check_gameover(self):
        player = self.player.sprite
        if player.hp < -10:
            self.over = True

    # PLAYER ACTIONS
    def shoot(self):
        player = self.player.sprite
        current_time = pygame.time.get_ticks()
        if current_time - player.last_shoot_time > player.bullet_cooldown * 1000:
            bullet = Bullet(self.player.sprite.rect,[self.visuals])
            player.last_shoot_time = current_time

    def secondary_shot(self):
        player = self.player.sprite
        current_time = pygame.time.get_ticks()
        if current_time - player.last_s_time > player.s_cooldown * 1000:
            bullet = D_Bullet(self.player.sprite.rect,[self.visuals])
            player.last_s_time = current_time

    def run(self):
        player = self.player.sprite
        self.visuals.custom_draw(player)
        self.visuals.update()
        self.collisions(player)
        self.check_gameover()
        



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 3
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #CREATE FLOOR
       
        self.floor_surf = pygame.image.load('./Assets/map_files/map_1/map_1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw floor
        floor_upset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_upset_pos)


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)


