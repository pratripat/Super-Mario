import pygame, math, random
from .funcs import *

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        visible_tiles = ['background', 'ground', 'castle']

        self.game.screen.fill((0,0,0))
        self.render_tiles_with_id(visible_tiles)
        self.game.entities.render()
        self.render_tiles_with_id(['pipes', 'flagpole', 'castle_half'])

        pygame.display.update()

    def render_tiles_with_id(self, visible_tiles):
        for entity in self.game.tilemap.entities:
            if entity['id'] in visible_tiles:
                position = [entity['position'][0]+entity['offset'][0]-self.game.camera.scroll[0], entity['position'][1]+entity['offset'][1]-self.game.camera.scroll[1]]
                self.game.screen.blit(entity['image'], position)
