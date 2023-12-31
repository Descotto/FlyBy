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
    def __init__(self,surface,area,rec_stats,record_player):
        self.rec_stats = rec_stats
        self.record_player = record_player
        self.area = area
        self.next_lv = False
        self.display_surface = surface
        self.level_setup()
        self.over = False
        self.respawn = False
        self.started = False
        self.start_text = False
        self.ui = UI()
        
        

    def level_setup(self):
        self.shield_sprites = pygame.sprite.Group()
        self.visuals = YSortCameraGroup(self.area,self.shield_sprites)
        self.obstacle_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.missile_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.stun_bullets = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.support = pygame.sprite.Group()
        self.driver = pygame.sprite.GroupSingle()
        self.entities = pygame.sprite.Group()
        self.kazis = pygame.sprite.Group()
        self.leve_up_sprites = pygame.sprite.Group()
        self.threshold_sprites = pygame.sprite.Group()
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
                                self.call_backup,
                                self.shield)
                            player_one.support = True
                            player_one.salvage = self.rec_stats['salvage']
                            player_one.lives = self.rec_stats['lives']
                            player_one.weapons_owned = self.rec_stats['weapons']
                            exhaust = Particles((x,y),[self.visuals],'Exhaust1')
                            # DRIVER
                        if style == 'driver':
                            driver = Driver(
                                (x,y),
                                [self.driver],
                                self.shoot,
                                self.secondary_shot,
                                self.call_support,
                                self.call_backup,
                                self.shield)
                        if style == 'threshold':
                            threshold = Tile((x,y), [self.threshold_sprites])

                        if style == 'cannons':
                            cannon = Cannon((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy1':
                            ship = Ship1((x,y), [self.visuals,self.entities,self.kazis],self.stun_shot,self.trigger_death)
                        if style == 'enemy2':
                            ship = Ship2((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy3':
                            ship = Ship3((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'enemy4':
                            ship = Ship4((x,y), [self.visuals,self.entities],self.enemy_shoot,self.trigger_death)
                        if style == 'boss':
                            boss = Boss((x,y),[self.visuals,self.entities,self.obstacle_sprites],self.boss_shot,self.trigger_death,self.boss_support)
                            arm = Boss_Arm((boss.rect.x - 96,boss.rect.y + 70),[self.visuals,self.entities],self.enemy_shoot,self.trigger_death,boss,BOSS_ARM_UP_URL)
                            arm2 = Boss_Arm((boss.rect.x - 96,boss.rect.y + 126),[self.visuals,self.entities],self.enemy_shoot,self.trigger_death,boss,BOSS_ARM_DOWN_URL)

    def play_music(self):
        music_file = './Assets/midi/trooper.mp3'
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)

    def collisions(self,player):

        player.rect.x += player.direction.x * player.speed
        player.rect.y += player.direction.y * player.speed

        for sprite in self.obstacle_sprites.sprites():
            if sprite.rect.colliderect(player.hitbox):
                player.take_damage(5)

        for sprite in self.kazis.sprites():
            if sprite.hitbox.colliderect(player.hitbox):
                player.take_damage(2)
                sprite.take_damage(3)

        for bullet in self.stun_bullets.sprites():
            if bullet.hitbox.colliderect(player.hitbox):
                player.take_damage(bullet.damage)
      
    def projectile_collision(self):
        for bullet in self.projectile_sprites.sprites():
            for obstacle in self.obstacle_sprites.sprites():
                if obstacle.rect.colliderect(bullet.hitbox):
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

            for entity in self.entities.sprites():
                if entity.hitbox.colliderect(bullet.hitbox):
                    entity.take_damage(bullet.damage)
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()     

        for missile in self.missile_sprites.sprites():
            for entity in self.entities.sprites():
                if entity.hitbox.colliderect(missile.hitbox):
                    entity.take_damage(missile.damage)
                    particle = Particles((missile.rect.x,missile.rect.y),[self.visuals],missile.type)
                    missile.kill()   

            for obstacle in self.obstacle_sprites.sprites():
                if obstacle.rect.colliderect(missile.hitbox):
                    missile.on_ground = True
                    missile.rect.y = obstacle.rect.y - 20

    def enemy_projectile_collision(self,player):
        for bullet in self.enemy_bullets.sprites():
            for entity in self.support.sprites():
                if entity.hitbox.colliderect(bullet.hitbox):
                    entity.take_damage(bullet.damage)
                    particle = Particles((bullet.rect.x,bullet.rect.y),[self.visuals],bullet.type)
                    bullet.kill()

            for shield in self.shield_sprites.sprites():
                if shield.hitbox.colliderect(bullet.hitbox):
                    shield.take_damage(bullet.damage)
                    particle = Particles((bullet.hitbox.x,bullet.hitbox.y),[self.visuals],bullet.type)
                    bullet.kill()

            
            if bullet.hitbox.colliderect(player.hitbox):
                player.take_damage(bullet.damage)
                particle = Particles((bullet.hitbox.x,bullet.hitbox.y),[self.visuals],bullet.type)
                bullet.kill()

    def check_gameover(self):
        player = self.player.sprite
        if player.hp < -5:
            if player.lives > 0:
                player.lives -= 1
                self.respawn = True
                self.record_player(self,player)
            elif player.lives < 1:
                self.over = True

                
    # PLAYER ACTIONS
    def shoot(self,player):
        if not player.critical_charge:
            current_time = pygame.time.get_ticks()
            if current_time - player.last_shoot_time > player.bullet_cooldown * 1000:
                bullet = Bullet(player.rect,[self.visuals,self.projectile_sprites],player.main_weapon['type'],player.main_weapon['damage'],player.main_weapon['speed'])
                player.capacity -= 1
                player.last_shoot_time = current_time

    def secondary_shot(self):
        player = self.player.sprite
        current_time = pygame.time.get_ticks()
        if current_time - player.last_s_time > player.s_cooldown * 1000:
            bullet = D_Bullet(self.player.sprite.rect,[self.visuals,self.missile_sprites])
            player.last_s_time = current_time

    def call_support(self):
        player = self.player.sprite
        
        support1 = Support((player.rect.x - 70,player.rect.y + 80),[self.visuals,self.support],self.shoot,self.secondary_shot,self.call_support,self.call_backup,self.shield)
        exhaust = Particles((support1.rect.x,support1.rect.y),[self.visuals],'Exhaust1',support1.on_death)
        support2 = Support((player.rect.x - 70,player.rect.y - 80),[self.visuals,self.support],self.shoot,self.secondary_shot,self.call_support,self.call_backup,self.shield)
        exhaust2 = Particles((support2.rect.x,support2.rect.y),[self.visuals],'Exhaust1',support2.on_death)

    def call_backup(self):
        player = self.player.sprite
        
        backup1 = Backup((player.rect.x - 10,player.rect.y + 42),[self.visuals],self.shoot,self.secondary_shot,self.call_support,self.call_backup,self.shield)
        #exhaust = Particles((support1.rect.x,support1.rect.y),[self.visuals],'Exhaust1',support1.on_death)
        backup2 = Backup((player.rect.x - 10,player.rect.y - 15),[self.visuals],self.shoot,self.secondary_shot,self.call_support,self.call_backup,self.shield)
        #exhaust2 = Particles((support2.rect.x,support2.rect.y),[self.visuals],'Exhaust1',support2.on_death)

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

    def boss_shot(self,enemy,vector):
        current_time = pygame.time.get_ticks()
        if current_time - enemy.last_shoot_time > enemy.bullet_cooldown * 1000:
            bullet = Boss_Shot(enemy.rect,[self.visuals,self.enemy_bullets],vector,enemy.bullet_type,enemy.rect.topleft)
            bullet2 = Boss_Shot(enemy.rect,[self.visuals,self.enemy_bullets],vector,enemy.bullet_type,enemy.rect.bottomleft)
            enemy.last_shoot_time = current_time

    def boss_support(self,boss):
        current_time = pygame.time.get_ticks()
        if current_time - boss.call_support_timer  > boss.call_support_cooldown * 1000:
            ship1 = Ship1((boss.rect.x,boss.rect.y - 80), [self.visuals,self.entities,self.kazis],self.stun_shot,self.trigger_death)
            ship2 = Ship1((boss.rect.x,boss.rect.y + 310), [self.visuals,self.entities,self.kazis],self.stun_shot,self.trigger_death)
            boss.call_support_timer = current_time

    def stun_shot(self,enemy,vector):
        current_time = pygame.time.get_ticks()
        if current_time - enemy.last_shoot_time > enemy.bullet_cooldown * 1000:
            bullet = Enemy_Shot(enemy.rect,[self.visuals,self.enemy_bullets],vector,enemy.bullet_type)
            bullet.speed = 20
            bullet.damage = 0.5
            enemy.last_shoot_time = current_time

    def trigger_death(self,entity):
        if entity.hp < 1:
            dead = Particles((entity.rect.x,entity.rect.y),[self.visuals],'mega_explosion')
            random_number = randint(1,10)
            reward_option = {'1': {'name': 'hp_up'},
                                 '2': {'name': 'hp_up'},
                                 '3': {'name': 'power_up'},
                                 '4': {'name': 'power_up'},
                                 '5': {'name': 'salvage'},
                                 '6': {'name': 'salvage'},
                                 '7': {'name': 'salvage'},
                                 '8': {'name': 'salvage'},
                                 '9': {'name': 'salvage'},
                                 '10': {'name': 'salvage'},
                                 '11': {'name': 'salvage'},
                                 '12': {'name': 'salvage'},
                                 '13': {'name': 'salvage'},
                                 '14': {'name': 'power_up'},
                                 '15': {'name': 'back_up'}}
            
            if random_number < 10 and random_number > 3:
                pick = randint(1,15)
                
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
        driver = self.driver.sprite
        for sprite in self.leve_up_sprites.sprites():
            if sprite.rect.colliderect(driver.rect):
                self.record_player(self,player)
                self.next_lv = True

    def handle_threshold(self):
        driver = self.driver.sprite
        player = self.player.sprite
        for sprite in self.threshold_sprites.sprites():
            if sprite.rect.colliderect(driver.rect):
                driver.speed = 0
                player.encounter = True

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
        self.projectile_collision()
        self.handle_reward()
        self.ui.display(player)
        self.handle_area()
        #self.enemy_projectile_collision(player)
        #self.shield_collision()
        self.handle_threshold()
        



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
                #pygame.draw.rect(self.display_surface, (255, 255, 255), hitbox_rect, 2)

        for sprite in self.shield_sprites:
            if hasattr(sprite, 'hitbox_center'):
                # Use sprite.hitbox_center as a Vector2
                hitbox_offset_pos = sprite.hitbox_center - pygame.math.Vector2(self.offset, 0)
                
                # Convert the hitbox_offset_pos to a tuple (x, y) for pygame.Rect
                hitbox_rect = pygame.Rect(hitbox_offset_pos.x, hitbox_offset_pos.y, sprite.rect.size[0], sprite.rect.size[1])

                # Draw the circle using the hitbox center and radius
                #pygame.draw.circle(self.display_surface, (255, 255, 255), hitbox_rect.topleft, sprite.hitbox_radius, 2)


                
                


            
                