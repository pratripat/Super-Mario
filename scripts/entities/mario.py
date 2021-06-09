import pygame, json
from ..funcs import *
from ..entity import Entity
from .fireball import Fireball

class Mario(Entity):
    def __init__(self, game, rect, id, transition_velocity):
        super().__init__(game.animations, id, list(rect.topleft), 'idle')
        self.game = game
        self.airtimer = 0
        self.speed = 4
        self.running = False
        self.directions = {k:False for k in ['left', 'right', 'up', 'down']}
        self.directions['down'] = True
        self.crouching = False
        self.flickering = False
        self.pipe_transition = False
        self.dead = False
        self.flicker_timer = 0
        self.invincible_timer = 0
        self.pipe_transition_timer = 0
        self.pipe_transition_velocity = [0,0]
        self.pipe_transition_velocity_2 = [0,0]

        self.power_up_sfx = pygame.mixer.Sound('data/sfx/power_up.wav')
        self.damage_sfx = pygame.mixer.Sound('data/sfx/damage.wav')
        self.small_mario_jump_sfx = pygame.mixer.Sound('data/sfx/small_mario_jump.wav')
        self.mario_jump_sfx = pygame.mixer.Sound('data/sfx/mario_jump.wav')
        self.fireball_sfx = pygame.mixer.Sound('data/sfx/fireball.wav')

        if transition_velocity:
            self.pipe_transition = True
            self.pipe_transition_timer = 96
            self.pipe_transition_velocity = transition_velocity.copy()

            if not transition_velocity == [0,0]:
                self.damage_sfx.play()
            else:
                self.set_animation('jump')

        self.load_collision_rect(self.id)

    def render(self):
        if self.invincible_timer > 0 and self.invincible_timer%3 == 0:
            return

        super().render(self.game.screen, self.game.camera.scroll)

    def run(self):
        self.update(self.game.dt)

        if self.dead:
            if not pygame.mixer.music.get_busy():
                self.game.load_level(self.game.level)

            self.rect[1] += self.velocity[1]
            self.velocity[1] += 0.25

            return

        if self.game.level_finished:
            return

        if int(self.current_animation.frame) == self.current_animation.animation_data.duration():
            self.game.paused = False
            self.flicker_timer = 0
            self.flickering = False

        if self.pipe_transition:
            self.rect[0] += self.pipe_transition_velocity[0]
            self.rect[1] += self.pipe_transition_velocity[1]

            self.pipe_transition_timer -= 1

            if self.pipe_transition_timer == 96:
                self.set_position(self.pipe_final_position)
                self.game.camera.scroll[0] = self.position[0]-self.game.screen.get_width()/2
                self.game.load_level(level=self.game.level, filepath=self.pipe_file_path, world_type=self.pipe_world_type, position=self.pipe_final_position, transition_velocity=self.pipe_transition_velocity_2)

            if self.pipe_transition_timer == 0:
                self.game.paused = False
                self.pipe_transition = False
                self.pipe_transition_velocity = [0,0]
                self.pipe_transition_velocity_2 = [0,0]

            return

        if self.flickering:
            self.flicker_timer += 1

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.game.paused:
            return

        if self.rect[1] > self.game.tilemap.bottom:
            self.die(False)

        self.move(self.game.entities.get_colliding_entities(), self.game.dt, self.game.tilemap)
        self.movement()
        self.hits(self.game.entities.get_enemies())

    def hits(self, enemies):
        if int(self.invincible_timer) > 0:
            return

        for enemy in enemies:
            if self.velocity[1] > 0 and not self.collisions['bottom']:
                return

            if enemy.dead or enemy.falling:
                continue

            rect = self.rect.copy()
            rect2 = enemy.rect.copy()
            if enemy.current_animation_id == f'{self.game.world_type}_koopa_idle' or enemy.current_animation_id == 'red_koopa_idle':
                rect[0] += self.velocity[0]
                rect[1] += self.velocity[1]

                if rect_rect_collision(rect, enemy.rect):
                    enemy.roll()
                    enemy.rect[0] += enemy.velocity[0]
                    return

                rect[0] -= self.velocity[0]
                rect[1] -= self.velocity[1]

            rect[0] += self.velocity[0]

            if rect_rect_collision(rect, enemy.rect):
                self.change_state('enemy')
                return

    def movement(self):
        speed = self.speed
        acceleration = 0.2

        if self.running:
            speed = 8

        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 15

        if self.directions['left'] and not self.directions['right'] and not self.crouching:
            animation_state = 'run'
            self.velocity[0] -= acceleration
            self.velocity[0] = max(-speed, self.velocity[0])
            self.flip(True)

            if self.velocity[0] >= 0:
                animation_state = 'slide'

        if self.directions['right'] and not self.directions['left'] and not self.crouching:
            animation_state = 'run'
            self.velocity[0] += acceleration
            self.velocity[0] = min(speed, self.velocity[0])
            self.flip(False)

            if self.velocity[0] <= 0:
                animation_state = 'slide'

        if (not (self.directions['right'] or self.directions['left'])) or (self.directions['right'] and self.directions['left']):
            if abs(self.velocity[0]) > 1:
                self.velocity[0] -= 0.3 * self.velocity[0]/abs(self.velocity[0])
                animation_state = 'slide'
            else:
                self.velocity[0] = 0

        if self.directions['down']:
            self.velocity[1] += 1

        #Jump
        elif self.directions['up']:
            if self.airtimer == 0:
                self.jump_sfx.play()

            if self.airtimer < 15:
                self.velocity[1] -= 3.8*self.airtimer/25
                self.airtimer += 1

            #If player is at max height, setting the upward movement false and allowing player to fall
            else:
                self.directions['up'] = False
                self.directions['down'] = True

        self.velocity[1] = min(8, self.velocity[1])

        if self.airtimer > 3:
            animation_state = 'jump'

        if self.crouching:
            animation_state = 'crouching'

        if self.current_animation_id.split('_')[-1] == 'shoot' and not int(self.current_animation.frame) == self.current_animation.animation_data.duration():
            return

        self.set_animation(animation_state)

    def change_state(self, type):
        states = json.load(open('data/configs/mario_states.json', 'r'))
        current_animation_id = f'{self.id}_to_{states[type][self.id]}'

        if states[type][self.id] == 'none':
            self.die()
            return

        if type != 'enemy':
            self.power_up_sfx.play()
        else:
            if self.flickering:
                return

            self.damage_sfx.play()
            self.flickering = True
            self.invincible_timer = 150

        if current_animation_id in self.animations.animations:
            self.current_animation_id = current_animation_id
            self.current_animation = self.animations.get_animation(self.current_animation_id)

            self.game.paused = True

        self.id = states[type][self.id]

        self.load_collision_rect(self.id)

    def load_collision_rect(self, id):
        collision_rects = json.load(open('data/configs/collision_boxes/mario.json', 'r'))
        collision_rect = collision_rects[id]
        offset = [collision_rect['offset'][0]*self.scale, collision_rect['offset'][1]*self.scale]
        start_offset = [collision_rect['start_offset'][0]*self.scale, collision_rect['start_offset'][1]*self.scale]
        size = collision_rect['size']

        self.rect = pygame.Rect(self.position[0]+offset[0]-start_offset[0], self.position[1]+offset[1]-start_offset[1], size[0]*self.scale, size[1]*self.scale)
        self.offset = offset

    def play_pipe_transition(self, file_path, end_position, world_type, direction1, direction2):
        if self.pipe_transition:
            return

        animation_state = 'idle'
        pygame.mixer.music.load('data/music/pipe.wav')
        pygame.mixer.music.play()

        if direction1[0] > 0:
            self.pipe_transition_velocity[0] =  1
            animation_state = 'run'
        if direction1[0] < 0:
            self.pipe_transition_velocity[0] = -1
            animation_state = 'run'
        if direction1[1] > 0:
            self.pipe_transition_velocity[1] =  1
            animation_state = 'crouching'

        if direction2[0] > 0:
            self.pipe_transition_velocity_2[0] =  1
        if direction2[0] < 0:
            self.pipe_transition_velocity_2[0] = -1
        if direction2[1] > 0:
            self.pipe_transition_velocity_2[1] =  1
        if direction2[1] < 0:
            self.pipe_transition_velocity_2[1] = -1

        self.game.paused = True
        self.pipe_transition_timer = 192
        self.pipe_transition = True
        self.pipe_final_position = list(end_position)
        self.pipe_final_position[0] -= direction2[0]
        self.pipe_final_position[1] -= direction2[1]
        self.pipe_file_path = file_path
        self.pipe_world_type = world_type
        self.set_animation(animation_state)

    def shoot_fireball(self):
        if self.id != 'fire_mario':
            return

        fireball = Fireball(self.game, self.center, self.flipped)
        self.game.entities.fireballs.append(fireball)
        self.set_animation('shoot')
        self.fireball_sfx.play()

    def die(self, jump=True):
        self.dead = True
        self.set_animation('fall')
        pygame.mixer.music.load('data/music/death.wav')
        pygame.mixer.music.play()

        if jump:
            self.velocity[1] = -5

    @property
    def jump_sfx(self):
        if self.id == 'small_mario':
            return self.small_mario_jump_sfx

        return self.mario_jump_sfx
