import pygame
from support import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,group,size=64):
        super().__init__(group)

        
        self.image = pygame.Surface((size,size), pygame.SRCALPHA)
        alpha_value = 0
        self.image.fill((0,0,255, alpha_value))
            
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        


    def update(self,player):
        pass