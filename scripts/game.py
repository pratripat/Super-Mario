import pygame, sys, json, os
from .entity_manager import Entity_Manager
from .animation_handler import Animation_Handler
from .renderer import Renderer
from .tilemap import Tilemap
from .camera import Camera
from .pipe_guides import Pipe_Guides
from .lift_spawner import Lift_Spawner_Manager

pygame.init()

class Game:
    def __init__(self):
        pygame.display.set_caption('Super Mario')
        self.screen = pygame.display.set_mode((960, 700), pygame.RESIZABLE+pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.animations = Animation_Handler()
        self.renderer = Renderer(self)
        self.camera = Camera()

        self.load_level()

    @property
    def dt(self):
        if self.clock.get_fps() == 0:
            return 0

        return 1/self.clock.get_fps()

    def load_level(self, level=0, filepath=None, world_type='overworld', position=[], transition_velocity=None):
        try:
            self.mario_data = self.entities.mario.id
        except:
            self.mario_data = 'small_mario'

        self.level = level

        if not filepath:
            level, self.world_type = json.load(open('data/levels/level_order.json', 'r'))[level]
        else:
            level = filepath
            self.world_type = world_type

        self.tilemap = Tilemap(f'data/levels/{level}.json')
        self.pipe_guides = Pipe_Guides(self)
        self.lift_spawners = Lift_Spawner_Manager(self)
        self.entities = Entity_Manager(self, position, transition_velocity)

        self.renderer.refresh()

        self.camera.scroll[0] = self.entities.mario.position[0]-self.screen.get_width()/2
        self.camera.set_target(self.entities.mario)

        self.paused = False
        self.level_finished = False

        self.play_music()

    def run(self):
        self.clock.tick(80)

        if self.clock.get_fps() < 30:
            return

        self.camera.update(self.screen, self.tilemap)
        self.lift_spawners.update()
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
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.entities.mario.directions['up'] = True
                    self.entities.mario.directions['down'] = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.entities.mario.directions['left'] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.entities.mario.directions['right'] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.entities.mario.crouching = True
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.entities.mario.running = True
                    self.entities.mario.shoot_fireball()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.entities.mario.directions['up'] = False
                    self.entities.mario.directions['down'] = True
                    self.entities.mario.airtimer = 15
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.entities.mario.directions['left'] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.entities.mario.directions['right'] = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.entities.mario.crouching = False
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.entities.mario.running = False

    def play_music(self):
        pygame.mixer.music.load('data/music/main_theme.wav')
        pygame.mixer.music.play(-1)

        if 'background' not in [entity['id'] for entity in self.tilemap.entities]:
            pygame.mixer.music.load('data/music/underground.wav')
            pygame.mixer.music.play(-1)

    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
