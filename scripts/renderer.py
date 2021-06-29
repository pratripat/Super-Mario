import pygame, math, random
from .funcs import *

class Renderer:
    def __init__(self, game):
        self.game = game
        self.background_image = pygame.image.load('data/graphics/images/background.png').convert()
        self.background_image.set_colorkey((0,0,0))
        self.rendering_background = False

    def refresh(self):
        self.background_color = (0,0,0)
        if self.game.world_type == 'overworld':
            self.background_color = (107, 139, 255)
            self.rendering_background = True
            self.offset = self.game.tilemap.left

    def render_background(self):
        self.game.screen.fill(self.background_color)
        if self.rendering_background:
            position = self.game.entities.mario.position[0] - (self.game.entities.mario.position[0] % self.background_image.get_width()) + self.offset

            self.game.screen.blit(self.background_image, (position-self.game.camera.scroll[0], -self.game.camera.scroll[1]))
            self.game.screen.blit(self.background_image, (position-self.background_image.get_width()-self.game.camera.scroll[0], -self.game.camera.scroll[1]))
            self.game.screen.blit(self.background_image, (position+self.background_image.get_width()-self.game.camera.scroll[0], -self.game.camera.scroll[1]))

    def render(self):
        self.render_background()
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
