import pygame, sys, json, os
from .entity_manager import Entity_Manager
from .animation_handler import Animation_Handler
from .renderer import Renderer
from .tilemap import Tilemap
from .camera import Camera
from .pipe_guides import Pipe_Guides
from .lift_spawner import Lift_Spawner_Manager
from .cutscene_manager import Cutscene
from .font_renderer import Font
from .ui import UI

pygame.init()

class Game:
    def __init__(self):
        pygame.display.set_caption('Super Mario')
        self.screen = pygame.display.set_mode((960, 700), pygame.RESIZABLE+pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.framerate = 80
        pygame.mouse.set_visible(False)

        self.camera = Camera()
        self.renderer = Renderer(self)
        self.animations = Animation_Handler()
        self.font = Font('data/graphics/spritesheet/font.png')
        self.ui = UI(self)

        self.load_level()

    @property
    def dt(self):
        if self.clock.get_fps() == 0:
            return 0

        return 1/self.clock.get_fps()

    def load_level(self, level=0, filepath=None, world_type='overworld', position=[], transition_velocity=None, mario_dead=False):
        self.paused = False
        self.castle_clear = False
        self.flag_animation = False
        self.playing_cutscene = False
        self.cutscene = None
        self.cutscene_path = None
        self.game_timer = 0

        if mario_dead:
            self.mario_data = 'small_mario'
        else:
            try:
                self.mario_data = self.entities.mario.id
            except:
                self.mario_data = 'small_mario'

        self.level = level

        if not filepath:
            level, self.world_type, self.cutscene_path = json.load(open('data/levels/level_order.json', 'r'))[level]
            self.ui.refresh(level)

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

        self.play_music()

        if self.cutscene_path:
            self.load_cutscene(self.cutscene_path)

    def run(self):
        self.clock.tick(self.framerate)
        self.game_timer += 1

        if self.clock.get_fps() < 30:
            return

        if self.playing_cutscene:
            self.cutscene.update()

        if self.playing_cutscene and self.cutscene.finished:
            if self.cutscene.function:
                self.cutscene.function(*self.cutscene.args)

            if self.cutscene and self.cutscene.finished:
                self.playing_cutscene = False
                self.cutscene = None

        self.camera.update(self.screen, self.tilemap)
        self.lift_spawners.update()
        self.entities.run()
        self.ui.update()

        self.renderer.render()

    def event_loop(self):
        self.mario_jumped = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.playing_cutscene:
                    continue

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.entities.mario.directions['up'] = True
                    self.entities.mario.directions['down'] = False
                    self.mario_jumped = True

                    if self.world_type == 'underwater':
                        self.entities.mario.airtimer = 0

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
                    if not self.world_type == 'underwater':
                        self.entities.mario.directions['up'] = False
                        self.entities.mario.directions['down'] = True
                        self.entities.mario.airtimer = self.entities.mario.max_airtimer
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.entities.mario.directions['left'] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.entities.mario.directions['right'] = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.entities.mario.crouching = False
                    self.entities.mario.load_collision_rect(self.entities.mario.id)
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.entities.mario.running = False

    def play_music(self):
        pygame.mixer.music.load(f'data/music/{self.world_type}.wav')
        pygame.mixer.music.play(-1)

    def load_cutscene(self, path, function=None, args=[]):
        data = json.load(open(path, 'r'))
        data['sequential_commands'][0]['target_position'][0] *= self.tilemap.RES
        data['sequential_commands'][0]['target_position'][0] += self.entities.mario.position[0]

        self.playing_cutscene = True
        self.cutscene = Cutscene({'mario':self.entities.mario}, self.font, **data, function=function, args=args)

    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
