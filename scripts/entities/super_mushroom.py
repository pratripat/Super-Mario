from .mushroom import Mushroom
from ..funcs import *

class Super_Mushroom(Mushroom):
    def __init__(self, game, position):
        super().__init__(game, position, 'super_mushroom')

    def update(self):
        super().update()

        if rect_rect_collision(self.rect, self.game.entities.mario.rect):
            self.game.entities.mario.change_state(self.id)
            self.used = True
