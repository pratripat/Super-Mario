import pygame, math, random, json
from .funcs import *

class Renderer:
    def __init__(self, game):
        self.game = game

    def refresh(self):
        self.background_color = (0,0,0)
        if self.game.world_type in ['overworld', 'underwater']:
            self.background_color = (107, 139, 255)

        self.texts = []

    def render(self):
        self.game.screen.fill(self.background_color)
        self.render_tiles_with_id(['decorations', 'background'])
        self.render_tiles_with_id(['castle', 'ground', 'chain', 'toad', 'princess'])
        self.game.entities.render()
        self.render_tiles_with_id(['pipes', 'flagpole', 'castle_half'])

        for text in self.texts:
            self.game.font.render(self.game.screen, text['text'], text['position'], scale=3, color=(255,255,255))

        self.game.ui.render()

        pygame.display.update()

    def render_level_details(self):
        self.game.screen.fill((0,0,0))

        mario_image = pygame.image.load('data/graphics/animations/small_mario_idle/0.png').convert()
        mario_image = pygame.transform.scale(mario_image, (mario_image.get_width()*3, mario_image.get_height()*3))

        font_surface = self.game.font.get_surface(f'  *    {self.game.entities.mario.lives}')
        font_surface = pygame.transform.scale(font_surface, (font_surface.get_width()*3, font_surface.get_height()*3))
        position = self.game.font.render(self.game.screen, f'  *    {self.game.entities.mario.lives}', [self.game.screen.get_width()/2+mario_image.get_width()*2, self.game.screen.get_width()/2-mario_image.get_height()], center=[True, False], scale=3)

        self.game.screen.blit(mario_image, [position[0]-mario_image.get_width(), position[1]-mario_image.get_height()+font_surface.get_height()])

        level, world_type, cutscene_path = json.load(open('data/levels/level_order.json', 'r'))[self.game.level]
        world = level.split('.')[0].split('/')

        self.game.font.render(self.game.screen, f'WORLD {world[-2][-1]}-{world[-1]}', [self.game.screen.get_width()/2+mario_image.get_width()/2, position[1]-font_surface.get_height()*5], center=[True, True], scale=3)

        self.game.ui.render()

        pygame.display.update()

    def render_tiles_with_id(self, visible_tiles):
        for entity in self.game.tilemap.entities:
            if entity['id'] in visible_tiles:
                position = [entity['position'][0]+entity['offset'][0]-self.game.camera.scroll[0], entity['position'][1]+entity['offset'][1]-self.game.camera.scroll[1]]
                self.game.screen.blit(entity['image'], position)
