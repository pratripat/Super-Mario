import pygame
from .enemy import Enemy

class Goomba(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, [rect[0], rect[1]], 'goomba', 'moving')

    def update(self):
        super().update(self.die)

    def die(self):
        self.current_animation_id = f'{self.id}_die'
        self.current_animation = self.animations.get_animation(self.current_animation_id)
        self.dead = True
        self.stomp_sfx.play()
