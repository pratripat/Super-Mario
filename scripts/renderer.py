import pygame, math, random

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        rendered = False
        visible_tiles = ['tiles']
        self.game.screen.fill((107,139,255))

        for tile in self.game.tilemap.tiles:
            if tile['layer'] == 0 and not rendered:
                self.game.entities.render()
                rendered = True
            if tile['id'] in visible_tiles:
                position = [tile['position'][0]+tile['offset'][0]-self.game.camera.scroll[0], tile['position'][1]+tile['offset'][1]-self.game.camera.scroll[1]]
                self.game.screen.blit(tile['image'], position)

        pygame.display.update()
