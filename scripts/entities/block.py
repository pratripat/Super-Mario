from ..funcs import *
import math

class Block:
    def __init__(self, rect, type):
        self.initial_rect = rect
        self.type = type
        self.remove = False
        self.updating_offset = False
        self.offset = 0
        self.offset_counter = 0
        self.hits = 1

    def update_offset(self, function=None):
        if not self.updating_offset:
            return

        self.offset_counter += 0.1
        self.offset = math.sin(self.offset_counter)*10

        if self.offset <= 0:
            self.updating_offset = False
            self.offset = 0
            self.offset_counter = 0

            if function:
                function()

    def up_collision(self, player, function):
        if player.velocity[1] < 0:
            rect = player.rect.copy()
            rect[1] += player.velocity[1]
            if rect_rect_collision(rect, self.rect):
                function()
                rect[1] -= player.velocity[1]
                player.velocity[1] = 0

                if self.hits > 0:
                    self.hits -= 1
                    self.updating_offset = True
                return

            rect[1] -= player.velocity[1]

    @property
    def rect(self):
        return pygame.Rect(self.initial_rect[0], self.initial_rect[1]-self.offset, self.initial_rect[2], self.initial_rect[3])
