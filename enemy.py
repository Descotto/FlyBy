import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(group)
        self.direction = pygame.math.Vector2(0,0)
        self.image = self.image = pygame.Surface((64,64))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-32)
        
        self.shoot = shoot
        self.trigger_death = trigger_death
        self.bullet_type = 'Shot2'

        # stats
        self.hp = 2

        # cooldowns
        self.moving = False
        self.bullet_cooldown = 2
        self.last_shoot_time = 0
        self.last_vulnerable = 0
        self.vulnerable_cooldown = 0.1

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 650:
            self.moving = False
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
    
    def take_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_vulnerable > self.vulnerable_cooldown * 1000:
            self.hp -= 1
            self.last_vulnerable = current_time
