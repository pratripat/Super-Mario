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
        enemies = {
            f'{self.game.world_type}_koopa': 'koopa',
            f'{self.game.world_type}_goomba': 'goomba',
            f'{self.game.world_type}_piranha_plant': 'piranha_plant',
            f'red_cheep_cheep': 'red_cheep_cheep',
            f'grey_cheep_cheep': 'grey_cheep_cheep',
            'red_koopa': 'koopa',
            'blooper': 'blooper'
        }

        for enemy in self.game.entities.enemies:
            if enemy.id == 'podoboo':
                continue

            if enemy.id != 'bowser' or (enemy.id == 'bowser' and enemy.fireball_hits <= 0):
                if rect_rect_collision(self.rect, enemy.rect):
                    enemy.dead = True
                    enemy.remove = True
                    self.remove = True
                    self.game.score_system.add_score('enemy', enemies[enemy.id], enemy)
                    return
            else:
                if rect_rect_collision(self.rect, enemy.rect) or rect_rect_collision(self.rect, enemy.head_rect):
                    enemy.fireball_hits -= 1
                    self.remove = True

    @property
    def on_screen(self):
        return (
            -self.rect.w < self.position[0]-self.game.camera.scroll[0] < self.game.screen.get_width() and
            -self.rect.h < self.position[1]-self.game.camera.scroll[1] < self.game.screen.get_height()
        )
