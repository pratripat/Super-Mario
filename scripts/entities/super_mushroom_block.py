from .question_block import Question_Block
from .super_mushroom import Super_Mushroom
from ..funcs import *

class Super_Mushroom_Block(Question_Block):
    def __init__(self, game, rect):
        super().__init__(game, rect)
        self.sfx = pygame.mixer.Sound('data/sfx/powerup_appearing.wav')

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.reveal)
        self.update_offset(self.spawn_mushroom)

    def spawn_mushroom(self):
        mushroom = Super_Mushroom(self.game, [self.rect[0], self.rect[1]])
        mushroom.static_timer = 48
        self.game.entities.mushrooms.append(mushroom)

    def reveal(self):
        if self.hits > 0:
            self.sfx.play()
            self.animation = self.game.animations.get_animation('empty_block')
