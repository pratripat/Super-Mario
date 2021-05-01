from .block import Block
from .brick_piece import Brick_Piece
import pygame, math

class Brick(Block):
    def __init__(self, game, rect):
        super().__init__(rect)
        self.game = game
        self.animation = self.game.animations.get_animation('brick')
        self.brick_break_sfx = pygame.mixer.Sound('data/sfx/brick_break.wav')

    def render(self):
        self.animation.render(self.game.screen, [self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.offset-self.game.camera.scroll[1]])

    def update(self):
        self.animation.run(self.game.dt)

        self.up_collision(self.game.entities.mario, self.burst)
        self.update_offset()

    def burst(self):
        self.brick_break_sfx.play()
        self.remove = True

        angle = -math.pi/1.3

        for i in range(2):
            self.game.entities.brick_pieces.append(Brick_Piece(self.game, list(self.rect.center), angle))
            angle -= math.pi/4

        angle = -math.pi/4

        for i in range(2):
            self.game.entities.brick_pieces.append(Brick_Piece(self.game, list(self.rect.center), angle))
            angle += math.pi/4
