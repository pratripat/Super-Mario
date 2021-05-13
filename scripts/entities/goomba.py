import pygame
from .enemy import Enemy

class Goomba(Enemy):
    def __init__(self, game, rect):
        super().__init__(game, [rect[0], rect[1]], 'goomba', 'moving')
        self.velocity[0] = 1
        self.stomp_sfx = pygame.mixer.Sound('data/sfx/stomp.wav')

    def update(self):
        if not self.on_screen:
            return

        super().update()
        self.stomp(self.die)

    def die(self):
        self.current_animation_id = f'{self.id}_die'
        self.current_animation = self.animations.get_animation(self.current_animation_id)
        self.dead = True
        self.stomp_sfx.play()

    @property
    def on_screen(self):
        return (
            0 < self.position[0]-self.game.camera.scroll[0] < self.game.screen.get_width() and
            0 < self.position[1]-self.game.camera.scroll[1] < self.game.screen.get_height()
        )
