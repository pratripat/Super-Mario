from .block import Block
import pygame, math

class Coin:
    def __init__(self, game, position):
        self.game = game
        self.position = position
        self.offset = 0
        self.timer = 0
        self.max_height = 144
        self.updating = False
        self.animation = game.animations.get_animation('coin_from_block')

    def render(self):
        self.animation.render(self.game.screen, [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]-self.offset])

    def update(self):
        self.animation.run(self.game.dt)

        self.timer += self.game.dt*4
        self.offset = math.sin(self.timer)*self.max_height

    @property
    def finished(self):
        return int(self.offset) <= 0

class Question_Block(Block):
    def __init__(self, game, rect):
        super().__init__(rect, 'question')
        self.game = game
        self.animation = self.game.animations.get_animation('question_block')
        self.sfx = pygame.mixer.Sound('data/sfx/coin.wav')
        self.coin = Coin(game, [self.rect[0]+self.animation.image.get_width()/2, self.rect[1]-self.animation.image.get_height()/2])

    def render(self):
        self.animation.render(self.game.screen, [self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.offset-self.game.camera.scroll[1]])

        if self.coin.updating:
            self.coin.render()

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.reveal)
        self.update_offset()

        if self.coin.updating:
            self.coin.update()

            if self.coin.finished:
                self.coin.updating = False

    def reveal(self):
        if self.hits > 0:
            self.sfx.play()
            self.animation = self.game.animations.get_animation('empty_block')
            self.coin.updating = True
