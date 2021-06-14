import pygame
from .mushroom import Mushroom
from ..funcs import *

class Star(Mushroom):
    def __init__(self, game, position):
        super().__init__(game, position, f'{game.world_type}_star')
        self.game = game
        self.max_flying_timer = 30
        self.flying_timer = self.max_flying_timer
        self.flying = True
        self.gravity = True

    def update(self):
        super().update()

        if rect_rect_collision(self.rect, self.game.entities.mario.rect):
            self.game.entities.mario.change_state('power_up')
            self.used = True

    def movement(self):
        if self.collisions['bottom']:
            self.flying_timer = self.max_flying_timer
            self.velocity[1] = -3
            self.gravity = False

        self.flying_timer -= 1

        if self.flying_timer == 0:
            self.gravity = True

        if self.gravity:
            self.velocity[1] += 0.25
            self.velocity[1] = min(3, self.velocity[1])
