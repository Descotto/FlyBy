import pygame


class Cannon(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('./Assets/enemies/cannon/cannon.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.rect = self.image.get_rect(topleft = pos)

    def update(self):
        pass