import pygame, json
from .enemy import Enemy
from .fire_breathe import Firebreathe

class Bowser(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, [rect[0], rect[1]], 'bowser', 'walk')
        self.horizontal_movement_counter = 2
        self.jump_counter = 1.5
        self.fire_counter = 3
        self.airtimer = 0
        self.jumping = False
        self.gravity = False
        self.load_rect()

    def load_rect(self):
        scale = self.current_animation.animation_data.config['scale']

        data = json.load(open('data/configs/collision_boxes/bowser.json', 'r'))
        self.rect = pygame.Rect(self.position[0]+data['offset'][0]*scale, self.position[1]+data['offset'][1]*scale, data['size'][0]*scale, data['size'][1]*scale)

        self.offset = [data['start_offset'][0]*scale, data['start_offset'][1]*scale]
        self.initial_offset = self.offset.copy()

    def update(self):
        super().update(function=self.hurt_mario, enemies=False, lifts=False)

        if self.on_screen:
            self.horizontal_movement_counter -= self.game.dt
            self.jump_counter -= self.game.dt
            self.fire_counter -= self.game.dt

            if self.horizontal_movement_counter <= 0:
                self.velocity[0] *= -1
                self.horizontal_movement_counter = 2

            if self.jump_counter <= 0 and not self.jumping:
                self.jumping = True
                self.airtimer = 0

            if self.fire_counter <= 0:
                self.fire()

            self.flip(self.game.entities.mario.center[0] < self.center[0])

            if self.jumping:
                if self.airtimer < 27:
                    self.velocity[1] -= 1.9*(27-self.airtimer)/80
                    self.airtimer += 1
                else:
                    self.jumping = False
                    self.airtimer = 0
                    self.jump_counter = 1.5
            else:
                self.velocity[1] += 0.25
                self.velocity[1] = min(self.velocity[1], 5)

        if self.game.entities.mario.center[0] > self.center[0]:
            self.offset[0] = 0
        else:
            self.offset[0] = self.initial_offset[0]

    def hurt_mario(self):
        self.game.entities.mario.change_state('enemy')

    def fire(self):
        velocity = [3,0]
        if self.game.entities.mario.center[0] < self.center[0]:
            velocity[0] = -3

        firebreathe = Firebreathe(self.game, pygame.Rect(*self.position, *self.rect.size), velocity, self.game.entities.mario.rect.copy())
        self.game.entities.firebreathes.append(firebreathe)

        self.fire_counter = 3
