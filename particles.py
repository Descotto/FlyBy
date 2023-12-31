import pygame
from support import *

class Particles(pygame.sprite.Sprite):
    def __init__(self,pos,group,particle_type,extra=None):
        super().__init__(group)
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.extra = extra
        self.particle_type = particle_type
        if particle_type == 'missile':
            self.particle_type = 'Explosion1'
        if particle_type == 'boss_shot':
            self.particle_type = 'mega_explosion'
        self.image = self.animations[self.particle_type][self.frame_index]
        if self.particle_type == 'bubble':
            self.hp = 10
        
        
        self.rect = self.image.get_rect(center =pos)
        if self.particle_type in ['Exhaust1', 'Exhaust2', 'Exhaust3']:
            self.rect.x -= 10
            self.rect.y += 30

        self.hitbox = self.rect.copy()
        if self.particle_type == 'bubble':
            self.radius = 58  # Adjust the radius according to your needs
            self.hitbox_center = pygame.math.Vector2(self.rect.center)
            self.hitbox_radius = self.radius

    def import_assets(self):
        particles_path = 'Assets/particles/'
        self.animations = {
            'Exhaust1':[],
            'Exhaust2':[],
            'Exhaust3':[],
            'Explosion1':[],
            'Explosion2': [],
            'Explosion3':[],
            'mega_explosion': [],
            'Shot1':[],
            'Shot2':[],
            'Shot3':[],
            'Shot4':[],    
            'Shot5':[],
            'Shot6':[],
            'Shot7':[],
            'bubble':[]}

        for animation in self.animations.keys():
            full_path = particles_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.particle_type]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.particle_type in ['bubble']:
                self.frame_index -= 1
            else:
                self.frame_index = 0
            if self.particle_type in [
                'Explosion1','Explosion2','Explosion3','mega_explosion',
                'Shot1','Shot2','Shot3','Shot4','Shot5','Shot6','Shot7']:
                self.kill()

        self.image = animation[int(self.frame_index)]
        

        # set the rect
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def keep_rect_pos(self,player):
        if self.particle_type in ['Exhaust1', 'Exhaust2', 'Exhaust3', 'bubble']:
            self.rect.x += player.speed * player.direction.x
            self.rect.y += player.speed * player.direction.y
            # update the hitbox after updating the rect
            if self.particle_type == 'bubble':
                self.hitbox = self.rect.inflate(-22,-22)

            self.hitbox.center = player.rect.center
            self.hitbox_center = player.rect.center
            
    def take_damage(self,amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
    

    def update(self,player):
        self.animate()
        self.keep_rect_pos(player)
        
        if self.extra:
            self.extra(self)

        if self.particle_type == 'bubble':
            player.shield_hp = self.hp
            

        

   
        