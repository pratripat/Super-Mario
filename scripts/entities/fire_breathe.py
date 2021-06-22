import pygame, json

class Firebreathe:
    def __init__(self, game, rect, velocity=[-3,0], target_rect=None):
        self.game = game
        self.velocity = velocity
        self.target_rect = target_rect
        self.position = list(rect.topleft)
        self.animation = self.game.animations.get_animation('fire_breathe')
        self.load_rect()

    def load_rect(self):
        scale = self.animation.animation_data.config['scale']
        data = json.load(open('data/configs/collision_boxes/firebreathe.json', 'r'))
        self.rect = pygame.Rect(self.position[0] + (data['offset'][0]*scale), self.position[1] + (data['offset'][1]*scale), data['size'][0]*scale, data['size'][1]*scale)

    def render(self):
        self.animation.render(self.game.screen, [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]], flipped=[self.velocity[0]>0, False])

    def update(self):
        if not self.on_screen:
            return

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.rect[0] += self.velocity[0]
        self.rect[1] += self.velocity[1]

        if not self.target_rect:
            return

        if self.target_rect[1] > self.rect[1]:
            self.position[1] += 1
            self.rect[1] += 1
        if self.target_rect[1] < self.rect[1]:
            self.position[1] -= 1
            self.rect[1] -= 1
        if self.target_rect[1] == self.rect[1]:
            self.target_rect = None

    @property
    def on_screen(self):
        return (
            -self.animation.image.get_width() < self.position[0]-self.game.camera.scroll[0] < self.game.screen.get_width() and
            -self.animation.image.get_height() < self.position[1]-self.game.camera.scroll[1] < self.game.screen.get_height()
        )
