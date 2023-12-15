import pygame
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group,shoot,s_shot):
        super().__init__(group)

        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-32)
        self.shoot = shoot
        self.s_shoot = s_shot


        # movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.status = 'idle'

        # stats
        self.hp = 10

        

        # cooldowns
        self.bullet_cooldown = 0.5
        self.last_shoot_time = 0
        self.s_cooldown = 0.5
        self.last_s_time = 0

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
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 2
        elif keys[pygame.K_LEFT]:
            self.direction.x = 0.5
        else:
            self.direction.x = 1

        if keys[pygame.K_SPACE]:
            if self.status != 'dead':
                self.shoot()
        if keys[pygame.K_x]:
            if self.status != 'dead':
                self.s_shoot()

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
                
    def update(self):
        self.hitbox.center = self.rect.center
        self.input()
        self.animate()
        self.get_status()