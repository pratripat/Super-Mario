from .block import Block
from .coin_vfx import Coin
from ..animation_handler import Animation_Data, Animation
from ..funcs import *
import pygame

class Question_Block(Block):
    def __init__(self, game, rect, id='question_block', hits=1, index=0):
        super().__init__(rect, 'question')
        self.game = game
        self.hits = hits
        self.set_new_animation(id, index)
        self.sfx = pygame.mixer.Sound('data/sfx/coin.wav')
        self.coin = Coin(game, [self.rect[0]+self.animation.image.get_width()/2, self.rect[1]-self.animation.image.get_height()/2])

    def set_new_animation(self, id, index):
        if id not in self.game.animations.animations:
            animation_data = Animation_Data('data/graphics/animations/question_block')
            animation_data.images.clear()
            animation_data.images.append(load_images_from_spritesheet('data/graphics/spritesheet/tiles.png')[index-2])
            animation_data.config['frames'] = [5]
            animation_data.config['loop'] = False
            self.animation = Animation(animation_data)
            return

        self.animation = self.game.animations.get_animation(id)

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
            if self.hits == 1:
                self.animation = self.game.animations.get_animation('empty_block')
            self.coin.updating = True
            self.coin.offset = 0
