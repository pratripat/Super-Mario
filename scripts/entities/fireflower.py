from ..entity import Entity
from ..funcs import *

class FireFlower(Entity):
    def __init__(self, game, position):
        super().__init__(game.animations, 'fireflower', position, 'updating')
        self.game = game
        self.movement_timer = 0
        self.used = False

    def render(self):
        super().render(self.game.screen, self.game.camera.scroll)

    def update(self):
        if self.movement_timer > 0:
            self.movement_timer -= 1
            self.rect[1] -= 1

        super().update(self.game.dt)

        if rect_rect_collision(self.rect, self.game.entities.mario.rect):
            self.game.entities.mario.change_state(self.id)
            self.used = True

    @property
    def offscreen(self):
        return (
            self.position[0]+self.image.get_width() < self.game.camera.scroll[0] or
            self.position[1] > self.game.tilemap.right or
            self.position[1] > self.game.tilemap.bottom
        )
