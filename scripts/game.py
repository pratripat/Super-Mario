import pygame, sys
from .entity_manager import Entity_Manager
from .animation_handler import Animation_Handler
from .renderer import Renderer
from .tilemap import TileMap
from .camera import Camera

pygame.init()

class Game:
    def __init__(self):
        pygame.display.set_caption('Super Mario')
        self.screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.animations = Animation_Handler()
        self.tilemap = TileMap('data/levels/level1.json')
        self.entities = Entity_Manager(self)
        self.renderer = Renderer(self)
        self.camera = Camera()
        self.camera.set_target(self.entities.mario)
        self.camera.set_movement(0.05)

        pygame.mixer.music.load('data/music/main_theme.wav')
        pygame.mixer.music.play(-1)

    @property
    def dt(self):
        if self.clock.get_fps() == 0:
            return 0

        return 1/self.clock.get_fps()

    def run(self):
        self.clock.tick(80)

        self.camera.update(self.screen, [[self.tilemap.left, self.tilemap.right], [self.tilemap.top, self.tilemap.bottom]])
        self.entities.run()

        self.renderer.render()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_w:
                    self.entities.mario.directions['up'] = True
                    self.entities.mario.directions['down'] = False
                if event.key == pygame.K_a:
                    self.entities.mario.directions['left'] = True
                if event.key == pygame.K_d:
                    self.entities.mario.directions['right'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.entities.mario.directions['up'] = False
                    self.entities.mario.directions['down'] = True
                if event.key == pygame.K_a:
                    self.entities.mario.directions['left'] = False
                if event.key == pygame.K_d:
                    self.entities.mario.directions['right'] = False

    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
