from ..funcs import *
import pygame, json

class Flagpole:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect
        self.flag_taken_down = False
        self.distance = 0
        self.load_level = 0
        self.waiting_timer = 40
        self.flag_image = pygame.image.load('data/graphics/images/flag.png').convert()
        self.flag_image = pygame.transform.scale(self.flag_image, (self.flag_image.get_width()*3, self.flag_image.get_height()*3))
        self.flag_image.set_colorkey((0,0,0))
        self.flag_position = [self.rect[0]+self.rect[2]/2-self.flag_image.get_width(), self.rect[1]+24]

    def render(self):
        self.game.screen.blit(self.flag_image, (self.flag_position[0]-self.game.camera.scroll[0], self.flag_position[1]-self.game.camera.scroll[1]))

    def run(self):
        if self.game.playing_cutscene:
            return

        if self.flag_taken_down and self.waiting_timer == 0:
            self.game.paused = False
            self.game.flag_animation = False
            self.game.entities.mario.running = False
            self.game.entities.mario.directions = {k:False for k in ['up', 'down', 'left', 'right']}
            self.game.entities.mario.directions['down'] = True

            self.game.load_cutscene('data/configs/cutscenes/flagpole.json', self.load_next_level)

            return
        elif self.flag_taken_down:
            self.waiting_timer -= 1

        rect = self.game.entities.mario.rect.copy()

        if rect_rect_collision(self.game.entities.mario.rect, self.rect):
            if self.distance == 0:
                self.distance = self.rect[1]+self.rect[3]-self.game.entities.mario.position[1]
                self.distance = self.distance//3
                print(self.distance)

            if not self.game.paused:
                pygame.mixer.music.load('data/music/flagpole.wav')
                pygame.mixer.music.play()

            self.game.paused = True
            self.game.flag_animation = True
            self.game.level_clear = True
            self.game.entities.mario.flip(False)
            self.game.entities.mario.set_animation('hold')

            if not self.flag_taken_down:
                self.game.entities.mario.rect[0] = self.rect[0]-self.game.entities.mario.rect[2]+12
                self.game.entities.mario.rect[1] += 4
                self.flag_position[1] += 4

            if self.game.entities.mario.rect[1] > self.rect[1]+self.rect[3]-rect[3]:
                self.game.entities.mario.rect[1] = self.rect[1]+self.rect[3]-rect[3]
                self.game.entities.mario.current_animation.frame = 0

            if not self.flag_position[1]+self.flag_image.get_height() > self.rect[1]+self.rect[3]-self.game.tilemap.RES*0.5 and pygame.mixer.music.get_busy():
                return

            pygame.mixer.music.load('data/music/stage_clear.wav')
            pygame.mixer.music.play()

            self.game.entities.mario.current_animation.frame = 0
            self.game.entities.mario.velocity[1] = -1
            self.flag_taken_down = True

            self.game.entities.mario.rect[0] = self.rect[0]+self.game.entities.mario.rect[2]-24
            self.game.entities.mario.flip(True)

            if self.distance < 18:
                self.game.score_system.add_score('others', 'flagpole_100', self.game.entities.mario)
            elif self.distance < 58:
                self.game.score_system.add_score('others', 'flagpole_400', self.game.entities.mario)
            elif self.distance < 82:
                self.game.score_system.add_score('others', 'flagpole_800', self.game.entities.mario)
            elif self.distance < 128:
                self.game.score_system.add_score('others', 'flagpole_2000', self.game.entities.mario)
            else:
                self.game.score_system.add_score('others', 'flagpole_5000', self.game.entities.mario)

    def load_next_level(self):
        if not pygame.mixer.music.get_busy():
            if not self.game.ui.time > 0:
                self.game.load_level(self.game.level+1)
            elif not self.game.reduce_coins:
                    self.game.reduce_coins = True
                    pygame.mixer.music.load('data/music/count_down.wav')
                    pygame.mixer.music.play()
