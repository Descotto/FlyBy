import pygame
from enemy import Enemy


class Cannon(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/cannon/cannon.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-12)
        self.shoot = shoot
        self.trigger_death = trigger_death

        # stats
        self.hp = 3

    def update(self,player):
        self.get_player_distance_direction(player)
        self.trigger_death(self)