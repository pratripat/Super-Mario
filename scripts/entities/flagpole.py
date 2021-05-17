from ..funcs import *

class Flagpole:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect

    def run(self):
        if rect_rect_collision(self.game.entities.mario.rect, self.rect):
            self.game.paused = True
            self.game.level_finished = True
