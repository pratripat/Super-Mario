import pygame, json
from ..entity import Entity

class Mario(Entity):
    def __init__(self, game):
        super().__init__(game.animations, 'small_mario', [500,100], False, 'idle')
        self.game = game
        self.airtimer = 0
        self.speed = 6
        self.directions = {k:False for k in ['left', 'right', 'up', 'down']}
        self.directions['down'] = True

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def run(self):
        self.move(self.game.entities.get_colliding_entities(), self.game.dt, self.game.tilemap)
        self.movement()
        self.update(self.game.dt)

    def movement(self):
        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 10

        if self.directions['left'] and not self.directions['right']:
            animation_state = 'run'
            self.velocity[0] -= 0.1
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)

            if self.velocity[0] >= 0:
                animation_state = 'slide'

        if self.directions['right'] and not self.directions['left']:
            animation_state = 'run'
            self.velocity[0] += 0.1
            self.velocity[0] = min(self.speed, self.velocity[0])
            self.flip(False)

            if self.velocity[0] <= 0:
                animation_state = 'slide'

        if not (self.directions['right'] or self.directions['left']):
            if abs(self.velocity[0]) > 1:
                self.velocity[0] -= 0.4 * self.velocity[0]/abs(self.velocity[0])
                animation_state = 'slide'
            else:
                self.velocity[0] = 0

        if self.directions['down']:
            self.velocity[1] += 1

        #Jump
        elif self.directions['up']:
            if self.airtimer < 10:
                self.velocity[1] -= 3.7*self.airtimer/10
                self.airtimer += 1

            #If player is at max height, setting the upward movement false and allowing player to fall
            else:
                self.directions['up'] = False
                self.directions['down'] = True

        self.velocity[1] = min(8, self.velocity[1])

        if self.airtimer > 3:
            animation_state = 'jump'

        self.set_animation(animation_state)

    def change_state(self, type):
        mario_states = json.load(open('data/configs/mario_states.json', 'r'))
        self.id = mario_states[type]
