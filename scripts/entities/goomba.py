import pygame, json
from .enemy import Enemy

class Goomba(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, [rect[0], rect[1]], f'{game.world_type}_goomba', 'moving')
        self.load_collision_rect()

    def update(self):
        super().update(self.die)

    def die(self):
        self.set_animation('die')
        self.dead = True
        self.stomp_sfx.play()

    def load_collision_rect(self):
        collision_rect = json.load(open('data/configs/collision_boxes/goomba.json', 'r'))['goomba']

        offset = [collision_rect['offset'][0]*self.scale, collision_rect['offset'][1]*self.scale]
        start_offset = [collision_rect['start_offset'][0]*self.scale, collision_rect['start_offset'][1]*self.scale]
        size = collision_rect['size']

        self.rect = pygame.Rect(self.position[0]+offset[0]-start_offset[0], self.position[1]+offset[1]-start_offset[1], size[0]*self.scale, size[1]*self.scale)
        self.offset = offset
