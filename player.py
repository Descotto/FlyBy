import pygame
from support import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group,shoot,s_shot,call_support,call_backup,shield):
        super().__init__(group)
        # setup
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-32)
        self.shoot = shoot
        self.s_shoot = s_shot
        self.shield = shield
        self.call_support = call_support
        self.call_backup = call_backup
        self.support_available = True
        self.support_active = False
        self.shield_ready = False
        self.shield_active = False
        self.shield_charging = False
        self.shield_hp = 0
        self.encounter = False
        self.charging_weapon = False
        self.critical_charge = False
        
        
        


        # movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 3
        self.status = 'idle'

        # stats
        self.hp = 10
        self.lives = 5
        self.weapons_owned = ['gravity','toxic']
        self.track_equipped = 0
        self.main_weapon = WEAPONS[self.weapons_owned[self.track_equipped]]
        self.secondary_weapon = WEAPONS['gravity']
        self.capacity = self.main_weapon['capacity']
        self.bullet_type = self.main_weapon['type']

        # progress
        self.level = 0
        self.salvage = 0
        self.wepaon_vault = ['gravity','toxic','speed','matter','mass','flux']
        

        # cooldowns
        self.bullet_cooldown = self.main_weapon['fire_rate']
        self.last_shoot_time = 0
        self.s_cooldown = 0.9
        self.last_s_time = 0
        self.vulnerable_cooldown = 0.2
        self.last_vulnerable = 0
        self.shield_timer = 0
        self.shield_clock = pygame.time.Clock()
        self.ammo_timer = pygame.time.get_ticks()
        self.switch_timer = pygame.time.get_ticks()
        

    def import_character_assets(self):
        character_path = 'Assets/player/'
        self.animations = {'idle':[], 'up':[], 'down':[], 'dead':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index -= 1
            if self.status == 'dead':
                self.frame_index = 0
                

        image = animation[int(self.frame_index)]
      
        self.image = image
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # set the rect
        
    def input(self):
        pygame.joystick.init()
        # Get the number of available joysticks
        
        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_UP]:
            self.direction.y = -2
        elif keys[pygame.K_DOWN]:
            self.direction.y = 2
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 3
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            if self.encounter:
                self.direction.x = 0
            else:
                self.direction.x = 1

        if keys[pygame.K_SPACE]:
            if self.status != 'dead':
                self.shoot(self)
        if keys[pygame.K_x]:
            if self.status != 'dead':
                self.s_shoot()
        if keys[pygame.K_s]:
            if self.status != 'dead' and self.support_available:
                if self.support_available:
                    self.support_available = False
                    self.call_support()
                    self.support_active = True

        # Check screen boundaries
        
        if self.rect.top < 0:
            self.direction.y = 1
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.direction.y = -1
                    

        if keys[pygame.K_a]:
            if self.shield_ready:
                self.shield_ready = False
                self.shield()
                self.shield_active = True
        if keys[pygame.K_o]:
            current_time = pygame.time.get_ticks()
            if current_time - self.switch_timer >= 1500:
                if self.track_equipped + 1 < len(self.weapons_owned):
                    self.track_equipped += 1
                    self.switch_weapon()
                else:
                    self.track_equipped = 0
                    self.switch_weapon()  # Call a method to handle weapon switching
                self.switch_timer = current_time
            else:
                self.switch_timer = current_time

        if keys[pygame.K_z]:
            if self.salvage >= 100:
                self.handle_salvage()

                                     
    def get_status(self):
        if self.hp <= 1:
            self.status = 'dead'
            self.hp -= 0.3
        elif self.direction.y < 0:
            self.status = 'up'
        elif self.direction.y > 0:
            self.status = 'down'
        else:
            self.status = 'idle'

    def take_damage(self,amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_vulnerable > self.vulnerable_cooldown * 1000:
            self.hp -= amount
            self.last_vulnerable = current_time

    def update_shield_hp(self):
        # Get the time elapsed since the last frame in milliseconds
        delta_time = self.shield_clock.tick(60) / 1000.0  
        # Increment the timer
        self.shield_timer += delta_time
        if self.shield_hp <= 1:
            self.shield_charging = True
            
        if self.shield_charging:
        # Check if 1 second has passed
            if self.shield_timer >= 1.0:
                # Reset the timer
                self.shield_timer -= 1.0
                # Add 1 to shield_hp
                self.shield_hp += 1
            if self.shield_hp >= 10:
                self.shield_ready = True
                self.shield_charging = False

    def update_ammo(self):
        if self.charging_weapon:
            # Check if a second has passed
            current_time = pygame.time.get_ticks()
            if current_time - self.ammo_timer >= 3000:  # 1000 milliseconds = 1 second
                # Increment ammo if it's less than max_ammo
                if self.capacity <= self.main_weapon['capacity']:
                    self.capacity += 1
                self.ammo_timer = current_time  # Reset the timer
        else:
            pass

    def track_charging(self):
        if self.capacity < self.main_weapon['capacity']:
            self.charging_weapon = True
            if self.capacity <= 0:
                self.critical_charge = True
        elif self.capacity >= self.main_weapon['capacity']:
            self.charging_weapon = False
            self.critical_charge = False

    def switch_weapon(self):
        self.main_weapon = WEAPONS[self.weapons_owned[self.track_equipped]]

    def handle_salvage(self):
        if self.salvage >= 100:
            self.salvage = 0
            self.level += 1
            self.weapons_owned.extend(self.wepaon_vault[self.level:])

    def update(self,player):
        self.hitbox.center = self.rect.center
        self.input()
        self.animate()
        self.get_status()
        self.update_shield_hp()
        self.update_ammo()
        self.track_charging()

class Support(Player):
    def __init__(self,pos,group,shoot,s_shot,call_support,call_backup,shield):
        super().__init__(pos,group,shoot,s_shot,call_support,call_backup,shield)
        self.hp = 2
        self.support_available = False
        self.shoot = shoot
        self.status = 'idle'
        


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.shoot(self)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index -= 1
            if self.status == 'dead':
                self.frame_index = 0
                self.kill()

        image = animation[int(self.frame_index)]
      
        self.image = image
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # set the rect
        
    def on_death(self,particle):
        if self.hp <= 0:
            particle.kill()

    def update(self,player):
        self.hitbox.center = self.rect.center
        self.input()
        self.animate()
        self.get_status()
        self.update_ammo()
        self.direction = player.direction
        self.rect.x += player.speed * player.direction.x
        self.rect.y += player.speed * player.direction.y

class Backup(Player):
    def __init__(self,pos,group,shoot,s_shot,call_support,call_backup,shield):
        super().__init__(pos,group,shoot,s_shot,call_support,call_backup,shield)
        self.hp = 20
        self.support_available = False
        self.shoot = shoot
        self.status = 'idle'
        self.image = pygame.image.load('./Assets/back_up/1.png')
        self.decay_cooldown = 0.5
        self.last_decay = 0


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot(self)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index -= 1
            if self.status == 'dead':
                self.frame_index = 0
                self.kill()

        image = animation[int(self.frame_index)]
      
        self.image = image
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # set the rect
        
    def on_death(self,particle):
        if self.hp <= 0:
            particle.kill()

    def decay(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_decay > self.decay_cooldown * 1000:
            self.hp -= 0.5
            self.last_decay = current_time
        if self.hp <= 0:
            self.kill()

    def update(self,player):
        self.hitbox.center = self.rect.center
        self.input()
        self.get_status()
        self.update_ammo()
        self.decay()
        self.direction = player.direction
        self.rect.x += player.speed * player.direction.x
        self.rect.y += player.speed * player.direction.y

class Driver(Player):
    def __init__(self,pos,group,shoot,s_shot,call_support,call_backup,shield):
        super().__init__(pos,group,shoot,s_shot,call_support,call_backup,shield)
        self.direction = pygame.math.Vector2(1,0)


    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed