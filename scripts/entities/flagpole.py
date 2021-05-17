from ..funcs import *
import pygame

class Flagpole:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect
        self.flag_taken_down = False
        self.load_level = 0

    def run(self):
        if self.flag_taken_down:
            self.game.entities.mario.movement()
            self.game.entities.mario.move(self.game.entities.get_colliding_entities(), self.game.dt, self.game.tilemap)

            if not pygame.mixer.music.get_busy():
                self.game.load_level()

            return

        rect = self.game.entities.mario.rect.copy()

        if rect_rect_collision(self.game.entities.mario.rect, self.rect):
            if not self.game.paused:
                pygame.mixer.music.load('data/music/flagpole.wav')
                pygame.mixer.music.play()

            self.game.paused = True
            self.game.level_finished = True
            self.game.entities.mario.set_animation('hold')

            self.game.entities.mario.rect[1] += 4

            if not rect[1]+rect[3] > self.rect[1]+self.rect[3]:
                return

            pygame.mixer.music.load('data/music/stage_clear.wav')
            pygame.mixer.music.play()

            self.game.entities.mario.rect[1] = self.rect[1]+self.rect[3]-rect[3]
            self.game.entities.mario.velocity[1] = -1
            self.game.entities.mario.directions = {k:False for k in ['up', 'down', 'left', 'right']}
            self.game.entities.mario.directions['right'] = True
            self.game.entities.mario.directions['down'] = True
            self.flag_taken_down = True
