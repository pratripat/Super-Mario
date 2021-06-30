import pygame, math, random
from .funcs import *

class Renderer:
    def __init__(self, game):
        self.game = game

    def refresh(self):
        self.background_color = (0,0,0)
        if self.game.world_type == 'overworld':
            self.background_color = (107, 139, 255)

    def render(self):
        self.game.screen.fill(self.background_color)
        self.render_tiles_with_id(['decorations', 'background'])
        self.render_tiles_with_id(['castle', 'ground', 'chain', 'toad', 'princess'])
        self.game.entities.render()
        self.render_tiles_with_id(['pipes', 'flagpole', 'castle_half'])

        pygame.display.update()

    def render_tiles_with_id(self, visible_tiles):
        for entity in self.game.tilemap.entities:
            if entity['id'] in visible_tiles:
                position = [entity['position'][0]+entity['offset'][0]-self.game.camera.scroll[0], entity['position'][1]+entity['offset'][1]-self.game.camera.scroll[1]]
                self.game.screen.blit(entity['image'], position)
