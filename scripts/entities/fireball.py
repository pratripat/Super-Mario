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
            self.flipped = True

    def render(self, surface=None, scroll=None):
        super().render(surface or self.game.screen, scroll or self.game.camera.scroll)

    def update(self):
        super().update(self.game.dt)
        self.move(self.game.entities.get_colliding_entities(enemies=False), self.game.dt)
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
            if enemy.id != 'bowser' or (enemy.id == 'bowser' and enemy.fireball_hits <= 0):
                if rect_rect_collision(self.rect, enemy.rect):
                    enemy.dead = True
                    enemy.remove = True
                    self.remove = True
                    return
            else:
                if rect_rect_collision(self.rect, enemy.rect) or rect_rect_collision(self.rect, enemy.head_rect):
                    enemy.fireball_hits -= 1
                    self.remove = True
