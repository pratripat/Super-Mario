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
from .score_system import Score_System

pygame.init()

class Game:
    def __init__(self):
        pygame.display.set_caption('Super Mario')
        self.screen = pygame.display.set_mode((960, 700), pygame.RESIZABLE+pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.framerate = 80
        self.game_timer = 0
        self.level = 0
        pygame.mouse.set_visible(False)

        self.camera = Camera()
        self.renderer = Renderer(self)
        self.animations = Animation_Handler()
        self.font = Font('data/graphics/spritesheet/font.png')
        self.ui = UI(self)
        self.score_system = Score_System(self)

        self.load_level()

    @property
    def dt(self):
        if self.clock.get_fps() == 0:
            return 0

        return 1/self.clock.get_fps()

    def load_level(self, level=0, filepath=None, world_type='overworld', position=[], transition_velocity=None, mario_dead=False):
        if level > 7:
            self.load_cutscene('data/configs/cutscenes/wait.json', self.play_end_music)
            return

        self.paused = False
        self.castle_clear = False
        self.level_clear = False
        self.flag_animation = False
        self.playing_cutscene = False
        self.reduce_coins = False
        self.game_over = False
        self.cutscene = None
        self.end_game = False
        self.cutscene_path = None

        if level != self.level:
            self.game_timer = 0

        if mario_dead:
            self.mario_data = 'small_mario'

            if self.entities.mario.lives == 0:
                self.game_over = True
                self.game_timer = -800
                world_level, world_type, cutscene_path = json.load(open('data/levels/level_order.json', 'r'))[level]
                world_number = world_level.split('/')[0].split('-')[1]

                level = (int(world_number)-1)*4

                self.entities.mario.lives = 3

                pygame.mixer.music.load('data/music/game_over.wav')
                pygame.mixer.music.play()

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

        if self.cutscene_path:
            self.load_cutscene(self.cutscene_path)

        if self.game_timer >= 240:
            self.play_music()

        pygame.event.clear()

    def run(self):
        self.clock.tick(self.framerate)
        self.game_timer += 1

        if self.end_game:
            self.play_end_music()

        if self.clock.get_fps() < 30:
            return

        if self.game_timer == 240:
            pygame.event.clear()
            self.play_music()

        if self.game_timer > 240:
            if self.reduce_coins:
                if self.ui.time > 0:
                    self.ui.time -= 1
                    self.score_system.add_score('others', 'time')
                else:
                    pygame.mixer.music.stop()

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
        elif self.game_timer >= 0:
            self.renderer.render_level_details()
        else:
            self.renderer.render_game_over()

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

    def play_end_music(self):
        self.end_game = True

        if pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load('data/music/end_music.wav')
        pygame.mixer.music.play(-1)

    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
