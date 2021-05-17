import math
from ..entity import Entity
from ..funcs import *

class Fireball(Entity):
    def __init__(self, game, position, flipped):
        super().__init__(game.animations, 'fireball', position, 'rolling')
        self.game = game
        self.velocity = [8, 5]
        self.remove = False

        if flipped:
            self.velocity[0] *= -1

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        super().update(self.game.dt)
        self.move(self.game.entities.get_colliding_entities(), self.game.dt)
        self.movement()
        self.hits()

    def movement(self):
        if self.collisions['bottom']:
            self.velocity[1] = -8

        if self.collisions['right'] or self.collisions['left'] or self.collisions['top']:
            self.remove = True

        self.velocity[1] += 1

    def hits(self):
        for enemy in self.game.entities.enemies:
            if rect_rect_collision(self.rect, enemy.rect):
                enemy.dead = True
                enemy.remove = True
                self.remove = True
                return
