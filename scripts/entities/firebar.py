from .fireball import Fireball
from ..funcs import *
import pygame, math

class Firebar:
    def __init__(self, game, id, position, index):
        self.id = id
        self.game = game
        self.index = index
        self.angle = 0
        self.n = int(self.id[-1])
        self.position = [position[0]+self.game.tilemap.RES//2, position[1]+self.game.tilemap.RES//2]
        self.fireballs = [Fireball(self.game, [self.game.tilemap.RES//2*i, 0], False) for i in range(self.n)]

        if self.index%2 == 1:
            self.position[0] += (self.game.tilemap.RES*self.n)//2

    def render(self):
        surface = pygame.Surface((self.game.tilemap.RES*self.n+self.game.tilemap.RES//2, self.game.tilemap.RES*self.n+self.game.tilemap.RES//2))
        surface.set_colorkey((0,0,0))

        for i, fireball in enumerate(self.fireballs):
            fireball.render(surface, [-surface.get_width()//2+self.game.tilemap.RES//4, -surface.get_height()//2+self.game.tilemap.RES//4])

        self.game.screen.blit(surface, (self.position[0]-surface.get_width()/2-self.game.camera.scroll[0], self.position[1]-surface.get_height()/2-self.game.camera.scroll[1]))

    def update(self):
        if self.index%2 == 0:
            self.angle += 0.03
        else:
            self.angle -= 0.03

        for i, fireball in enumerate(self.fireballs):
            px, py = fireball.position

            qx = math.cos(self.angle) * self.game.tilemap.RES//2*i
            qy = math.sin(self.angle) * self.game.tilemap.RES//2*i

            fireball.set_position((qx, qy))

            fireball.current_animation.run(self.game.dt)
