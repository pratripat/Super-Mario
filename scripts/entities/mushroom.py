from ..entity import Entity
import pygame

class Mushroom(Entity):
    def __init__(self, game, position, type):
        super().__init__(game.animations, type, position, 'moving')
        self.game = game
        self.velocity[0] = 1
        self.movement_timer = 0
        self.max_distance = 3696
        self.used = False

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        if self.movement_timer == 0:
            self.movement()
            self.move(self.game.entities.get_colliding_entities(), self.game.dt)
        else:
            self.movement_timer -= 1
            self.rect[1] -= 1

        super().update(self.game.dt)

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

    @property
    def offscreen(self):
        return (
            self.position[0]+self.image.get_width() < self.game.camera.scroll[0] or
            self.position[1] > self.game.tilemap.right or
            self.position[1] > self.game.tilemap.bottom
        )

    @property
    def far_from_mario(self):
        return abs(self.game.entities.mario.position[0]-self.position[0]) > self.max_distance
