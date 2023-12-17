import pygame
import os
from settings import *
from player import *
from tiles import Tile
from bullet import *
from cannon import Cannon
from ships import *
from power_ups import Power_Up
from particles import Particles

class Level:
    def __init__(self,surface):
        
        self.display_surface = surface
        self.level_setup()
        self.over = False
        self.play_music('./Assets/midi/EnterSandman.mp3')
        

    def level_setup(self):
        self.visuals = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.projectile_spritess = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.entities = pygame.sprite.Group()
        self.rewards = pygame.sprite.Group()

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
                                self.secondary_shot,
                                self.call_support)
                            player_one.support = True
                            exhaust = Particles((x,y),[self.visuals],'Exhaust1')

                        if style == 'cannons':
                            cannon = Cannon((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy1':
                            ship = Ship1((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy2':
                            ship = Ship2((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy3':
                            ship = Ship3((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy4':
                            ship = Ship4((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)

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
  
    def projectile_collision(self):
        for bullet in self.projectile_spritess.sprites():
            for obstacle in self.obstacle_sprites.sprites():
                if obstacle.rect.colliderect(bullet.rect):
                    #particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

            for entity in self.entities.sprites():
                if entity.rect.colliderect(bullet.rect):
                    entity.take_damage()
                    #particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

    def check_gameover(self):
        player = self.player.sprite
        if player.hp < -10:
            self.over = True

    # PLAYER ACTIONS
    def shoot(self,player):
        
        current_time = pygame.time.get_ticks()
        if current_time - player.last_shoot_time > player.bullet_cooldown * 1000:
            bullet = Bullet(player.rect,[self.visuals,self.projectile_spritess])
            
            player.last_shoot_time = current_time

    

    def secondary_shot(self):
        player = self.player.sprite
        current_time = pygame.time.get_ticks()
        if current_time - player.last_s_time > player.s_cooldown * 1000:
            bullet = D_Bullet(self.player.sprite.rect,[self.visuals,self.projectile_spritess])
            player.last_s_time = current_time

    def call_support(self):
        player = self.player.sprite
        if player.support_active:
            support = Support((player.rect.x - 70,player.rect.y + 80),[self.visuals,self.entities],self.shoot,self.secondary_shot,self.call_support)
            exhaust = Particles((support.rect.x,support.rect.y),[self.visuals],'Exhaust1')
        else:
            support = Support((player.rect.x - 70,player.rect.y - 80),[self.visuals,self.entities],self.shoot,self.secondary_shot,self.call_support)
            exhaust = Particles((support.rect.x,support.rect.y),[self.visuals],'Exhaust1')
    # ==============
    # ENEMY ACTIONS
    def enemy_shoot(self,enemy,vector):
        current_time = pygame.time.get_ticks()
        if current_time - enemy.last_shoot_time > enemy.bullet_cooldown * 1000:
            bullet = Enemy_Shot((enemy.rect.x,enemy.rect.y),[self.visuals],vector)
            enemy.last_shoot_time = current_time

    def trigger_death(self,entity):
        if entity.hp < 1:
            dead = Particles((entity.rect.x,entity.rect.y),[self.visuals],'Explosion3')
            reward = Power_Up((entity.rect.x,entity.rect.y),[self.visuals,self.rewards],'power_up')
            entity.kill()

    # ==============
    # REWARDS AND MISC 
    def handle_reward(self):
        player = self.player.sprite

        for sprite in self.rewards.sprites():
            if sprite.rect.colliderect(player.hitbox):
                sprite.action(player)

    # ==============    

    def run(self):
        player = self.player.sprite
        self.visuals.custom_draw(player)
        self.visuals.update(player)
        self.collisions(player)
        self.check_gameover()
        self.projectile_collision()
        self.handle_reward()
        



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


