from ..entity import Entity
import pygame

class Mushroom(Entity):
    def __init__(self, game, position, type):
        super().__init__(game.animations, type, position, False, 'moving')
        self.game = game
        self.type = type
        self.velocity[0] = 1
        self.used = False

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        self.movement()
        self.move(self.game.entities.get_colliding_entities(), self.game.dt)
        super().update(self.game.dt)

    def movement(self):
        if self.collisions['bottom']:
            self.velocity[1] = 0

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] *= -1

        self.velocity[1] += 1

    @property
    def offscreen(self):
        return (
            self.position[0]+self.image.get_width() < self.game.camera.scroll[0] or
            self.position[1] > self.game.tilemap.right or
            self.position[1] > self.game.tilemap.bottom
        )
