from ..funcs import *
import pygame

class Flagpole:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect
        self.rect[2] = 200
        self.flag_taken_down = False

    def run(self):
        if self.flag_taken_down:
            self.game.entities.mario.movement()
            self.game.entities.mario.move(self.game.entities.get_colliding_entities(), self.game.dt, self.game.tilemap)
            return

        rect = self.game.entities.mario.rect.copy()

        if rect_rect_collision(self.game.entities.mario.rect, self.rect):
            self.game.paused = True
            self.game.level_finished = True

            self.game.entities.mario.rect[1] += 5

            if not rect[1]+rect[3] > self.rect[1]+self.rect[3]:
                return

            self.game.entities.mario.rect[1] = self.rect[1]+self.rect[3]-rect[3]
            self.game.entities.mario.velocity[1] = -1
            self.game.entities.mario.directions = {k:False for k in ['up', 'down', 'left', 'right']}
            self.game.entities.mario.directions['right'] = True
            self.game.entities.mario.directions['down'] = True
            self.flag_taken_down = True
