from ..entity import Entity
from ..funcs import *
import pygame

class Lift(Entity):
    def __init__(self, game, rect, velocity=None, top_position=None, bottom_position=None, left_position=None, right_position=None):
        super().__init__(game.animations, 'lift', list(rect.topleft), '')
        self.game = game
        self.top_position = top_position
        self.bottom_position = bottom_position
        self.left_position = left_position
        self.right_position = right_position

        if velocity:
            self.velocity = velocity
        else:
            self.load_velocity()

    def load_velocity(self):
        indicators = self.game.tilemap.get_tiles_with_position('lift_indicators', self.position)

        if len(indicators) == 0:
            return

        top_indicator = None
        current_indicator = indicators[0]
        current_position = self.position.copy()

        while True:
            current_position[1] -= self.game.tilemap.RES

            indicator = self.game.tilemap.get_tiles_with_position('lift_indicators', current_position)

            if len(indicator) == 0:
                top_indicator = current_indicator
                break

            current_indicator = indicator[0]

        bottom_indicator = None
        current_indicator = indicators[0]
        current_position = self.position.copy()

        while True:
            current_position[1] += self.game.tilemap.RES

            indicator = self.game.tilemap.get_tiles_with_position('lift_indicators', current_position)

            if len(indicator) == 0:
                bottom_indicator = current_indicator
                break

            current_indicator = indicator[0]

        if top_indicator and bottom_indicator:
            if top_indicator['position'] != bottom_indicator['position']:
                self.top_position = top_indicator['position']
                self.bottom_position = bottom_indicator['position']
                self.velocity[1] = 2
                return

        left_indicator = None
        current_indicator = indicators[0]
        current_position = self.position.copy()

        while True:
            current_position[0] -= self.game.tilemap.RES

            indicator = self.game.tilemap.get_tiles_with_position('lift_indicators', current_position)

            if len(indicator) == 0:
                left_indicator = current_indicator
                break

            current_indicator = indicator[0]

        right_indicator = None
        current_indicator = indicators[0]
        current_position = self.position.copy()

        while True:
            current_position[0] += self.game.tilemap.RES

            indicator = self.game.tilemap.get_tiles_with_position('lift_indicators', current_position)

            if len(indicator) == 0:
                right_indicator = current_indicator
                break

            current_indicator = indicator[0]

        if left_indicator and right_indicator:
            if left_indicator['position'] != right_indicator['position']:
                self.left_position = left_indicator['position']
                self.right_position = right_indicator['position']
                self.velocity[0] = 2
                return

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        super().update(self.game.dt)
        self.move([], self.game.dt)

        if self.top_position and self.bottom_position:
            if self.position[1] <= self.bottom_position[1]:
                if self.velocity[1] < 0 and self.position[1] <= self.top_position[1]:
                    self.velocity[1] =  2

            if self.position[1] >= self.top_position[1]:
                if self.velocity[1] > 0 and self.position[1] >= self.bottom_position[1]:
                    self.velocity[1] = -2

            rect = pygame.Rect(self.position[0], self.position[1]-self.game.tilemap.RES//2, self.rect.w, self.rect.h)

            if rect_rect_collision(rect, self.game.entities.mario.rect):
                self.game.entities.mario.rect[1] += self.velocity[1]

        if self.left_position and self.right_position:
            if self.position[0] <= self.right_position[0]:
                if self.velocity[0] < 0 and self.position[0] <= self.left_position[0]:
                    self.velocity[0] =  2

            if self.position[0] >= self.left_position[0]:
                if self.velocity[0] > 0 and self.position[0] >= self.right_position[0]:
                    self.velocity[0] = -2

            rect = pygame.Rect(self.position[0], self.position[1]-self.game.tilemap.RES//2, self.rect.w, self.rect.h)

            if rect_rect_collision(rect, self.game.entities.mario.rect):
                self.game.entities.mario.rect[0] += self.velocity[0]

    @property
    def offscreen(self):
        return (
            self.position[0]+self.rect.w < self.game.tilemap.left or
            self.position[1] > self.game.tilemap.right or
            self.position[1]+self.rect.h < self.game.tilemap.top or
            self.position[1] > self.game.tilemap.bottom
        )
