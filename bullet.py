import pygame
import math
from support import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,group):
        super().__init__(group)
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        # enemies
        self.damage = 1
        self.speed = 10

        # bullet type
        self.type = 'Shot1'
        
        

        # Set the dimensions and color of the bullet
        self.width = 5
        self.height = 5
        self.image = self.image = self.animations[self.type][self.frame_index]
        self.direction = pygame.math.Vector2(1,0)
        # Set the initial position of the bullet based on the player's position
 
        self.rect = self.image.get_rect(midleft=(player_rect.x +70, player_rect.y + 32))
       
    def import_bullet_assets(self):
        bullet_path = 'Assets/bullets/'
        self.animations = {'Shot1':[], 'Shot2':[], 'Shot3':[], 'Shot4':[], 'Shot5':[], 'Shot6':[]}

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

    def update(self,player):
        # Move the bullet horizontally
        self.rect.x += self.speed * self.direction.x
        self.animate()

class D_Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,group):
        super().__init__(group)
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.damage = 1
        self.speed = 16
        self.gravity = 0.5
        self.type = 'Shot4'
        

        # Set the dimensions and color of the bullet
        self.width = 5
        self.height = 5
        self.image = self.animations[self.type][self.frame_index]
        self.direction = pygame.math.Vector2(2,1)
        self.rect = self.image.get_rect(midleft=(player_rect.x +57, player_rect.y + 32))

    def import_bullet_assets(self):
        bullet_path = 'Assets/bullets/'
        self.animations = {'Shot1':[], 'Shot2':[], 'Shot3':[], 'Shot4':[], 'Shot5':[], 'Shot6':[]}

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

    def add_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self,player):
        # Move the bullet in an angle
        self.rect.x += self.speed * self.direction.x
        self.add_gravity()
        self.add_gravity()
        self.animate()

class Enemy_Shot(pygame.sprite.Sprite):
    def __init__(self,enemy_rect,group,vector):
        super().__init__(group)
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        # enemies
        self.damage = 1
        self.speed = 10

        self.type = 'Shot2'
        self.damage = 2
        self.speed = 5
        self.direction = pygame.math.Vector2(vector)
       
        # Set the dimensions and color of the bullet
        self.width = 5
        self.height = 5
        self.image = self.image = self.animations[self.type][self.frame_index]
        self.rect = self.image.get_rect(topright = enemy_rect.topleft)

    def import_bullet_assets(self):
        bullet_path = 'Assets/bullets/'
        self.animations = {'Shot1':[], 'Shot2':[], 'Shot3':[], 'Shot4':[], 'Shot5':[], 'Shot6':[]}

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


    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.animate()