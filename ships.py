import pygame
from enemy import Enemy

class Ship1(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/0/Ship1.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.moving = True
        self.speed = 2






    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.get_player_distance_direction(player)
        self.trigger_death(self)


# =================================================================================================
        

class Ship2(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/1/Ship2.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.moving = True
        self.speed = 1
        self.hp = 5
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-64,-96)






    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center= self.rect.center
        self.get_player_distance_direction(player)
        self.trigger_death(self)



# =================================================================================================
        

class Ship3(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/2/Ship3.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.moving = True
        self.speed = 2
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-64,-96)


    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.get_player_distance_direction(player)
        self.trigger_death(self)


# =================================================================================================
        

class Ship4(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/3/Ship4.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.moving = True
        self.speed = 2
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,-96)


    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.get_player_distance_direction(player)
        self.trigger_death(self)

