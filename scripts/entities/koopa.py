from .enemy import Enemy
from ..funcs import *
import pygame, json

class Koopa(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, [rect[0], rect[1]], 'koopa', 'moving')
        self.load_collision_rect()

    def update(self):
        super().update(self.stomped, False)

    def stomped(self):
        state = self.current_animation_id

        if state == 'koopa_idle':
            self.roll()
            return

        if state == 'koopa_moving':
            self.set_animation('idle')
            self.velocity[0] = 0
            self.load_collision_rect()
            return

        if state == 'koopa_rolling':
            self.set_animation('idle')
            self.velocity[0] = 0
            self.load_collision_rect()
            return

    def roll(self):
        self.set_animation('rolling')

        if self.game.entities.mario.rect[0] > self.rect[0]:
            self.velocity[0] = -10
        else:
            self.velocity[0] =  10

        self.rect[0] += self.velocity[0]
        self.load_collision_rect()

    def load_collision_rect(self):
        collision_rects = json.load(open('data/configs/collision_boxes/koopa.json', 'r'))
        collision_rect = collision_rects[self.current_animation_id]
        offset = [collision_rect['offset'][0]*self.scale, collision_rect['offset'][1]*self.scale]
        start_offset = [collision_rect['start_offset'][0]*self.scale, collision_rect['start_offset'][1]*self.scale]
        size = collision_rect['size']

        self.rect = pygame.Rect(self.position[0]+offset[0]-start_offset[0], self.position[1]+offset[1]-start_offset[1], size[0]*self.scale, size[1]*self.scale)
        self.offset = offset
