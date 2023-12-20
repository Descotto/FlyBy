import pygame
import os
from random import randint
from settings import *
from player import *
from tiles import Tile
from bullet import *
from cannon import Cannon
from ships import *
from power_ups import Power_Up
from particles import Particles
from ui import UI

class Level:
    def __init__(self,surface,area):
        self.area = area
        self.next_lv = False
        self.display_surface = surface
        self.level_setup()
        self.over = False
        # self.play_music('./Assets/midi/EnterSandman.mp3')
        self.ui = UI()
        
        

    def level_setup(self):
        self.shield_sprites = pygame.sprite.Group()
        self.visuals = YSortCameraGroup(self.area,self.shield_sprites)
        self.obstacle_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.driver = pygame.sprite.GroupSingle()
        self.entities = pygame.sprite.Group()
        self.leve_up_sprites = pygame.sprite.Group()
        self.rewards = pygame.sprite.Group()

        maps = MAP_LAYOUTS[f'map_{self.area}']
        
        for style,map in maps.items():
            for row_index, row in enumerate(map):
                for col_index, cell in enumerate(row):

                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if cell != '-1':
                        if style == 'floor':
                            tile = Tile((x,y), [self.obstacle_sprites])
                        if style == 'to_next':
                            tile = Tile((x,y), [self.leve_up_sprites])
                            # CREATING PLAYER 
                        if style == 'player': 
                            player_one = Player(
                                (x,y),
                                [self.visuals,self.player],
                                self.shoot,
                                self.secondary_shot,
                                self.call_support,
                                self.shield)
                            player_one.support = True
                            exhaust = Particles((x,y),[self.visuals],'Exhaust1')
                            # DRIVER
                        if style == 'driver':
                            driver = Driver(
                                (x,y),
                                [self.driver],
                                self.shoot,
                                self.secondary_shot,
                                self.call_support,
                                self.shield)

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
        for bullet in self.projectile_sprites.sprites():
            for obstacle in self.obstacle_sprites.sprites():
                if obstacle.rect.colliderect(bullet.rect):
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

            for entity in self.entities.sprites():
                if entity.rect.colliderect(bullet.rect):
                    entity.take_damage()
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

                #for projectile in self.enemy_bullets.sprites():
                #     if projectile.rect.colliderect(bullet.rect):
                #         projectile.speed -= 2

    def enemy_projectile_collision(self):
        for bullet in self.enemy_bullets.sprites():
            for obstacle in self.obstacle_sprites.sprites():
                if obstacle.rect.colliderect(bullet.rect):
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

            for entity in self.entities.sprites():
                if entity.rect.colliderect(bullet.rect):
                    entity.take_damage()
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

            for shield in self.shield_sprites.sprites():
                if shield.rect.colliderect(bullet.rect):
                    shield.take_damage()
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

    def check_gameover(self):
        player = self.player.sprite
        if player.hp < -10:
            self.over = True

    # PLAYER ACTIONS
    def shoot(self,player):
        
        current_time = pygame.time.get_ticks()
        if current_time - player.last_shoot_time > player.bullet_cooldown * 1000:
            bullet = Bullet(player.rect,[self.visuals,self.projectile_sprites],'Shot1')
            
            player.last_shoot_time = current_time

    def secondary_shot(self):
        player = self.player.sprite
        current_time = pygame.time.get_ticks()
        if current_time - player.last_s_time > player.s_cooldown * 1000:
            bullet = D_Bullet(self.player.sprite.rect,[self.visuals,self.projectile_sprites])
            player.last_s_time = current_time

    def call_support(self):
        player = self.player.sprite
        
        support1 = Support((player.rect.x - 70,player.rect.y + 80),[self.visuals,self.entities],self.shoot,self.secondary_shot,self.call_support,self.shield)
        exhaust = Particles((support1.rect.x,support1.rect.y),[self.visuals],'Exhaust1',support1.on_death)
        support2 = Support((player.rect.x - 70,player.rect.y - 80),[self.visuals,self.entities],self.shoot,self.secondary_shot,self.call_support,self.shield)
        exhaust2 = Particles((support2.rect.x,support2.rect.y),[self.visuals],'Exhaust1',support2.on_death)
        
    def shield(self):
        player = self.player.sprite
        shield = Particles((player.rect.centerx,player.rect.centery),[self.shield_sprites,self.visuals], 'bubble')
    # ==============
    # ENEMY ACTIONS
    def enemy_shoot(self,enemy,vector):
        current_time = pygame.time.get_ticks()
        if current_time - enemy.last_shoot_time > enemy.bullet_cooldown * 1000:
            bullet = Enemy_Shot(enemy.rect,[self.visuals,self.enemy_bullets],vector,enemy.bullet_type)
            enemy.last_shoot_time = current_time

    def trigger_death(self,entity):
        if entity.hp < 1:
            dead = Particles((entity.rect.x,entity.rect.y),[self.visuals],'mega_explosion')
            random_number = randint(1,20)
            if random_number < 8 and random_number > 4:
                reward_option = {'1': {'name': 'power_up'}, '2': {'name': 'hp_up'}}
                pick = randint(1,2)
                
                reward = Power_Up((entity.rect.x,entity.rect.y),[self.visuals,self.rewards],reward_option[str(pick)]['name'])
            entity.kill()

    # ==============
    # REWARDS AND MISC 
    def handle_reward(self):
        player = self.player.sprite

        for sprite in self.rewards.sprites():
            if sprite.rect.colliderect(player.hitbox):
                sprite.action(player)

    def handle_area(self):
        player = self.player.sprite
        for sprite in self.leve_up_sprites.sprites():
            if sprite.rect.colliderect(player.hitbox):
                self.next_lv = True

    def shield_collision(self):
        for bullet in self.enemy_bullets.sprites():
            for shield in self.shield_sprites.sprites():
                if shield.hitbox.colliderect(bullet.hitbox):
                    shield.take_damage()
                    bullet.kill()
                


                    

    # ==============    

    def run(self):
        player = self.player.sprite
        driver = self.driver.sprite
        self.visuals.custom_draw(driver)
        self.visuals.update(player)
        self.driver.update()
        self.collisions(player)
        self.check_gameover()
        self.projectile_collision()
        self.handle_reward()
        self.ui.display(player)
        self.handle_area()
        self.enemy_projectile_collision()
        self.shield_collision()
        



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self,area,shield_sprites):

        super().__init__()
        self.area = area
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 7 
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.shield_sprites = shield_sprites

        #CREATE FLOOR
       
        self.floor_surf = pygame.image.load(MAP_URL[f'map_{self.area}']['url']).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = 0
        # self.offset.y = player.rect.centery - self.half_height

        # draw floor
        floor_upset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_upset_pos)


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

            if hasattr(sprite, 'hitbox'):
                hitbox_offset_pos = sprite.hitbox.topleft - self.offset
                hitbox_rect = pygame.Rect(hitbox_offset_pos, sprite.hitbox.size)
                pygame.draw.rect(self.display_surface, (255, 255, 255), hitbox_rect, 2)

        for sprite in self.shield_sprites:
            if hasattr(sprite, 'hitbox_center'):
                # Use sprite.hitbox_center as a Vector2
                hitbox_offset_pos = sprite.hitbox_center - pygame.math.Vector2(self.offset, 0)
                
                # Convert the hitbox_offset_pos to a tuple (x, y) for pygame.Rect
                hitbox_rect = pygame.Rect(hitbox_offset_pos.x, hitbox_offset_pos.y, sprite.rect.size[0], sprite.rect.size[1])

                # Draw the circle using the hitbox center and radius
                pygame.draw.circle(self.display_surface, (255, 255, 255), hitbox_rect.topleft, sprite.hitbox_radius, 2)


                
                


            
                