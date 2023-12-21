import pygame
from enemy import Enemy

class Ship1(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/0/Ship1.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.name = 'Kazi-Vir'
        self.moving = True
        self.speed = 5
        self.hp = 1
        self.bullet_type = 'Shot2'
        




    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 650:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
        elif distance < 900 and self.moving:
            direction = (player_vec - enemy_vec).normalize()
            self.direction = pygame.math.Vector2(direction)
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
            self.direction = pygame.math.Vector2(0,0)
        
        return (distance,direction)
    

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
        self.bullet_type = 'Shot4'







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
        self.hp = 5
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,-96)
        self.bullet_type = 'Shot6'


    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 650:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
        elif distance < 900 and self.moving:
            direction = pygame.math.Vector2(2.5,0)
            self.direction = pygame.math.Vector2(direction)
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
            self.direction = pygame.math.Vector2(0,0)
        
        return (distance,direction)
    

    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.get_player_distance_direction(player)
        self.trigger_death(self)

