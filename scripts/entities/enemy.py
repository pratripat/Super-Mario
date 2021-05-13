from ..entity import Entity
from ..funcs import *

class Enemy(Entity):
    def __init__(self, game, position, type, animation_id):
        super().__init__(game.animations, type, position, animation_id)
        self.game = game
        self.dead = False
        self.remove = False

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        super().update(self.game.dt)

        if self.dead:
            if int(self.current_animation.frame) == self.current_animation.animation_data.duration():
                self.remove = True
            return

        self.movement()
        self.move(self.game.entities.get_colliding_entities(), self.game.dt)

        if rect_rect_collision(self.rect, self.game.entities.mario.rect):
            self.game.entities.mario.change_state('enemy')

    def stomp(self, function=None):
        if self.game.entities.mario.velocity[1] > 0:
            rect = self.game.entities.mario.rect.copy()
            rect[1] += self.game.entities.mario.velocity[1]

            if rect_rect_collision(rect, self.rect):
                if function:
                    function()

                self.game.entities.mario.rect[1] -= self.game.entities.mario.velocity[1]
                self.game.entities.mario.velocity[1] *= -1

    def movement(self):
        if self.collisions['bottom']:
            self.velocity[1] = 1

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] *= -1

        if self.velocity[0] < 0:
            self.flip(True)
        else:
            self.flip(False)

        self.velocity[1] += 1
