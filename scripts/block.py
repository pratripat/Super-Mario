from .funcs import *

class Block:
    def __init__(self, rect):
        self.rect = rect
        self.remove = False

    def up_collision(self, player, function):
        if player.velocity[1] < 0:
            player.position[1] += player.velocity[1]
            if rect_rect_collision(player.rect, self.rect):
                function()
                player.position[1] -= player.velocity[1]
                player.velocity[1] = 0
                return
            player.position[1] -= player.velocity[1]
