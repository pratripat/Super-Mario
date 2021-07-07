import pygame, json, os
from ..funcs import *
from ..entity import Entity
from .fireball import Fireball

class Mario(Entity):
    def __init__(self, game, rect, id, transition_velocity):
        super().__init__(game.animations, id, list(rect.topleft), 'idle')
        self.game = game
        self.dead = False
        self.running = False
        self.invisible = False
        self.crouching = False
        self.flickering = False
        self.pipe_transition = False
        self.invincible_star = False
        self.current_animation_frame = None
        self.speed = 4
        self.airtimer = 0
        self.max_airtimer = 15
        self.flicker_timer = 0
        self.invincible_timer = 0
        self.pipe_transition_timer = 0
        self.star_animation_number = 0
        self.pipe_transition_velocity = [0,0]
        self.pipe_transition_velocity_2 = [0,0]

        self.directions = {k:False for k in ['left', 'right', 'up', 'down']}
        self.directions['down'] = True

        self.power_up_sfx = pygame.mixer.Sound('data/sfx/power_up.wav')
        self.damage_sfx = pygame.mixer.Sound('data/sfx/damage.wav')
        self.small_mario_jump_sfx = pygame.mixer.Sound('data/sfx/small_mario_jump.wav')
        self.mario_jump_sfx = pygame.mixer.Sound('data/sfx/mario_jump.wav')
        self.fireball_sfx = pygame.mixer.Sound('data/sfx/fireball.wav')

        if transition_velocity != None:
            if transition_velocity == [0,0]:
                self.set_animation('jump')
            else:
                self.pipe_transition = True
                self.pipe_transition_timer = 96
                self.pipe_transition_velocity = transition_velocity.copy()

        self.load_collision_rect(self.id)

    def render(self):
        if self.invisible and self.invincible_timer > 0 and int(self.invincible_timer*30)%3 == 0:
            return

        super().render(self.game.screen, self.game.camera.scroll)

    def run(self):
        self.update(self.game.dt)

        if self.dead:
            if not pygame.mixer.music.get_busy():
                self.game.load_level(self.game.level, mario_dead=True)

            self.rect[1] += self.velocity[1]
            self.velocity[1] += 0.25

            return

        if self.game.flag_animation:
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
                if self.pipe_transition_velocity_2 != None and self.pipe_transition_velocity_2 != [0,0]:
                    pygame.mixer.music.stop()

            if self.pipe_transition_timer == 60:
                pygame.mixer.music.load('data/music/pipe.wav')
                pygame.mixer.music.play()

            if self.pipe_transition_timer == -1:
                self.game.paused = False
                self.pipe_transition = False
                self.pipe_transition_velocity = [0,0]
                self.pipe_transition_velocity_2 = [0,0]
                self.game.play_music()

            return

        if self.flickering:
            self.flicker_timer += 1

        if self.invincible_timer > 0:
            self.invincible_timer -= self.game.dt

            if self.invincible_star:
                if int(self.invincible_timer) <= 0:
                    self.invincible_star = False
                    self.invincible_timer = 0
                    self.current_animation_frame = None
                elif int(self.invincible_timer*30)%3 == 0:
                    self.current_animation_frame = self.current_animation.frame
                    self.star_animation_number += 1
                    self.star_animation_number %= 5

                elif self.invincible_timer < 2:
                    self.game.play_music()

            if self.invisible:
                if int(self.invincible_timer) <= 0:
                    self.invisible = False

        if self.game.paused:
            return

        if self.rect[1] > self.game.tilemap.bottom:
            self.die(False)

        self.move(self.game.entities.get_colliding_entities(), self.game.dt, self.game.tilemap)
        self.movement()
        self.hits(self.game.entities.get_enemies())

        if self.crouching and self.current_animation_id == self.id + '_crouching':
            if self.id == 'small_mario':
                self.crouching = False
            else:
                self.load_collision_rect(self.current_animation_id)

    def hits(self, enemies):
        if int(self.invincible_timer) > 0 and not self.invincible_star:
            return

        for enemy in enemies:
            if self.velocity[1] > 0 and not self.collisions['bottom']:
                return

            if enemy.dead or enemy.falling:
                continue

            rect = self.rect.copy()
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
                if self.invincible_star:
                    enemy.dead = True
                    enemy.falling = True
                    enemy.stomp_sfx.play()
                else:
                    self.change_state('enemy')
                return

            if enemy.id == 'bowser':
                if rect_rect_collision(rect, enemy.head_rect):
                    if self.invincible_star:
                        enemy.dead = True
                        enemy.falling = True
                        enemy.stomp_sfx.play()
                    else:
                        self.change_state('enemy')
                    return

        for firebar in self.game.entities.firebars:
            for fireball in firebar.fireballs:
                fireball_rect = fireball.rect.copy()
                fireball_rect[0] += firebar.position[0]
                fireball_rect[1] += firebar.position[1]

                if rect_rect_collision(self.rect, fireball_rect):
                    if not self.invincible_star:
                        self.change_state('enemy')
                    return

        for firebreathe in self.game.entities.firebreathes:
            if rect_rect_collision(self.rect, firebreathe.rect):
                if not self.invincible_star:
                    self.change_state('enemy')
                return

    def movement(self):
        speed = self.speed
        acceleration = 0.15

        if self.running and not self.game.world_type == 'underwater':
            speed = 7.5

        if self.game.world_type == 'underwater':
            self.max_airtimer = 13
        else:
            self.max_airtimer = 15

        animation_state = 'idle'

        if self.collisions['left'] or self.collisions['right']:
            self.velocity[0] = 0
        if self.collisions['top']:
            self.velocity[1] = 0

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0 and self.game.world_type != 'underwater':
            self.airtimer = self.max_airtimer

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

        if (not (self.directions['right'] or self.directions['left'])) or (self.directions['right'] and self.directions['left']) or self.crouching:
            if abs(self.velocity[0]) > 1:
                self.velocity[0] -= 0.2 * self.velocity[0]/abs(self.velocity[0])
                animation_state = 'slide'
            else:
                self.velocity[0] = 0

        if self.directions['down']:
            if self.game.world_type == 'underwater':
                self.velocity[1] += 0.5
            else:
                self.velocity[1] += 1

        #Jump
        elif self.directions['up']:
            if self.airtimer == 0:
                self.jump_sfx.play()

            if self.airtimer < self.max_airtimer:
                self.velocity[1] -= 4*self.airtimer/25
                self.airtimer += 1

            #If player is at max height, setting the upward movement false and allowing player to fall
            else:
                self.directions['up'] = False
                self.directions['down'] = True

            if self.game.world_type == 'underwater':
                self.velocity[1] = max(-5, self.velocity[1])

        if self.game.world_type == 'underwater':
            self.velocity[1] = min(5, self.velocity[1])
        else:
            self.velocity[1] = min(8, self.velocity[1])

        if self.airtimer > 3:
            animation_state = 'jump'

        if self.crouching:
            animation_state = 'crouching'

        if self.game.world_type == 'underwater' and self.airtimer > 0:
            animation_state = 'swim'

        if self.current_animation_id.split('_')[-1] == 'shoot' and not int(self.current_animation.frame) == self.current_animation.animation_data.duration():
            return

        if self.invincible_star:
            animation_state = f'star_{self.star_animation_number}_' + animation_state

        self.set_animation(animation_state, self.current_animation_frame)

        self.current_animation_frame = None

    def change_state(self, type):
        states = json.load(open('data/configs/mario_states.json', 'r'))

        try:
            new_id = states[type][self.id]
        except:
            new_id = self.id

        current_animation_id = f'{self.id}_to_{new_id}'

        if new_id == 'none':
            self.die()
            return

        if type == 'power_up':
            self.power_up_sfx.play()
        elif type == 'enemy':
            if self.flickering:
                return

            self.damage_sfx.play()
            self.flickering = True
            self.invincible_timer = 5
            self.invisible = True
        elif type == 'star':
            self.invincible_star = True
            self.invincible_timer = 9

            pygame.mixer.music.load('data/music/star.wav')
            pygame.mixer.music.play(3)

        if current_animation_id in self.animations.animations:
            self.current_animation_id = current_animation_id
            self.current_animation = self.animations.get_animation(self.current_animation_id)

            self.game.paused = True

        self.id = new_id

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

        if self.pipe_transition_velocity[0] > 0:
            self.flip(False)
        if self.pipe_transition_velocity[0] < 0:
            self.flip(True)

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
