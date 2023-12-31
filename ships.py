import pygame
from enemy import Enemy

class Ship1(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/0/Ship1.png').convert_alpha()
        self.left_img = self.image
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.name = 'Kazi-Vir'
        self.moving = True
        self.speed = 7
        self.hp = 1
        self.weapon = self.inv['stun']
        self.bullet_type = self.weapon['type']
        self.bullet_cooldown = self.weapon['fire_rate']


        

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
                self.image = self.flip
            else:
                self.image = self.left_img
        elif distance < 900 and self.moving:
            direction = (player_vec - enemy_vec).normalize()
            self.direction = pygame.math.Vector2(direction)
            if self.direction.x > 0:
                self.direction.x = 3.5
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
            self.direction = pygame.math.Vector2(0,0)
        
        return (distance,direction)
    
    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.get_player_distance_direction(player)
        #self.adjust_dir()
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
        self.hp = 4
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-64,-96)
        self.weapon = self.inv['matter']
        self.bullet_type = self.weapon['type']
        self.bullet_cooldown = self.weapon['fire_rate']

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 650:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            self.direction = pygame.math.Vector2(2,0)
        elif distance < 900 and self.moving:
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
            self.direction = pygame.math.Vector2(0,0)
        
        return (distance,direction)
    
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
        self.speed = 5
        self.hp = 4
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-64,-96)
        self.weapon = self.inv['flux']
        self.bullet_type = self.weapon['type']
        self.bullet_cooldown = self.weapon['fire_rate']

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 650:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            self.direction = pygame.math.Vector2(2,0)
        elif distance < 900 and self.moving:
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
            
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
        

class Ship4(Enemy):
    def __init__(self,pos,group,shoot,trigger_death):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/3/Ship4.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.moving = True
        self.speed = 3
        self.hp = 6
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,-96)
        self.weapon = self.inv['speed']
        self.bullet_type = self.weapon['type']
        self.bullet_cooldown = self.weapon['fire_rate']

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 650:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            self.direction = pygame.math.Vector2(1,0)
        elif distance < 900 and self.moving:
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
            
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
        

class Boss(Enemy):
    def __init__(self,pos,group,shoot,trigger_death,support):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load('./Assets/enemies/boss/boss_body.png').convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        self.image = self.flip
        self.support = support
        self.moving = True
        self.speed = 2
        self.hp = 7
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,0)
        self.weapon = self.inv['boss_shot']
        self.bullet_type = self.weapon['type']
        self.bullet_cooldown = self.weapon['fire_rate']
        self.call_support_cooldown = 10
        self.call_support_timer = 0

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 350:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            self.direction = pygame.math.Vector2(1,0)
        elif distance < 1000 and self.moving:
            direction = pygame.math.Vector2(-2,0)
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
                
                self.support(self)
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
            self.direction = pygame.math.Vector2(0,0)
        
        return (distance,direction)
    
    def boss_reward(self,player):
        if self.hp <= 2:
            player.wepaon_vault.append('boss_shot')
        self.trigger_death(self)

    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.get_player_distance_direction(player)
        self.boss_reward(player)


# =================================================================================================
        

class Boss_Arm(Enemy):
    def __init__(self,pos,group,shoot,trigger_death,boss,image):
        super().__init__(pos,group,shoot,trigger_death)
        self.image = pygame.image.load(image).convert_alpha()
        self.flip = pygame.transform.flip(self.image, True,False)
        
        self.boss = boss
        self.moving = True
        self.speed = self.boss.speed
        self.hp = 4
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(10,-5)
        self.weapon = self.inv['mass']
        self.bullet_type = self.weapon['type']
        self.bullet_cooldown = self.weapon['fire_rate']

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.topright)
        distance = (player_vec - enemy_vec).magnitude()
        # enemy_vec.distance_to(player_vec)
        
        if distance < 150:
            self.moving = True
            direction = (player_vec - enemy_vec).normalize()
            
        elif distance < 900 and self.moving:
            direction = (player_vec - enemy_vec).normalize()
            if player.rect.x < self.rect.x:
                self.shoot(self,direction)
            
        else:
            
            direction = pygame.math.Vector2(-1,0)
            
        
        return (distance,direction)
    
    def track_boss_hp(self):
        if self.boss.hp <= 0:
            self.hp = 0

    def update(self,player):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        self.hitbox.center = self.rect.center
        self.direction = self.boss.direction
        self.get_player_distance_direction(player)
        self.trigger_death(self)
        self.track_boss_hp()



