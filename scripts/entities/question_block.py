from .block import Block
import pygame

class Question_Block(Block):
    def __init__(self, game, rect):
        super().__init__(rect, 'question')
        self.game = game
        self.animation = self.game.animations.get_animation('question_block')
        self.coin_sfx = pygame.mixer.Sound('data/sfx/coin.wav')

    def render(self):
        self.animation.render(self.game.screen, [self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.offset-self.game.camera.scroll[1]])

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.reveal)
        self.update_offset()

    def reveal(self):
        if self.hits > 0:
            self.coin_sfx.play()
            self.animation = self.game.animations.get_animation('empty_block')
