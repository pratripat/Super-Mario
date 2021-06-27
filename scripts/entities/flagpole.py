from ..funcs import *
import pygame, json

class Flagpole:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect
        self.flag_taken_down = False
        self.load_level = 0
        self.waiting_timer = 40
        self.flag_image = pygame.image.load('data/graphics/images/flag.png').convert()
        self.flag_image = pygame.transform.scale(self.flag_image, (self.flag_image.get_width()*3, self.flag_image.get_height()*3))
        self.flag_image.set_colorkey((0,0,0))
        self.flag_position = [self.rect[0]+self.rect[2]/2-self.flag_image.get_width(), self.rect[1]+24]

    def render(self):
        self.game.screen.blit(self.flag_image, (self.flag_position[0]-self.game.camera.scroll[0], self.flag_position[1]-self.game.camera.scroll[1]))

        pygame.draw.rect(self.game.screen, (255,0,0), (self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.game.camera.scroll[1], self.rect[2], self.rect[3]))

    def run(self):
        if self.game.playing_cutscene:
            return

        if self.flag_taken_down and self.waiting_timer == 0:
            self.game.paused = False
            self.game.flag_animation = False
            self.game.entities.mario.running = False
            self.game.entities.mario.directions = {k:False for k in ['up', 'down', 'left', 'right']}
            self.game.entities.mario.directions['down'] = True

            self.game.load_cutscene('data/configs/cutscenes/flagpole.json', self.load_next_level)

            return
        elif self.flag_taken_down:
            self.waiting_timer -= 1

        rect = self.game.entities.mario.rect.copy()

        if rect_rect_collision(self.game.entities.mario.rect, self.rect):
            if not self.game.paused:
                pygame.mixer.music.load('data/music/flagpole.wav')
                pygame.mixer.music.play()

            self.game.paused = True
            self.game.flag_animation = True
            self.game.entities.mario.flip(False)
            self.game.entities.mario.set_animation('hold')

            self.game.entities.mario.rect[0] = self.rect[0]-self.game.entities.mario.rect[2]+12
            self.game.entities.mario.rect[1] += 4
            self.flag_position[1] += 4

            if self.game.entities.mario.rect[1] > self.rect[1]+self.rect[3]-rect[3]:
                self.game.entities.mario.rect[1] = self.rect[1]+self.rect[3]-rect[3]

            if not self.flag_position[1]+self.flag_image.get_height() > self.rect[1]+self.rect[3]-self.game.tilemap.RES*0.5 and pygame.mixer.music.get_busy():
                return

            pygame.mixer.music.load('data/music/stage_clear.wav')
            pygame.mixer.music.play()

            self.game.entities.mario.rect[1] = self.rect[1]+self.rect[3]-rect[3]
            self.game.entities.mario.velocity[1] = -1
            self.flag_taken_down = True

            self.game.entities.mario.rect[0] = self.rect[0]+self.game.entities.mario.rect[2]-12
            self.game.entities.mario.flip(True)

    def load_next_level(self):
        if not pygame.mixer.music.get_busy():
            self.game.load_level(self.game.level+1)
