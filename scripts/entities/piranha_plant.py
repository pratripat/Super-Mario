from .enemy import Enemy
import pygame, math, json

class Piranha_Plant(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, list(rect.topleft), 'piranha_plant', '')
        self.movement_timer = 0
        self.velocity[0] = 0
        self.velocity[1] = 1
        self.gravity = False
        self.stompable = False
        self.top_position = self.position.copy()
        self.bottom_position = [self.position[0], self.position[1] + self.game.tilemap.RES*2]
        self.holding_timer = 0
        self.load_collision_rect()

    def update(self):
        super().update(None, False, False)

        if self.holding_timer > 0:
            self.holding_timer -= self.game.dt
            return

        if self.position[1] >= self.bottom_position[1]:
            self.velocity[1] = -1

        if self.position[1] <= self.top_position[1]:
            self.velocity[1] = 1

    def load_collision_rect(self):
        collision_rects = json.load(open('data/configs/collision_boxes/piranha_plant.json', 'r'))
        collision_rect = collision_rects['piranha_plant']
        offset = [collision_rect['offset'][0]*self.scale, collision_rect['offset'][1]*self.scale]
        start_offset = [collision_rect['start_offset'][0]*self.scale, collision_rect['start_offset'][1]*self.scale]
        size = collision_rect['size']

        self.rect = pygame.Rect(self.position[0]+offset[0]-start_offset[0], self.position[1]+offset[1]-start_offset[1], size[0]*self.scale, size[1]*self.scale)
        self.offset = offset
