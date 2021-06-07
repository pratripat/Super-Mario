import pygame
from .enemy import Enemy

class Goomba(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, [rect[0], rect[1]], f'{game.world_type}_goomba', 'moving')

    def update(self):
        super().update(self.die)

    def die(self):
        self.set_animation('die')
        self.dead = True
        self.stomp_sfx.play()
