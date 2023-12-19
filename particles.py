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
        self.image = self.animations[self.particle_type][self.frame_index]
        
        
        self.rect = self.image.get_rect(center =pos)
        if self.particle_type == 'Exhaust1':
            self.rect.x -= 10
            self.rect.y += 30



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
            'Shot7':[]}

        for animation in self.animations.keys():
            full_path = particles_path + animation
            
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.particle_type]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = -1
            if self.particle_type != 'Exhaust1':
                self.kill()

        self.image = animation[int(self.frame_index)]
        

        # set the rect
        self.rect = self.image.get_rect(center = self.rect.center)

    def keep_rect_pos(self,player):
        if self.particle_type == 'Exhaust1':
            self.rect.x += player.speed * player.direction.x
            self.rect.y += player.speed * player.direction.y



    def update(self,player):
        self.animate()
        self.keep_rect_pos(player)
        if self.extra:
            self.extra(self)
   
        