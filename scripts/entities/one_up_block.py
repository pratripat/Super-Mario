from .question_block import Question_Block
from .one_up_mushroom import One_Up
from ..funcs import *

class One_Up_Block(Question_Block):
    def __init__(self, game, rect):
        super().__init__(game, rect)
        self.sfx = pygame.mixer.Sound('data/sfx/powerup_appearing.wav')

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.reveal)
        self.update_offset(self.spawn_mushroom)

    def spawn_mushroom(self):
        item = One_Up(self.game, list(self.rect.topleft))
        item.movement_timer = 48
        self.game.entities.items.append(item)

    def reveal(self):
        if self.hits > 0:
            self.sfx.play()
            self.animation = self.game.animations.get_animation(f'{self.game.world_type}_empty_block')
            self.is_invisible = False
