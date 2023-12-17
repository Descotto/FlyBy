import pygame


class Cannon(pygame.sprite.Sprite):
    def __init__(self,pos,group,shoot):
        super().__init__(group)
        self.image = pygame.image.load('./Assets/enemies/cannon/cannon.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-32)
        self.shoot = shoot

        # cooldowns
        self.bullet_cooldown = 0.7
        self.last_shoot_time = 0

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 550:
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
        
        return (distance,direction)
    
    def update(self,player):
        self.get_player_distance_direction(player)