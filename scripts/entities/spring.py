from ..entity import Entity
from ..funcs import *
import json

class Spring(Entity):
    def __init__(self, game, rect):
        super().__init__(game.animations, 'spring', list(rect.topleft), 'static')
        self.game = game
        self.type = 'spring'
        self.offset[1] += 15
        self.rect[1] += 15
        self.rect[3] -= 15

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        super().update(self.game.dt)

        if self.game.entities.mario.rect[0]+self.game.entities.mario.image.get_width() > self.position[0] and self.game.entities.mario.rect[0] < self.position[0]+self.image.get_width():
            if self.game.entities.mario.rect[1]+self.game.entities.mario.image.get_height() >= self.position[1]+self.image.get_height()/4 and self.game.entities.mario.rect[1]+self.game.entities.mario.image.get_height() < self.position[1]+self.image.get_height() and self.game.entities.mario.directions['down']:
                key_presses = [event for event in pygame.event.get() if event.type == pygame.KEYDOWN and event.key in [pygame.K_w, pygame.K_SPACE]]

                if len(key_presses):
                    self.game.entities.mario.velocity[1] = -30
                    self.game.entities.mario.rect[1] += self.game.entities.mario.velocity[1]
                    self.game.entities.mario.directions['up'] = True
                    self.game.entities.mario.airtimer = 0
                    self.game.entities.mario.jump_sfx.play()
                    self.set_animation('shrink')
                    self.current_animation.frame = 0

        if self.game.entities.mario.velocity[1] > 1 and self.game.entities.mario.directions['down']:
            if self.game.entities.mario.dead:
                return

            rect = self.game.entities.mario.rect.copy()
            rect[1] += self.game.entities.mario.velocity[1]

            if rect_rect_collision(rect, self.rect):
                self.game.entities.mario.velocity[1] *= -1
                self.set_animation('shrink')
                self.current_animation.frame = 0
