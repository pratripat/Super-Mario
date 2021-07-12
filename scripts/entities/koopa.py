from .enemy import Enemy
from ..funcs import *
import pygame, json, math

class Koopa(Enemy):
    def __init__(self, game, rect, animation='moving'):
        super().__init__(game, [rect[0], rect[1]], f'{game.world_type}_koopa', animation)
        self.load_collision_rect()

        if animation == 'flying':
            self.max_flying_timer = 50
            self.flying_timer = self.max_flying_timer
            self.flying = True

    def update(self):
        enemy_collisions = True
        if self.current_animation_id == f'{self.game.world_type}_koopa_rolling' or self.current_animation_id == 'red_koopa_rolling':
            enemy_collisions = False

        super().update(self.stomped, enemy_collisions)

        if self.current_animation_id == f'{self.game.world_type}_koopa_flying' or self.current_animation_id == 'red_koopa_flying':
            self.fly()

    def fly(self):
        if self.collisions['bottom']:
            self.flying_timer = self.max_flying_timer
            self.gravity = False
            self.velocity[1] = 0

        if self.flying_timer > 0:
            self.flying_timer -= 1
            self.rect[1] -= 3

        if self.flying_timer == 0:
            self.gravity = True

        if self.gravity:
            self.velocity[1] += 0.25
            self.velocity[1] = min(3, self.velocity[1])

    def stomped(self):
        self.game.score_system.add_score('enemy', 'koopa')
        state = self.current_animation_id

        if state == f'{self.game.world_type}_koopa_idle':
            self.roll()
            return

        if state == f'{self.game.world_type}_koopa_flying':
            self.set_animation('moving')
            self.load_collision_rect()
            self.gravity = True
            return

        if state == f'{self.game.world_type}_koopa_moving':
            self.set_animation('idle')
            self.velocity[0] = 0
            self.load_collision_rect()
            return

        if state == f'{self.game.world_type}_koopa_rolling':
            self.set_animation('idle')
            self.velocity[0] = 0
            self.load_collision_rect()
            return

    def roll(self):
        self.set_animation('rolling')

        if self.game.entities.mario.rect[0] > self.rect[0]:
            self.velocity[0] = -9
        else:
            self.velocity[0] =  9

        self.rect[0] += self.velocity[0]
        self.load_collision_rect()

    def load_collision_rect(self):
        if self.id == 'red_koopa':
            animation_id = self.current_animation_id
        else:
            animation_id = self.current_animation_id.split(f'{self.game.world_type}_')[1]

        collision_rects = json.load(open('data/configs/collision_boxes/koopa.json', 'r'))
        collision_rect = collision_rects[animation_id]
        offset = [collision_rect['offset'][0]*self.scale, collision_rect['offset'][1]*self.scale]
        start_offset = [collision_rect['start_offset'][0]*self.scale, collision_rect['start_offset'][1]*self.scale]
        size = collision_rect['size']

        self.rect = pygame.Rect(self.position[0]+offset[0]-start_offset[0], self.position[1]+offset[1]-start_offset[1], size[0]*self.scale, size[1]*self.scale)
        self.offset = offset

class Red_Koopa(Koopa):
    def __init__(self, game, rect, animation='moving'):
        super().__init__(game, rect)
        self.id = 'red_koopa'
        self.set_animation(animation)

        if animation == 'flying':
            self.gravity = False
            self.velocity[0] = 0
            self.flying = True
            self.max_flying_timer = 200
            self.flying_timer = self.max_flying_timer

    def update(self):
        super().update()

        if self.current_animation_id != 'red_koopa_moving':
            return

        position = self.position
        position = [position[0]//self.game.tilemap.RES, position[1]//self.game.tilemap.RES+2]
        position = [position[0]*self.game.tilemap.RES, position[1]*self.game.tilemap.RES]

        if not self.flipped:
            position[0] += self.game.tilemap.RES

        tiles = self.game.tilemap.get_tiles_with_position('ground', position)

        if len(tiles) == 0:
            self.velocity[0] *= -1
            self.rect[0] += self.velocity[0]

    def fly(self):
        self.gravity = False
        if self.collisions['bottom'] and not self.flying:
            self.flying_timer = self.max_flying_timer
            self.flying = True

        if self.flying:
            self.flying_timer -= 1
            self.rect[1] -= 2
        else:
            self.flying_timer -= 1
            self.rect[1] += 2

        if self.flying_timer == 0:
            self.flying_timer = self.max_flying_timer
            self.flying = not self.flying

    def stomped(self):
        self.game.score_system.add_score('enemy', 'koopa')
        state = self.current_animation_id

        if state == 'red_koopa_idle':
            self.roll()
            return

        if state == 'red_koopa_flying':
            self.set_animation('moving')
            self.velocity[0] = 0
            self.gravity = True
            self.load_collision_rect()
            return

        if state == 'red_koopa_moving':
            self.set_animation('idle')
            self.velocity[0] = 0
            self.load_collision_rect()
            return

        if state == 'red_koopa_rolling':
            self.set_animation('idle')
            self.velocity[0] = 0
            self.load_collision_rect()
            return
