from .block import Block
from .brick_piece import Brick_Piece
from ..funcs import *
import pygame, math

class Brick(Block):
    def __init__(self, game, rect):
        super().__init__(rect, 'brick')
        self.game = game
        self.animation = self.game.animations.get_animation('brick')
        self.brick_break_sfx = pygame.mixer.Sound('data/sfx/brick_break.wav')
        self.brick_bump_sfx = pygame.mixer.Sound('data/sfx/brick_bump.wav')

    def render(self):
        self.animation.render(self.game.screen, [self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.offset-self.game.camera.scroll[1]])

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.burst)
        self.update_offset()

    def up_collision(self, player, function):
        if player.velocity[1] < 0:
            rect = player.rect.copy()
            rect[1] += player.velocity[1]
            if rect_rect_collision(rect, self.rect):
                if self.hits > 0:
                    self.hits -= 1
                    self.updating_offset = True

                if player.id != 'small_mario':
                    if self.hits == 0:
                        function()

                else:
                    self.hits += 1
                    self.brick_bump_sfx.play()

                player.velocity[1] = 0

                return

    def burst(self):
        self.brick_break_sfx.play()
        self.remove = True

        angle = -math.pi/1.3
        n = 0

        for i in range(2):
            self.game.entities.brick_pieces.append(Brick_Piece(self.game, list(self.rect.center), angle, n))
            angle -= math.pi/4
            n += 1

        angle = -math.pi/4

        for i in range(2):
            self.game.entities.brick_pieces.append(Brick_Piece(self.game, list(self.rect.center), angle, n))
            angle += math.pi/4
            n += 1
