import pygame, json
from ..entity import Entity

class Mario(Entity):
    def __init__(self, game):
        super().__init__(game.animations, 'small_mario', [500,100], 'idle')
        self.game = game
        self.airtimer = 0
        self.speed = 4
        self.running = False
        self.directions = {k:False for k in ['left', 'right', 'up', 'down']}
        self.directions['down'] = True

        self.power_up_sfx = pygame.mixer.Sound('data/sfx/power_up.wav')

        self.load_collision_rect()

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def run(self):
        self.update(self.game.dt)

        if int(self.current_animation.frame) == self.current_animation.animation_data.duration():
            self.game.paused = False

        if self.game.paused:
            return

        self.move(self.game.entities.get_colliding_entities(), self.game.dt, self.game.tilemap)
        self.movement()

    def movement(self):
        speed = self.speed
        acceleration = 0.1

        if self.running:
            speed = 7.5
            acceleration = 0.2

        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 10

        if self.directions['left'] and not self.directions['right']:
            animation_state = 'run'
            self.velocity[0] -= acceleration
            self.velocity[0] = max(-speed, self.velocity[0])
            self.flip(True)

            if self.velocity[0] >= 0:
                animation_state = 'slide'

        if self.directions['right'] and not self.directions['left']:
            animation_state = 'run'
            self.velocity[0] += acceleration
            self.velocity[0] = min(speed, self.velocity[0])
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
        states = json.load(open('data/configs/mario_states.json', 'r'))
        current_animation_id = f'{self.id}_to_{states[type]}'

        self.power_up_sfx.play()

        if current_animation_id in self.animations.animations:
            self.current_animation_id = current_animation_id
            self.current_animation = self.animations.get_animation(self.current_animation_id)

            self.game.paused = True

        self.id = states[type]

        self.load_collision_rect()

    def load_collision_rect(self):
        collision_rects = json.load(open('data/configs/mario_collision_boxes.json', 'r'))
        collision_rect = collision_rects[self.id]
        offset = [collision_rect['offset'][0]*self.scale, collision_rect['offset'][1]*self.scale]
        start_offset = [collision_rect['start_offset'][0]*self.scale, collision_rect['start_offset'][1]*self.scale]
        size = collision_rect['size']

        self.rect = pygame.Rect(self.position[0]+offset[0]-start_offset[0], self.position[1]+offset[1]-start_offset[1], size[0]*self.scale, size[1]*self.scale)
        self.offset = offset
