from ..funcs import *
import math

class Block:
    def __init__(self, rect, type):
        self.rect = rect
        self.type = type
        self.remove = False
        self.updating_offset = False
        self.offset = 0
        self.offset_counter = 0
        self.hits = 1

    def update_offset(self):
        if not self.hits > 0 or not self.updating_offset:
            return

        self.offset_counter += 0.1
        self.offset = math.sin(self.offset_counter)*10

        if self.offset <= 0:
            self.updating_offset = False
            self.offset = 0
            self.offset_counter = 0
            self.hits -= 1

    def up_collision(self, player, function):
        if player.velocity[1] < 0:
            player.position[1] += player.velocity[1]
            if rect_rect_collision(player.rect, self.rect):
                function()
                player.position[1] -= player.velocity[1]
                player.velocity[1] = 0
                self.updating_offset = True
                return
            player.position[1] -= player.velocity[1]
