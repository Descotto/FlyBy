import pygame
from support import *

class Power_Up(pygame.sprite.Sprite):
    def __init__(self,pos,group,type):
        super().__init__(group)
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.09
        self.type = type
        self.image = self.animations[self.type][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)



    def import_character_assets(self):
        character_path = 'Assets/power_ups/'
        self.animations = {'power_up':[],'hp_up':[],'salvage':[],'back_up':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.type]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
                

        image = animation[int(self.frame_index)]
      
        self.image = image
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # set the rect

    def action(self,player):
        if self.type == 'power_up':
            player.support_available = True
            self.kill()
        elif self.type == 'hp_up':
            player.hp = 10
            self.kill()
        elif self.type == 'salvage':
            player.salvage += 10
            self.kill()
        elif self.type == 'back_up':
            player.call_backup()

    def update(self,player):
        self.animate()