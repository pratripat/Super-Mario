import pygame

class Coin:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect
        self.animation = self.game.animations.get_animation(f'{self.game.world_type}_coin')
        self.coin_sfx = pygame.mixer.Sound('data/sfx/coin.wav')

    def render(self):
        self.animation.render(self.game.screen, (self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.game.camera.scroll[1]))

    def update(self):
        self.animation.run(self.game.dt)
