from .mushroom import Mushroom
from ..funcs import *

class One_Up(Mushroom):
    def __init__(self, game, position):
        super().__init__(game, position, 'one_up_mushroom')
        self.sfx = pygame.mixer.Sound('data/sfx/one_up.wav')

    def update(self):
        super().update()

        if rect_rect_collision(self.rect, self.game.entities.mario.rect):
            self.sfx.play()
            self.used = True
            self.game.entities.mario.lives += 1
            self.game.score_system.add_score('others', 'power_up', self)
