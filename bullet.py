import pygame
import math
from support import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,group,type, bullet_damage,speed):
        super().__init__(group)
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        # enemies
        self.damage = bullet_damage
        self.speed = speed

        # bullet type
        self.type = type
        
        

        # Set the dimensions and color of the bullet
        self.width = 5
        self.height = 5
        self.image = self.image = self.animations[self.type][self.frame_index]
        self.direction = pygame.math.Vector2(1,0)
        # Set the initial position of the bullet based on the player's position
 
        self.rect = self.image.get_rect(midleft=(player_rect.x +70, player_rect.y + 32))
        if self.type == 'Shot1':
            self.hitbox = self.rect.inflate(-25,-25)
        elif self.type in ['Shot5','Shot6']: 
            self.hitbox = self.rect.inflate(-120,-120)
        elif self.type == 'Shot7':
            self.hitbox = self.rect.inflate(-16,-16)
        else:
            self.hitbox = self.rect.inflate(-52,-52)
       
    def import_bullet_assets(self):
        bullet_path = 'Assets/bullets/'
        self.animations = {'Shot1':[], 'Shot2':[], 'Shot3':[], 'Shot4':[], 'Shot5':[], 'Shot6':[], 'Shot7': []}

        for animation in self.animations.keys():
            full_path = bullet_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.type]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        self.image = image

    def check_offscreen(self,player):
        start_position = player.rect.x
        if self.direction:
            if self.rect.x >= (start_position + 1000): 
                self.kill()
             

    def update(self,player):
        # Move the bullet horizontally
        self.rect.x += self.speed * self.direction.x
        self.hitbox.center = self.rect.center
        self.animate()
        self.check_offscreen(player)

class D_Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,group):
        super().__init__(group)
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.damage = 3
        self.speed = 16
        self.gravity = 0.5
        self.on_ground = False
        self.type = 'missile'
        self.status = 'fall'
        

        # Set the dimensions and color of the bullet
        self.width = 5
        self.height = 5
        self.image = self.animations[self.status][self.frame_index]
        self.direction = pygame.math.Vector2(0.5,0)
        self.rect = self.image.get_rect(midleft=(player_rect.x + 20, player_rect.y + 50))
        self.hitbox = self.rect.inflate(-10,-10)

    def import_bullet_assets(self):
        bullet_path = 'Assets/bullets/missile/'
        self.animations = {'fall':[], 'run':[], 'ignite':[],}

        for animation in self.animations.keys():
            full_path = bullet_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        self.image = image

    def add_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def  get_status(self):
        if self.on_ground:
            self.status = 'run'
            self.gravity = 0
            self.direction = pygame.math.Vector2(1,0)
            self.speed += 0.3
        else:
            self.status = 'fall'


    def update(self,player):
        # Move the bullet in an angle
        self.rect.x += self.speed * self.direction.x
        self.hitbox.center = self.rect.center
        self.add_gravity()
        self.get_status()

        self.animate()

class Enemy_Shot(pygame.sprite.Sprite):
    def __init__(self,enemy_rect,group,vector,type="Shot3"):
        super().__init__(group)
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        # enemies
        self.damage = 1
        self.speed = 10

        self.type = type
        self.damage = 1
        self.speed = 5
        self.direction = pygame.math.Vector2(vector)
       
        # Set the dimensions and color of the bullet
        self.width = 5
        self.height = 5
        self.image = self.image = self.animations[self.type][self.frame_index]
        
        
        self.rect = self.image.get_rect(topright = enemy_rect.topleft)
        
        if self.type == 'Shot1':
            self.hitbox = self.rect.inflate(-25,-25)
        elif self.type in ['Shot5','Shot6']:
            self.hitbox = self.rect.inflate(-120,-120)
        elif self.type == 'Shot7':
            self.hitbox = self.rect.inflate(-16,-16)
        elif self.type == 'boss_shot':
            self.hitbox = self.rect.inflate(-50,0)
        else:
            self.hitbox = self.rect.inflate(-52,-52)
        
    def import_bullet_assets(self):
        bullet_path = 'Assets/bullets/'
        self.animations = {'Shot1':[], 'Shot2':[], 'Shot3':[], 'Shot4':[], 'Shot5':[], 'Shot6':[],'Shot7': [], 'boss_shot': []}

        for animation in self.animations.keys():
            full_path = bullet_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.type]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        self.image = image
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip

    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.midleft
        self.animate()

class enemy_stunt_shot(Enemy_Shot):
    def __init__(self,enemy_rect,group,vector,type="Shot3"):
        super().__init__(self,enemy_rect,group,vector,type='Shot3')
        self.speed = 20

    def update(self):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.midleft
        self.animate()

class Boss_Shot(Enemy_Shot):
    def __init__(self,enemy_rect,group,vector,type,pos):
        super().__init__(enemy_rect,group,vector,type)
        self.rect = self.image.get_rect(center = pos)

    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.midleft
        self.animate()