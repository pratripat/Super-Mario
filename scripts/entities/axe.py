from ..funcs import *

class Axe:
    def __init__(self, game, rect):
        self.game = game
        self.rect = rect
        self.animation = self.game.animations.get_animation('axe')

    def render(self):
        self.animation.render(self.game.screen, (self.rect[0]-self.game.camera.scroll[0], self.rect[1]-self.game.camera.scroll[1]))

    def update(self):
        self.animation.run(self.game.dt)

        if rect_rect_collision(self.rect, self.game.entities.mario.rect):
            for enemy in self.game.entities.enemies:
                enemy.dead = enemy.falling = True

            self.game.tilemap.remove_entity('axe')
            self.game.tilemap.remove_entity('chain')
            self.game.entities.axes = []

            pygame.mixer.music.load('data/music/bowser_die.wav')
            pygame.mixer.music.play()
            pygame.mixer.music.queue('data/music/castle_clear.wav')
