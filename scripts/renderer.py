import pygame, math, random
from .funcs import *

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        visible_tiles = ['ground']
        self.game.screen.fill((107,139,255))

        for entity in self.game.tilemap.entities:
            if entity['id'] in visible_tiles:
                position = [entity['position'][0]+entity['offset'][0]-self.game.camera.scroll[0], entity['position'][1]+entity['offset'][1]-self.game.camera.scroll[1]]
                self.game.screen.blit(entity['image'], position)

        self.game.entities.render()

        pygame.display.update()
