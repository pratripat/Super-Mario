from .question_block import Question_Block
from .super_mushroom import Super_Mushroom
from .fireflower import FireFlower
from ..funcs import *

class Power_Up_Block(Question_Block):
    def __init__(self, game, rect):
        super().__init__(game, rect)
        self.sfx = pygame.mixer.Sound('data/sfx/powerup_appearing.wav')

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.reveal)
        self.update_offset(self.spawn_mushroom)

    def spawn_mushroom(self):
        items = {
            'Super_Mushroom': Super_Mushroom(self.game, [self.rect[0], self.rect[1]]),
            'FireFlower': FireFlower(self.game, [self.rect[0], self.rect[1]])
        }
        item = self.load_item(items)
        item.movement_timer = 48
        self.game.entities.items.append(item)

    def load_item(self, items):
        if self.game.entities.mario.id == 'small_mario':
            return items['Super_Mushroom']

        return items['FireFlower']

    def reveal(self):
        if self.hits > 0:
            self.sfx.play()
            self.animation = self.game.animations.get_animation('empty_block')
